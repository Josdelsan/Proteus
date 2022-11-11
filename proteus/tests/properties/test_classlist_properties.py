# ==========================================================================
# File: test_classlist_properties.py
# Description: pytest file for PROTEUS clas list properties
# Date: 22/10/2022
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

from proteus.model.property import CLASS_TAG, CLASSLIST_PROPERTY_TAG

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------

import proteus.tests.properties.fixtures as fixtures

# --------------------------------------------------------------------------
# Class list property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, expected_value, expected_value_as_list',
    [
        (str(),     str(),     []                  ),
        ('A',       'A',       ['A']               ), 
        ('A B C D', 'A B C D', ['A', 'B', 'C', 'D'])
    ]
)
@pytest.mark.parametrize('new_value, new_expected_value, new_expected_value_as_list',
    [
        ('X Y Z', 'X Y Z', ['X', 'Y', 'Z']),
        ('B',     'B',     ['B']          ),
        (str(),   str(),   []             )
    ]
)

def test_classlist_properties(name, category, value, expected_value, expected_value_as_list, new_value, new_expected_value, new_expected_value_as_list):
    """
    It tests creation, cloning, and evolution (cloning with a new value) 
    of classlist properties.
    """
    # Create property from XML element
    property_tag = CLASSLIST_PROPERTY_TAG
    # <class>
    child_property_tag = CLASS_TAG
    (property, name, category) = fixtures.create_property(property_tag, name, category, value)

    # Check property
    assert(property.name     == name                          )
    assert(property.category == category                      )
    assert(property.value    == expected_value                )
    assert(property.get_class_list() == expected_value_as_list)
    
    #We get the values parsed as <class>value</class><class>value</class>...
    expected_values_parsed = ""
    for class_value in expected_value_as_list:
        expected_values_parsed += "<" + child_property_tag + ">" + class_value + "</" + child_property_tag + ">"
    
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{expected_values_parsed}</{property_tag}>'
    )

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name     == property.name    )
    assert(cloned_property.category == property.category)
    assert(cloned_property.value    == property.value   )
    assert(cloned_property.get_class_list() == property.get_class_list() )

    # Clone the property changing value
    evolved_property = property.clone(new_value)

    # Check cloned property
    assert(evolved_property.name     == property.name     )
    assert(evolved_property.category == property.category )
    assert(evolved_property.value    == new_expected_value  )    
    assert(evolved_property.get_class_list() == new_expected_value_as_list)

    #We get the values parsed as <class>value</class><class>value</class>...
    new_expected_values_parsed = ""
    for class_value in new_expected_value_as_list:
        new_expected_values_parsed += "<" + child_property_tag + ">" + class_value + "</" + child_property_tag + ">"

    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}">{new_expected_values_parsed}</{property_tag}>'
    )
