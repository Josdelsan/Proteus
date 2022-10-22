# ==========================================================================
# File: property_fixtures.py
# Description: pytest fixtures for testing PROTEUS properties
# Date: 22/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================
# About pytest fixtures: 
# https://docs.pytest.org/en/7.1.x/explanation/fixtures.html#about-fixtures
#
# Pytest fixtures are called automatically from function tests. For the 
# moment, the "fixtures" in this module are not actually pytest fixtures but 
# repeated code extracted as functions.
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
    Property,                      \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    CHOICES_TAG,                   \
    PropertyFactory

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

def create_property(property_tag, name, category, value, choices = None) -> tuple([Property,str,str]):
    """
    It creates a PROTEUS property using the tag, name, category and value
    passed as arguments. It returns a tuple containing the new property, 
    the name, and the category values, which are set to default in case
    they were not set.
    """
    # Create XML element for property
    property_element = ET.Element(property_tag)

    # Process name
    if name:
        property_element.set(NAME_TAG, name)
    else:
        name = DEFAULT_NAME

    # Process category
    if category:
        property_element.set(CATEGORY_TAG, category)
    else:
        category = DEFAULT_CATEGORY

    # Set value as a string
    property_element.text = str(value)

    # Set choices if needed (EnumProperty only)
    if choices is not None:
        property_element.set(CHOICES_TAG, choices)
  
    # Create property from XML element
    property = PropertyFactory.create(property_element)

    # return tuple(property,name,category)
    return (property, name, category)
