# ==========================================================================
# File: test_file_properties.py
# Description: pytest file for PROTEUS file properties
# Date: 22/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# ==========================================================================
# Update: 22/10/2022 (Amador)
# Description:
# - Tests updated after adding is_file property.
# - Common code extracted as fixtures.
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import pathlib
import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties import FILE_PROPERTY_TAG

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------

import proteus.tests.properties.fixtures as fixtures

# --------------------------------------------------------------------------
# File property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, is_file_expected',        
    [
        (__file__, True),
        (pathlib.Path.cwd(), False),
        (7.5, False),
        (str(), False)
    ]
)
@pytest.mark.parametrize('new_value, is_file_new_expected',    
    [
        (__file__, True),
        (pathlib.Path.cwd().resolve().parent, False),
        (str(), False),
        (3, False)
    ]
)

def test_file_properties(name, category, value, is_file_expected, new_value, is_file_new_expected):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of file properties.
    """  
    # Create property from XML element
    property_tag = FILE_PROPERTY_TAG
    (property, name, category) = fixtures.create_property(property_tag, name, category, value)

    # Check property
    assert(property.name     == name            )
    assert(property.category == category        )
    assert(property.value    == str(value)      )
    assert(property.is_file  == is_file_expected)
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
    assert(cloned_property.is_file  == is_file_expected )

    # Clone the property changing value
    evolved_property = property.clone(new_value)

    # Check cloned property
    assert(evolved_property.name     == name                )
    assert(evolved_property.category == category            )
    assert(evolved_property.value    == str(new_value)      )
    assert(evolved_property.is_file  == is_file_new_expected)
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}"><![CDATA[{new_value}]]></{property_tag}>'
    )
