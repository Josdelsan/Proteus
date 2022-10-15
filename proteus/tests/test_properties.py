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

import copy
import datetime

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
    CATEGORY_TAG, DEFAULT_NAME, NAME_TAG

from proteus.model.property import \
    DEFAULT_CATEGORY,       \
    PropertyFactory,        \
    DATE_FORMAT,            \
    TIME_FORMAT,            \
    STRING_PROPERTY_TAG,    \
    MARKDOWN_PROPERTY_TAG,  \
    DATE_PROPERTY_TAG,      \
    DEFAULT_CATEGORY

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

# --------------------------------------------------------------------------
# String & markdown property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('property_tag', [STRING_PROPERTY_TAG, MARKDOWN_PROPERTY_TAG])
@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value',        [str(), 'test value', 'test <>& value' ])
@pytest.mark.parametrize('new_value',    [str(), 'new test value', 'new test <>& value'])

def test_string_and_markdown_properties(property_tag, name, value, category, new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of string and markdown properties.
    """
    property_element = ET.Element(property_tag)

    if name:
        property_element.set(NAME_TAG, name)
    else:
        name = DEFAULT_NAME
        
    if category:
        property_element.set(CATEGORY_TAG, category)
    else:
        category = DEFAULT_CATEGORY

    property_element.text = str(value)

    property = PropertyFactory.create(property_element)

    assert(property.name == name)
    assert(property.value == value)
    assert(property.category == category)
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}"><![CDATA[{value}]]></{property_tag}>'
    )

    evolved_property = copy.copy(property)
    evolved_property.value = str(new_value)

    assert(evolved_property.name == name)
    assert(evolved_property.value == new_value)
    assert(evolved_property.category == category)
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}"><![CDATA[{new_value}]]></{property_tag}>'
    )

# --------------------------------------------------------------------------
# Date property tests
# --------------------------------------------------------------------------

today : str = datetime.date.today().strftime(DATE_FORMAT)

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, expected_value', 
    [
        (str(), today), 
        ('2022-01-01','2022-01-01'),
        ('2022-99-99', today),
        ('not a date', today)
    ]
)
@pytest.mark.parametrize('new_value, expected_new_value',
    [
        (str(), today), 
        ('2022-01-01','2022-01-01'),
        ('2022-99-99', today),
        ('not a date', today)
    ]
)

def test_date_properties(name, value, expected_value, category, new_value, expected_new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of date properties.
    """
    property_tag = DATE_PROPERTY_TAG
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

    property = PropertyFactory.create(property_element)

    assert(property.name == name)
    assert(property.generate_xml_value() == expected_value)
    assert(property.category == category)
    assert(
         ET.tostring(property.generate_xml()).decode() ==
         f'<{property_tag} name="{name}" category="{category}">{expected_value}</{property_tag}>'
    )

    evolved_property = copy.copy(property)
    #evolved_property.value = str(new_value)

    # TODO: these lines should not be here
    try:
        evolved_property.value = datetime.datetime.strptime(new_value, DATE_FORMAT).date()
    except ValueError:
        evolved_property.value = datetime.date.today()

    assert(evolved_property.name == name)
    assert(evolved_property.generate_xml_value() == expected_new_value)
    assert(evolved_property.category == category)
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_new_value}</{property_tag}>'
    )

