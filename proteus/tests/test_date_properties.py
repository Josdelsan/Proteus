# ==========================================================================
# File: test_date_properties.py
# Description: pytest file for PROTEUS date properties
# Date: 15/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import datetime

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
    DATE_PROPERTY_TAG,             \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    DATE_FORMAT,                   \
    PropertyFactory

# --------------------------------------------------------------------------
# Date property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, expected_value', 
    [
        ('2022-01-01', '2022-01-01'),
        (str(),        datetime.date.today().strftime(DATE_FORMAT)),
        ('2022-99-99', datetime.date.today().strftime(DATE_FORMAT)),
        ('not a date', datetime.date.today().strftime(DATE_FORMAT))
    ]
)
@pytest.mark.parametrize('new_value, expected_new_value',
    [
        ('2022-12-31', '2022-12-31'),
        (str(),        datetime.date.today().strftime(DATE_FORMAT)),
        ('2022-99-99', datetime.date.today().strftime(DATE_FORMAT)),
        ('not a date', datetime.date.today().strftime(DATE_FORMAT))
    ]
)

def test_date_properties(name, category, value, expected_value, new_value, expected_new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of date properties.
    """
    # Prepare XML element
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

    # Create property from XML element
    property = PropertyFactory.create(property_element)

    # Check property
    assert(property.name == name)
    assert(property.value == datetime.datetime.strptime(expected_value, DATE_FORMAT).date())
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
    evolved_property = property.clone(str(new_value))

    # Check cloned property
    assert(evolved_property.name == name)
    assert(evolved_property.value == datetime.datetime.strptime(expected_new_value, DATE_FORMAT).date())
    assert(evolved_property.category == category)
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_new_value}</{property_tag}>'
    )
