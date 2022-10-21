# ==========================================================================
# File: test_time_properties.py
# Description: pytest file for PROTEUS time properties
# Date: 21/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# ==========================================================================
# Update: 21/10/2022 (Amador)
# Description:
# - Code review.
# - Use of datetime substraction to count difference in seconds.
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

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, expected_value', 
    [
        ('20:10:02', '20:10:02'),
        (str(),        datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('26:10:02',   datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:61:02',   datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:10:99',   datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('not a time', datetime.datetime.now().time().strftime(TIME_FORMAT))
    ]
)
@pytest.mark.parametrize('new_value, expected_new_value',
    [
        ('20:10:02', '20:10:02'),
        (str(),        datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('26:10:02',   datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:61:02',   datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('20:10:99',   datetime.datetime.now().time().strftime(TIME_FORMAT)),
        ('not a time', datetime.datetime.now().time().strftime(TIME_FORMAT))
    ]
)

def test_time_properties(name, category, value, expected_value, new_value, expected_new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of time properties.
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

    # Create a time from the expected_value string
    # This could be avoided passing times as expected value
    expected_value_as_time = datetime.datetime.strptime(expected_value, TIME_FORMAT).time()

    # Maximum number of seconds between test function call and creation of property
    epsilon_seconds = 10

    # To calculate the difference between two times, they have to be converted into datetime
    # https://stackoverflow.com/questions/43305577/python-calculate-the-difference-between-two-datetime-time-objects
    delta = \
        datetime.datetime.combine(datetime.date.today(), property.value) - \
        datetime.datetime.combine(datetime.date.today(), expected_value_as_time)        
    
    # Check property
    assert(property.name == name)
    assert(property.category == category)    
    assert(delta.total_seconds() < epsilon_seconds)

    # To avoid fail because of potentional difference in seconds, we just check
    # that the property value is correctly generated in XML.
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{property.value.strftime(TIME_FORMAT)}</{property_tag}>'
    )

    # Clone the property without changes
    # Suprinsingly, clone() produces small differences in miliseconds
    cloned_property = property.clone()

    # To calculate the difference between two times, they have to be converted into datetime
    delta = \
        datetime.datetime.combine(datetime.date.today(), property.value) - \
        datetime.datetime.combine(datetime.date.today(), cloned_property.value)

    # Check cloned property
    assert(cloned_property.name == property.name)
    assert(cloned_property.category == property.category)
    assert(delta.total_seconds() < epsilon_seconds)    

    # Clone the property changing value
    evolved_property = property.clone(str(new_value))

    # Create a time from the expected_new_value string    
    expected_new_value_as_time = datetime.datetime.strptime(expected_new_value, TIME_FORMAT).time()

    # To calculate the difference between two times, they have to be converted into datetime
    delta = \
        datetime.datetime.combine(datetime.date.today(), evolved_property.value) - \
        datetime.datetime.combine(datetime.date.today(), expected_new_value_as_time)        

    # Check cloned property
    assert(evolved_property.name == name)
    assert(evolved_property.category == category)
    assert(delta.total_seconds() < epsilon_seconds)  

    # To avoid fail because of potentional difference in seconds, we just check
    # that the property value is correctly generated in XML.
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{evolved_property.value.strftime(TIME_FORMAT)}</{property_tag}>'
    )

