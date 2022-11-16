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

import copy
import os
import pathlib
import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.model.project import Project

# --------------------------------------------------------------------------
# Object tests
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

    # Check that all their children the proper parent
    def check_parent(object: Object):
        for child in object.children.values():
            assert(child.parent == object)
            check_parent(child)
    
    check_parent(test_object)

    # Check if states changes properly
    assert (test_object.state == ProteusState.CLEAN)
    test_object.state = ProteusState.DEAD
    assert (test_object.state == ProteusState.DEAD)
    test_object.state = ProteusState.DIRTY
    assert (test_object.state == ProteusState.DIRTY)
    test_object.state = ProteusState.FRESH
    assert (test_object.state == ProteusState.FRESH)
    test_object.state = ProteusState.CLEAN
    
    # Check if generate xml, generates properly the xml
    xml = (ET.tostring(element,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True).decode())

    gemerated_xml = (ET.tostring(test_object.generate_xml(),
                     xml_declaration=True,
                     encoding='utf-8',
                     pretty_print=True).decode())

    assert(xml == gemerated_xml)

    # We have to copy the value otherwise it changes automatically when clone
    children_before_clone = copy.deepcopy(test_project.documents)

    test_object.clone_object(test_project)
    
    children_after_clone = test_project.documents

    # Check if clone_object clones properly
    assert(len(test_project.documents) > len(children_before_clone))

    new_object_id = list(set(children_after_clone) - set(children_before_clone))

    new_object = test_project.documents[new_object_id[0]]

    # Check if the new object is a clone of the original one (We can't compare the XML because they are different
    # because of the id, as well as the children id's are different)
    assert(new_object.properties == test_object.properties)
    assert (new_object.acceptedChildren == test_object.acceptedChildren)
    assert (new_object.classes == test_object.classes)
    assert (len(new_object.children) == len(test_object.children))

