# ==========================================================================
# File: test_properties.py
# Description: pytest file for the PROTEUS properties
# Date: 14/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

#from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

#import validators
import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import \
    CATEGORY_TAG, DEFAULT_NAME, NAME_TAG, DEFAULT_CATEGORY

from proteus.model.property import \
    PropertyFactory, StringProperty, STRING_PROPERTY_TAG
    
# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize( 
    "name, name_expected, category, category_expected",
    [
        (str(),       DEFAULT_NAME, str(),           DEFAULT_CATEGORY),
        (str(),       DEFAULT_NAME, 'test_category', 'test_category' ),
        ('test_name', 'test_name',  str(),           DEFAULT_CATEGORY),
        ('test_name', 'test_name',  'test_category', 'test_category' )
    ]
)   
def test_property_name_and_category(name, name_expected, category, category_expected):
    """
    It tests whether a (string) property is correctly created with and
    without name and category.
    """
    property_element : ET._Element = ET.Element(STRING_PROPERTY_TAG)
 
    if name:
        property_element.set(NAME_TAG, name)
    
    if category:
        property_element.set(CATEGORY_TAG, category)
    
    property_element.text = 'test text'

    property : StringProperty = PropertyFactory.create(property_element)

    assert(property.name == name_expected)
    assert(property.value == 'test text')
    assert(property.category == category_expected)
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<stringProperty name="{name_expected}" category="{category_expected}"><![CDATA[{property.value}]]></stringProperty>'
    )

