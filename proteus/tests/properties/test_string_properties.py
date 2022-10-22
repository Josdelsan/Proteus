# ==========================================================================
# File: test_string_properties.py
# Description: pytest file for PROTEUS string and markdown properties
# Date: 22/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# ==========================================================================
# Update: 22/10/2022 (Amador)
# Description:
# - Common code extracted as fixtures.
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

from proteus.model.property import STRING_PROPERTY_TAG, MARKDOWN_PROPERTY_TAG         

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------

import proteus.tests.properties.fixtures as fixtures

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
    # Create property from XML element
    (property, name, category) = fixtures.create_property(property_tag, name, category, value)

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
