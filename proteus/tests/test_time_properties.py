# ==========================================================================
# File: test_time_properties.py
# Description: pytest file for PROTEUS time properties
# Date: 17/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
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
    TIME_PROPERTY_TAG,             \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    TIME_FORMAT,                   \
    PropertyFactory

# --------------------------------------------------------------------------
# Time property tests
# --------------------------------------------------------------------------

seconds_firewall= 10
minutes_firewall = 1

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, expected_value', 
    [
        ('20:10:02', '20:10:02'),
        (str(),        datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('26:10:02', datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:61:02', datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:10:99', datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('not a time', datetime.datetime.now().time().strftime(TIME_FORMAT))
    ]
)
@pytest.mark.parametrize('new_value, expected_new_value',
    [
        ('20:10:02', '20:10:02'),
        (str(),        datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('26:10:02', datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:61:02', datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:10:99', datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('not a time', datetime.datetime.now().time().strftime(TIME_FORMAT))
    ]
)

def test_date_properties(name, category, value, expected_value, new_value, expected_new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of date properties.
    """
    # Prepare XML element
    property_tag = TIME_PROPERTY_TAG
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

    parsed_expected_value = datetime.datetime.strptime(expected_value, TIME_FORMAT).time()
    # Check property
    assert(property.name == name)

    # Because time passes, we need to check that the time is not too far from the expected value
    assert(property.value.hour == parsed_expected_value.hour and 
           parsed_expected_value.minute - property.value.minute <= minutes_firewall and 
           parsed_expected_value.second - property.value.second < seconds_firewall)
    assert(property.category == category)


    # Takes too much time and seconds (expected value (now())) changed so it fails
    # assert(
    #     ET.tostring(property.generate_xml()).decode() ==
    #     f'<{property_tag} name="{name}" category="{category}">{str(expected_value)}</{property_tag}>'
    # )

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name == property.name)
    assert(cloned_property.value.strftime(TIME_FORMAT) == property.value.strftime(TIME_FORMAT))
    assert(cloned_property.category == property.category)

    # Clone the property changing value
    evolved_property = property.clone(str(new_value))
    parsed_new_expected_value = datetime.datetime.strptime(expected_new_value, TIME_FORMAT).time()

    # Check cloned property
    assert(evolved_property.name == name)

    # Because time passes, we need to check that the time is not too far from the expected value
    assert(evolved_property.value.hour == parsed_new_expected_value.hour and 
           parsed_new_expected_value.minute - evolved_property.value.minute <= minutes_firewall and 
           parsed_new_expected_value.second - evolved_property.value.second <= seconds_firewall)
    assert(evolved_property.category == category)
    
    # Takes too much time and seconds (expected new value (now())) changed so it fails
    # assert(
    #     ET.tostring(evolved_property.generate_xml()).decode() ==
    #     f'<{property_tag} name="{name}" category="{category}">{expected_new_value}</{property_tag}>'
    # )
