# ==========================================================================
# File: test_properties.py
# Description: pytest file for PROTEUS properties (general)
# Date: 14/10/2022
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

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import NAME_TAG, CATEGORY_TAG

from proteus.model.property import \
    STRING_PROPERTY_TAG,           \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    PropertyFactory
    
# --------------------------------------------------------------------------
# General property tests
# --------------------------------------------------------------------------

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
        property_element.set(NAME_TAG, name)
    
    if category:
        property_element.set(CATEGORY_TAG, category)
    
    property_element.text = 'test text'

    property = PropertyFactory.create(property_element)

    assert(property.name == name_expected)
    assert(property.value == 'test text')
    assert(property.category == category_expected)
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_element.tag} name="{name_expected}" category="{category_expected}"><![CDATA[{property.value}]]></{property_element.tag}>'
    )
