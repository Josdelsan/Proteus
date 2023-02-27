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

import os
import pathlib
import shutil
import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import NAME_TAG, CATEGORY_TAG
from proteus.model.abstract_object import ProteusState
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.project import Project
from proteus.model.properties import Property

# --------------------------------------------------------------------------
# Project tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('path', [pathlib.Path.cwd()])

def test_projects(path):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of string and markdown properties.
    """

    # New path where we want to clone the archetype
    new_cloned_project_path = pathlib.Path.cwd().parent / "new_cloned_project"

    
    # If dir already exists, then we remove it
    if(new_cloned_project_path.resolve().exists()):
        shutil.rmtree(new_cloned_project_path)

    # Create a dir
    os.mkdir(new_cloned_project_path)

    # Clone project
    ArchetypeManager.clone_project(os.path.join(path, "proteus.xml"),new_cloned_project_path.resolve())

    # Load the project
    test_project = Project.load(new_cloned_project_path)

    # Iterate over properties
    property : Property
    name : str
    for name, property in test_project.properties.items():
        assert (test_project.get_property(name) == property)
        assert (name == property.name)

    # Iterate over documents
    for id, document in test_project.documents.items():
        assert(document.id == id)

    # Compare xml
    
    # Parser to avoid conflicts with CDATA
    parser = ET.XMLParser(strip_cdata=False)
    proteusET = ET.parse(new_cloned_project_path / "proteus.xml", parser = parser)
    
    generated_xml = (ET.tostring(test_project.generate_xml(),
                    xml_declaration=True,
                    encoding='utf-8',
                    pretty_print=True).decode())

    xml = (ET.tostring(proteusET,
                    xml_declaration=True,
                    encoding='utf-8',
                    pretty_print=True).decode())
    
    assert(generated_xml == xml)

    # Compare Path
    assert pathlib.Path(test_project.path).resolve() == (new_cloned_project_path / "proteus.xml")
    
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

    # Get the number of children before setting to DEAD
    number_of_children = len(os.listdir(new_cloned_project_path / "objects"))
    
    # Set all children to DEAD 
    for doc in test_project.documents.values():
        number_of_children -= 1
        assert(doc.parent == test_project)

        # If the document has children we also substract 1 per each and ask if it has children.
        # This is because we are setting to Dead all the documents, then their children are going
        # to be removed as well
        def children_from_docs(doc, number_of_children):
            for child in doc.children.values():
                number_of_children -= 1
                assert(child.parent == doc)
                if (child.children):
                    children_from_docs(child, number_of_children)
            return (number_of_children)
        doc.state = ProteusState.DEAD
        if(doc.children):
            number_of_children = children_from_docs(doc, number_of_children)
    
    # We save the project and check that the property we set before is saved.
    test_project.save_project()
    test_project2 = Project.load(new_cloned_project_path)
    assert (test_project2.get_property("name").value == "new name")

    # Check that the number of children is the one that we calculate
    assert(len(os.listdir(new_cloned_project_path / "objects")) == number_of_children)

    # Check that the state before saving is Clean
    assert(test_project.state == ProteusState.CLEAN)

    # Check that the project hasn't any document
    assert(len(test_project.documents) == 0)