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
from proteus.model.object import Object
from proteus.model.project import Project

from proteus.model.property import Property, StringProperty

# --------------------------------------------------------------------------
# Project tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('path', [pathlib.Path.cwd()])

def test_objects(path):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of string and markdown properties.
    """

    # Load project
    test_project : Project = Project.load(path)
    test_object : Object = Object.load(test_project, "3fKhMAkcEe2C")
    
    # Parser to avoid conflicts with CDATA
    parser = ET.XMLParser(strip_cdata=False)
    element = ET.parse( test_object.path, parser = parser)
    root = element.getroot()

    # Compare ET elements with Object elements
    assert(root.attrib["id"] == test_object.id)
    assert(root.attrib["acceptedChildren"] == test_object.acceptedChildren)
    assert(root.attrib["classes"] == test_object.classes)

    children = root.find("children")
    children_list : list = []
    for child in children:
        children_list.append(child.attrib["id"] )

    # Check that Object contains all the children of the xml    
    assert(all(child in test_object.children.keys()  for child in children_list))

    assert (test_project.state == ProteusState.CLEAN)
    test_project.state = ProteusState.DEAD
    assert (test_project.state == ProteusState.DEAD)
    test_project.state = ProteusState.DIRTY
    assert (test_project.state == ProteusState.DIRTY)
    test_project.state = ProteusState.FRESH
    assert (test_project.state == ProteusState.FRESH)
    test_project.state = ProteusState.CLEAN
    
    xml = (ET.tostring(element,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True).decode())

    gemerated_xml = (ET.tostring(test_object.generate_xml(),
                     xml_declaration=True,
                     encoding='utf-8',
                     pretty_print=True).decode())


    assert(xml == gemerated_xml)