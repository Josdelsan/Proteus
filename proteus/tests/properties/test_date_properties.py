# ==========================================================================
# File: test_date_properties.py
# Description: pytest file for PROTEUS date properties
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

import datetime

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.property import DATE_PROPERTY_TAG, DATE_FORMAT

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------

import proteus.tests.properties.fixtures as fixtures

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
    # Create property from XML element
    property_tag = DATE_PROPERTY_TAG
    (property, name, category) = fixtures.create_property(property_tag, name, category, value)

    # Check property
    assert(property.name == name)
    assert(property.category == category)    
    assert(property.value == datetime.datetime.strptime(expected_value, DATE_FORMAT).date())
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_value}</{property_tag}>'
    )

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name == property.name)
    assert(cloned_property.category == property.category)
    assert(cloned_property.value == property.value)
    
    # Clone the property changing value
    evolved_property = property.clone(str(new_value))

    # Check cloned property
    assert(evolved_property.name == name)
    assert(evolved_property.category == category)    
    assert(evolved_property.value == datetime.datetime.strptime(expected_new_value, DATE_FORMAT).date())
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_new_value}</{property_tag}>'
    )
