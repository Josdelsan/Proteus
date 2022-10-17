# ==========================================================================
# File: test_integer_properties.py
# Description: pytest file for PROTEUS Integer properties
# Date: 17/10/2022
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

from proteus.model import NAME_TAG, CATEGORY_TAG

from proteus.model.property import \
    INTEGER_PROPERTY_TAG,           \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    PropertyFactory
 
# --------------------------------------------------------------------------
# String & markdown property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, expected_value',
    [
        (1, 1),
        (str(), 0),
        ('test value', 0),
        (7.5, 0)
    ]
)
@pytest.mark.parametrize('new_value, expected_new_value',
    [
        (2,2),
        ("test value", 0),
        (9.5, 0),
        ('new test value', 0)
    ]
)

def test_string_and_markdown_properties(name, category, value, expected_value, new_value, expected_new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of string and markdown properties.
    """
    # Prepare XML element
    property_tag = INTEGER_PROPERTY_TAG
    property_element = ET.Element(property_tag)

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
    assert(property.value == expected_value)
    assert(property.category == category)
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_value}</{property_tag}>'
    )

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name == property.name)
    assert(cloned_property.value == property.value)
    assert(cloned_property.category == property.category)

    # Clone the property changing value
    evolved_property = property.clone(new_value)

    # Check cloned property
    assert(evolved_property.name == name)
    assert(evolved_property.value == expected_new_value)
    assert(evolved_property.category == category)
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_new_value}</{property_tag}>'
    )
