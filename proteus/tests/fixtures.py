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

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import NAME_ATTR, CATEGORY_ATTR

from proteus.model.properties import \
    Property,                      \
    DEFAULT_NAME,                  \
    DEFAULT_CATEGORY,              \
    CHOICES_ATTR,                   \
    CLASS_TAG,                     \
    PropertyFactory

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

def create_property(property_tag, name, category, value, choices = None) -> tuple[Property,str,str]:
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
        property_element.set(NAME_ATTR, name)
    else:
        name = DEFAULT_NAME

    # Process category
    if category:
        property_element.set(CATEGORY_ATTR, category)
    else:
        category = DEFAULT_CATEGORY

    # Set value as a string
    property_element.text = str(value)

    # Set choices attribute if needed (EnumProperty only)
    if choices is not None:
        property_element.set(CHOICES_ATTR, choices)

    # Add <class> children if needed (ClasslistProperty only)
    for class_name in str(value).split():
        class_element = ET.SubElement(property_element, CLASS_TAG)
        class_element.text = class_name
  
    # Create property from XML element
    property = PropertyFactory.create(property_element)

    # return tuple(property,name,category)
    return (property, name, category)

def get_root(path) -> ET.Element:
    """
    Helper function that returns the root element of an xml file.
    :param path: Path to the xml file.
    :return: Root element of the xml file.
    """
    # Parser to avoid conflicts with CDATA
    parser = ET.XMLParser(strip_cdata=False)
    element = ET.parse(path, parser = parser)
    return element.getroot()