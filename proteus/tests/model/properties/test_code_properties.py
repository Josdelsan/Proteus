# ==========================================================================
# File: test_code_properties.py
# Description: pytest file for PROTEUS code properties
# Date: 16/11/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
# NOTE: code property logic is heavily acopled to ProteusCode class. This
#       should be fixed in the future so it can be tested independently.

import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import NAME_ATTRIBUTE, CATEGORY_ATTRIBUTE
from proteus.model.properties import CODE_PROPERTY_TAG, PREFIX_TAG, NUMBER_TAG, SUFFIX_TAG
from proteus.model.properties.code_property import ProteusCode, CodeProperty
from proteus.model.properties.property_factory import PropertyFactory

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------



# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------
DUMMY_PREFIX = "prefix"
DUMMY_NUMBER = "0001"
DUMMY_SUFFIX = "suffix"
DUMMY_NAME = "test name"
DUMMY_CATEGORY = "test category"
DUMMY_INMUTABLE = "False"

@pytest.fixture
def code():
    """
    Simple ProteusCode object fixture.
    """
    return ProteusCode(DUMMY_PREFIX, DUMMY_NUMBER, DUMMY_SUFFIX)

@pytest.fixture
def code_property_element() -> ET.Element:
    """
    Simple code property XML element fixture.
    """
    code_element = ET.Element(CODE_PROPERTY_TAG)
    # Add attributes
    code_element.set(NAME_ATTRIBUTE, DUMMY_NAME)
    code_element.set(CATEGORY_ATTRIBUTE, DUMMY_CATEGORY)
    # Add subelements
    prefix_element = ET.SubElement(code_element, PREFIX_TAG)
    prefix_element.text = ET.CDATA(DUMMY_PREFIX)
    number_element = ET.SubElement(code_element, NUMBER_TAG)
    number_element.text = DUMMY_NUMBER
    suffix_element = ET.SubElement(code_element, SUFFIX_TAG)
    suffix_element.text = ET.CDATA(DUMMY_SUFFIX)
    return code_element

@pytest.fixture
def code_property(code_property_element: ET.Element):
    """
    Simple code property fixture.
    """
    return PropertyFactory.create(code_property_element)


# --------------------------------------------------------------------------
# Code property tests
# --------------------------------------------------------------------------
def test_create_property(code_property_element: ET.Element):
    """
    Test code property creation using factory method.
    """
    # Act -----------------------------
    # Create property from XML element
    property: CodeProperty = PropertyFactory.create(code_property_element)

    # Assert --------------------------
    # Check property type
    assert isinstance(property.value, ProteusCode)

    # Check property attributes
    assert property.value.prefix == DUMMY_PREFIX
    assert property.value.number == DUMMY_NUMBER
    assert property.value.suffix == DUMMY_SUFFIX

def test_clone_property(code_property: CodeProperty, code: ProteusCode):
    """
    Test code property cloning.
    """
    # Act -----------------------------
    # Clone the property without changes
    cloned_property: CodeProperty = code_property.clone(code)

    # Assert --------------------------
    # Check ProteusCode objects ids are different after cloning
    assert id(cloned_property.value) != id(code_property.value), \
        f"Cloned ProteusCode object id ({id(cloned_property.value)}) is the same as the original ({id(code_property.value)}), but it should be different"
    
    # Check the value was updated successfully
    assert cloned_property.value == code, \
        f"Cloned property value ({cloned_property.value}) is not the same as the new value ({code}), but it should be"
    assert id(cloned_property.value) == id(code), \
        f"Cloned ProteusCode object id ({id(cloned_property.value)}) is not the same as the new value id ({id(code)}), but it should be"
    
    
def test_generate_xml(code_property: CodeProperty, code_property_element: ET.Element):
    """
    Test code property XML value generation.
    """
    # Act -----------------------------
    # Generate XML value (property method + subclass method)
    xml_value = code_property.generate_xml()

    # Assert --------------------------
    # Check XML generation
    assert ET.tostring(xml_value).decode() == ET.tostring(code_property_element).decode(), \
        f"XML value ({ET.tostring(xml_value).decode()}) is not the same as the expected value ({ET.tostring(code_property_element).decode()}), but it should be"

    

