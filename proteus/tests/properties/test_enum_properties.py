# ==========================================================================
# File: test_enum_properties.py
# Description: pytest file for PROTEUS enum properties
# Date: 22/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# ==========================================================================
# Update: 22/10/2022 (Amador)
# Description:
# - Common code extracted as fixtures.
# - Tests updated. Choices cannot be changed in clone(), only value.
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

from proteus.model.properties import ENUM_PROPERTY_TAG

# --------------------------------------------------------------------------
# Test specific imports
# --------------------------------------------------------------------------

import proteus.tests.fixtures as fixtures

# --------------------------------------------------------------------------
# Enum property tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('name',         [str(), 'test name'     ])
@pytest.mark.parametrize('category',     [str(), 'test category' ])
@pytest.mark.parametrize('value, choices, expected_value, expected_choices',
    [
        ('high',    'low medium high', 'high', 'low medium high'),
        ('not low', 'low medium high', 'low',  'low medium high'),
        (str(),     'low medium high', 'low',  'low medium high'),
        (1,         'low medium high', 'low',  'low medium high'),
        ('high',    str(),             'high', 'high'           ),
        (str(),     str(),             str(),  str()            )
    ]
)
@pytest.mark.parametrize('new_value', [str(), 'medium', 'bad value', 10])

def test_enum_properties(name, category, value, choices, expected_value, expected_choices, new_value):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of enum properties.
    """
    # Create property from XML element
    property_tag = ENUM_PROPERTY_TAG
    (property, name, category) = fixtures.create_property(property_tag, name, category, value, choices)

    # Check property
    assert(property.name     == name            )
    assert(property.category == category        )
    assert(property.value    == expected_value  )
    assert(property.choices  == expected_choices)
    if property.value:
        assert(property.value in property.get_choices_as_set())
    assert(
        ET.tostring(property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}" choices="{expected_choices}">{expected_value}</{property_tag}>'
    )

    # Clone the property without changes
    cloned_property = property.clone()

    # Check cloned property
    assert(cloned_property.name     == property.name    )
    assert(cloned_property.category == property.category)
    assert(cloned_property.value    == property.value   )
    assert(cloned_property.choices  == property.choices )

    # Clone the property changing value
    evolved_property = property.clone(new_value)

    # Compute new expected values (too complex to use @pytest.mark.parametrize)
    # no value, no choices in original property
    new_value = str(new_value).replace(' ', '_') if new_value else str(new_value)

    if not new_value and not property.choices:
        expected_value = str()
        expected_choices = str()
    # no value, choices
    elif not new_value:
        expected_value = property.choices.split()[0]
        expected_choices = property.choices
    # value, no choices in original property
    elif not property.choices:
        expected_value = new_value
        expected_choices = new_value
    # value, choices, value not in choices in original property
    elif new_value not in property.get_choices_as_set():
        expected_value = property.choices.split()[0]
        expected_choices = property.choices
    # value, choices, value in choices        
    else:
        expected_value = new_value
        expected_choices = property.choices

    # Check cloned property
    assert(evolved_property.name     == name            )
    assert(evolved_property.category == category        )
    assert(evolved_property.value    == expected_value  )    
    assert(evolved_property.choices  == expected_choices)
    if evolved_property.value:
        assert(evolved_property.value in evolved_property.get_choices_as_set())
    assert(
        ET.tostring(evolved_property.generate_xml()).decode() ==
        f'<{property_tag} name="{name}" category="{category}" choices="{expected_choices}">{expected_value}</{property_tag}>'
    )
