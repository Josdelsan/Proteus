# ==========================================================================
# File: test_string_properties.py
# Description: pytest file for PROTEUS string and markdown properties
# Date: 15/10/2022
# Version: 0.1
# Author: Amador Durán Toro
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
    STRING_PROPERTY_TAG,           \
    MARKDOWN_PROPERTY_TAG,         \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    PropertyFactory
 
# --------------------------------------------------------------------------
# String & markdown property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('property_tag', [STRING_PROPERTY_TAG, MARKDOWN_PROPERTY_TAG])
@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value',        [str(), 'test value', 'test <>& value', 7.5 ])
@pytest.mark.parametrize('new_value',    [str(), 'new test value', 'new test <>& value', -7.5])

def test_string_and_markdown_properties(property_tag, name, category, value, new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of string and markdown properties.
    """
    # Prepare XML element
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
    assert(property.value == str(value))
    assert(property.category == category)
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}"><![CDATA[{value}]]></{property_tag}>'
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
    assert(evolved_property.value == str(new_value))
    assert(evolved_property.category == category)
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}"><![CDATA[{new_value}]]></{property_tag}>'
    )
