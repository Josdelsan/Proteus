# ==========================================================================
# File: test_properties.py
# Description: pytest file for PROTEUS properties (general)
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

from proteus.model import NAME_ATTR, CATEGORY_ATTR

from proteus.model.properties import \
    STRING_PROPERTY_TAG,           \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    PropertyFactory

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------

import proteus.tests.fixtures as fixtures

# --------------------------------------------------------------------------
# General property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('property_tag', ['WrongProperty', 'wrong_property'])
@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value',        [str(), 'test value', 'test <>& value', 7.5])

def test_wrong_property_tag(property_tag, name, category, value):
    """
    It tests that PropertyFactory returns None when the XML
    element is not a property element.
    """
    # Create property from XML element
    (property, name, category) = fixtures.create_property(property_tag, name, category, value)

    assert(property is None)


@pytest.mark.parametrize('name, name_expected', 
    [(str(), DEFAULT_NAME), ('test_name', 'test_name')])

@pytest.mark.parametrize('category, category_expected', 
    [(str(), DEFAULT_CATEGORY), ('test_category', 'test_category')])

def test_property_name_and_category(name, name_expected, category, category_expected):
    """
    It tests whether a (string) property is correctly created with and
    without name and category.
    """
    property_element = ET.Element(STRING_PROPERTY_TAG)
 
    if name:
        property_element.set(NAME_ATTR, name)
    
    if category:
        property_element.set(CATEGORY_ATTR, category)
    
    property_element.text = 'test text'

    property = PropertyFactory.create(property_element)

    assert(property.name == name_expected)
    assert(property.value == 'test text')
    assert(property.category == category_expected)
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_element.tag} name="{name_expected}" category="{category_expected}"><![CDATA[{property.value}]]></{property_element.tag}>'
    )
