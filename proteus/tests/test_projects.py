# ==========================================================================
# File: test_projects.py
# Description: pytest file for PROTEUS projects
# Date: 15/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
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
from proteus.config import Config

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import NAME_TAG, CATEGORY_TAG
from proteus.model.abstract_object import ProteusState
from proteus.model.project import Project

from proteus.model.property import Property, StringProperty

# --------------------------------------------------------------------------
# Project tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('path', [pathlib.Path.cwd()])

def test_projects(path):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of string and markdown properties.
    """

    # Load project
    test_project : Project = Project.load(path)

    # Generate xml to compare
    generate_xml :str = "<?xml version='1.0' encoding='utf-8'?>\n"
    generate_xml += f'<project id="{test_project.id}">\n'
    generate_xml += f'  <properties>\n'

    # Iterate over properties
    property : Property
    name : str
    for name, property in test_project.properties.items():
        assert (test_project.get_property(name) == property)
        generate_xml += f"    {ET.tostring(property.generate_xml(), encoding='utf-8',pretty_print=True).decode()}"
        assert (name == property.name)
    generate_xml += f'  </properties>\n  <documents>\n'

    # Iterate over documents
    for id, document in test_project.documents.items():
        assert(document.id == id)
        generate_xml += f'    <document id="{id}"/>\n'
    generate_xml += f'  </documents>\n</project>\n'

    # Compare xml
    assert ((ET.tostring(test_project.generate_xml(),
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True).decode()) == generate_xml)

    # Compare Path
    assert pathlib.Path(test_project.path).resolve() == (path / "proteus.xml")
    
    # Test ProteusState
    assert (test_project.state == ProteusState.CLEAN)
    test_project.state = ProteusState.DEAD
    assert (test_project.state == ProteusState.DEAD)
    test_project.state = ProteusState.DIRTY
    assert (test_project.state == ProteusState.DIRTY)
    test_project.state = ProteusState.FRESH
    assert (test_project.state == ProteusState.FRESH)
    test_project.state = ProteusState.CLEAN

    # Test set_property
    new_prop = test_project.get_property("name").clone("new name")
    test_project.set_property(new_prop)
    assert (test_project.get_property("name").value == "new name")
    