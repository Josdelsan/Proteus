# ==========================================================================
# File: test_url_properties.py
# Description: pytest file for PROTEUS url properties
# Date: 22/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# ==========================================================================
# Update: 22/10/2022 (Amador)
# Description:
# - Common code extracted as fixtures.
# - URLs without protocol (i.e. https://) are not valid.
# - Tests updated after adding is_valid property.
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

from proteus.model.properties import URL_PROPERTY_TAG

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------

import proteus.tests.properties.fixtures as fixtures

# --------------------------------------------------------------------------
# Url property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',      [str(), 'test name'     ])
@pytest.mark.parametrize('category',  [str(), 'test category' ])
@pytest.mark.parametrize('value, is_valid_value',     
    [
        ('https://www.google.com', True),
        ('http://www.google.com', True),
        ('www.google.com', False),
        ('not an URL', False),        
        (7.5, False),
        (str(), False)
    ]
)
@pytest.mark.parametrize('new_value, is_valid_new_value', 
    [
        ('https://www.google.com', True),
        ('http://www.google.com', True),
        ('www.google.com', False),
        ('not an URL', False),        
        (7.5, False),
        (str(), False)
    ]
)

def test_url_properties(name, category, value, is_valid_value, new_value, is_valid_new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of url properties.
    """
    # Create property from XML element
    property_tag = URL_PROPERTY_TAG
    (property, name, category) = fixtures.create_property(property_tag, name, category, value)

    # Check property
    assert(property.name     == name          )
    assert(property.category == category      )
    assert(property.value    == str(value)    )
    assert(property.is_valid == is_valid_value)    
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}"><![CDATA[{value}]]></{property_tag}>'
    )

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name     == property.name    )
    assert(cloned_property.category == property.category)
    assert(cloned_property.value    == property.value   )
    assert(cloned_property.is_valid == is_valid_value   )

    # Clone the property changing value
    evolved_property = property.clone(new_value)

    # Check cloned property
    assert(evolved_property.name     == name              )
    assert(evolved_property.value    == str(new_value)    )
    assert(evolved_property.category == category          )
    assert(evolved_property.is_valid == is_valid_new_value)
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}"><![CDATA[{new_value}]]></{property_tag}>'
    )
