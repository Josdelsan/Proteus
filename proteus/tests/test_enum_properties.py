# ==========================================================================
# File: test_enum_properties.py
# Description: pytest file for PROTEUS enum properties
# Date: 18/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import CHOICES_TAG, NAME_TAG, CATEGORY_TAG

from proteus.model.property import \
    ENUM_PROPERTY_TAG,           \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,       \
    EnumProperty,            \
    PropertyFactory,             \
    Property
 
# --------------------------------------------------------------------------
# Enum property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, choices, expected_value',
    [
        ("low", "low medium high", "low"),
        ("not low", "low medium high", None),
        (str(), "low medium high", None),
        (1, "low medium high", None)
    ]
)
@pytest.mark.parametrize('new_value, new_choices, expected_new_value',
    [   
        
        ("medium", "low medium high", "medium"),
        ("not low", "bottom top", None),
        (str(), "low medium high", None),
        (1, "low medium high", None)
    ]
)

def test_float_properties(name, category, value, choices, expected_value, new_value, new_choices, expected_new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of float properties.
    """
    # Prepare XML element
    property_tag = ENUM_PROPERTY_TAG
    property_element = ET.Element(property_tag)
    property_element.set(CHOICES_TAG, choices)

    if name:
        property_element.set(NAME_TAG, name)
    else:
        name = DEFAULT_NAME
    
    property_element.text = str(value)
    
    if category:
        property_element.set(CATEGORY_TAG, category)
    else:
        category = DEFAULT_CATEGORY
    

    # Create property from XML element
    property = PropertyFactory.create(property_element)

    # Check property
    assert(property.name == name)
    assert(property.choices == choices)
    assert(property.category == category)
    if (expected_value == None):
        assert(property.value in property.choices)
    else:
        assert(property.value == expected_value)
        assert(
            ET.tostring(property.generate_xml()).decode() ==
            f'<{property_tag} name="{name}" category="{category}" choices="{choices}">{expected_value}</{property_tag}>'
        )
        

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name == property.name)
    assert(cloned_property.value == property.value)
    assert(cloned_property.choices == property.choices)
    assert(cloned_property.category == property.category)

    # Clone the property changing value
    evolved_property : EnumProperty = property.clone(new_value, new_choices)

    # Check cloned property
    assert(evolved_property.name == name)
    
    assert(evolved_property.choices == new_choices)
    assert(evolved_property.category == category)
    if (expected_new_value == None):
        assert(evolved_property.value in evolved_property.choices)
    else:
        assert(evolved_property.value == expected_new_value)
        assert(
            ET.tostring(evolved_property.generate_xml()).decode() ==
            f'<{property_tag} name="{name}" category="{category}" choices="{new_choices}">{expected_new_value}</{property_tag}>'
        )
    
