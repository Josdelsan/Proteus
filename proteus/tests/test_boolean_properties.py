# ==========================================================================
# File: test_boolean_properties.py
# Description: pytest file for PROTEUS boolean properties
# Date: 18/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# ==========================================================================
# Update: 21/10/2022 (Amador)
# Description:
# - Code review.
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
    BOOLEAN_PROPERTY_TAG,          \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    PropertyFactory
 
# --------------------------------------------------------------------------
# Boolean property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, expected_value, expected_xml_value',
    [
        ('false', False, 'false'),
        ('true', True, 'true'),
        ('True', True, 'true'),
        ('False', False, 'false'),
        (str(), False, 'false'),
        (7.5, False, 'false'),
        (7, False, 'false'),
        ('test value', False, 'false')
    ]
)
@pytest.mark.parametrize('new_value, expected_new_value, expected_new_xml_value',
    [   
        ('false', False, 'false'),
        ('true', True, 'true'),
        ('True', True, 'true'),
        ('False', False, 'false'),
        (str(), False, 'false'),
        (7.5, False, 'false'),
        (7, False, 'false'),
        ('test value', False, 'false')
    ]
)

def test_boolean_properties(name, category, value, expected_value, expected_xml_value, new_value, expected_new_value, expected_new_xml_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of boolean properties.
    """
    # Prepare XML element
    property_tag = BOOLEAN_PROPERTY_TAG
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
    assert(property.category == category)    
    assert(property.value == expected_value)
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_xml_value}</{property_tag}>'
    )

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name == property.name)
    assert(cloned_property.category == property.category)
    assert(cloned_property.value == property.value)

    # Clone the property changing value
    evolved_property = property.clone(new_value)

    # Check cloned property
    assert(evolved_property.name == name)
    assert(evolved_property.category == category)
    assert(evolved_property.value == expected_new_value)    
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_new_xml_value}</{property_tag}>'
    )
