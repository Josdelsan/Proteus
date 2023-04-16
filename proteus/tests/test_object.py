# ==========================================================================
# File: test_object.py
# Description: pytest file for PROTEUS object class
# Date: 15/10/2022
# Version: 0.2
# Author: José María Delgado Sánchez
#         Pablo Rivera Jiménez
# ==========================================================================
# Update: 12/04/2023 (José María)
# Description:
# - Created tests for different Object methods and lazy load of children.
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import copy
import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties import STRING_PROPERTY_TAG
from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.model.archetype_manager import ArchetypeManager
from proteus.tests import PROTEUS_TEST_SAMPLE_DATA_PATH
from proteus.tests import fixtures

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

# NOTE: This is a sample project that is used for testing purposes. The
#       sample object id was selected from this project.
SAMPLE_PROJECT_PATH = PROTEUS_TEST_SAMPLE_DATA_PATH / "example_project"
SAMPLE_OBJECT_ID = "3fKhMAkcEe2C"

# --------------------------------------------------------------------------
# Fixtures and helpers
# --------------------------------------------------------------------------

@pytest.fixture
def sample_project() -> Project:
    """
    Fixture that returns a PROTEUS sample project.
    """
    return Project.load(SAMPLE_PROJECT_PATH)

@pytest.fixture
def sample_object(sample_project) -> Object:
    """
    Fixture that returns a PROTEUS sample object.
    """
    return Object.load(SAMPLE_OBJECT_ID, sample_project)

# TODO: For rich tests we need sample archetype objects. This is a temporary
#       based on the current archetype repository content (16/04/2023)
#       solution. Sample archetype objects should have children to test
#       lazy loading and loading of children completely.
@pytest.fixture
def sample_archetype_object() -> Object:
    """
    Fixture that returns a PROTEUS sample archetype object.
    """
    archetype_list : list[Object] = ArchetypeManager.load_document_archetypes()
    return archetype_list[1]

# --------------------------------------------------------------------------
# Object tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('path',
    [
        SAMPLE_PROJECT_PATH
    ]
)

def test_objects(path):
    """
    It tests creation, update, and evolution (cloning with a new value) 
    of string and markdown properties.
    """

    # Load project
    test_project : Project = Project.load(path)
    test_object : Object = Object.load("3fKhMAkcEe2C", test_project)
    
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

# --------------------------------------------------------------------------
# Object unit tests
# NOTE: Some methods are not testes with Archetype Objects because they
# are not meant to be used with them.
# --------------------------------------------------------------------------

def test_init():
    """
    Test Object initialization method
    """
    # Setup test object
    object_file_path = SAMPLE_PROJECT_PATH / "objects" / f"{SAMPLE_OBJECT_ID}.xml"
    test_object : Object = Object(object_file_path)

    # Check type of the object
    assert(isinstance(test_object, Object)), \
        f"Object is not an instance of Object. It is {type(test_object)}"

    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(test_object.path)

    # Compare ET elements with Object elements
    assert(root.attrib["id"] == test_object.id), \
        f"Object id is not the same as the root element id."
    assert(root.attrib["acceptedChildren"] == test_object.acceptedChildren), \
        f"Object acceptedChildren is not the same as the root element acceptedChildren."
    assert(root.attrib["classes"] == test_object.classes), \
        f"Object classes is not the same as the root element classes."

def test_load(sample_project: Project):
    """
    Test Object load method
    """
    # Setup test object
    test_object : Object = Object.load(SAMPLE_OBJECT_ID, sample_project)

    # Check type of the object
    assert(isinstance(test_object, Object)), \
        f"Object is not an instance of Object. It is {type(test_object)}"

    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(test_object.path)

    # Compare ET elements with Object elements
    assert(root.attrib["id"] == test_object.id), \
        f"Object id is not the same as the root element id."
    assert(root.attrib["acceptedChildren"] == test_object.acceptedChildren), \
        f"Object acceptedChildren is not the same as the root element acceptedChildren."
    assert(root.attrib["classes"] == test_object.classes), \
        f"Object classes is not the same as the root element classes."

@pytest.mark.parametrize(
        "sample_object_fixture",
        ["sample_object", "sample_archetype_object"],
)
def test_children_lazy_load(sample_object_fixture: str, request):
    """
    Test Object children property lazy loading
    """
    # Get sample object from fixture
    # NOTE: using parameterized fixtures to get the sample project
    # https://engineeringfordatascience.com/posts/pytest_fixtures_with_parameterize/
    sample_object = request.getfixturevalue(sample_object_fixture)

    # Check that children are not loaded yet checking private
    # variable _children
    assert(sample_object._children == None), \
        "Children should not be loaded if the 'children' property is not accessed"

    # Check that children are loaded when accessing children
    # property for the first time
    assert(type(sample_object.children) == dict),                     \
        f"Children should have been loaded when accessing 'children'  \
        property but they are of type {type(sample_object.children)}"
    assert(type(sample_object._children) == dict),                    \
        f"Children private var should have been loaded when accessing \
        'Children' property but they are of type {type(sample_project._documents)}"

@pytest.mark.parametrize(
        "sample_object_fixture",
        ["sample_object", "sample_archetype_object"],
)
def test_load_children(sample_object_fixture: str, request):
    """
    Test Object load_children method
    """
    # Get sample object from fixture
    # NOTE: using parameterized fixtures to get the sample project
    # https://engineeringfordatascience.com/posts/pytest_fixtures_with_parameterize/
    sample_object = request.getfixturevalue(sample_object_fixture)

    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(sample_object.path)

    # Get children of the xml file and store them in a list
    children = root.find("children")
    children_list : list = []
    for child in children:
        children_list.append(child.attrib["id"] )

    # Call method to load children
    # NOTE: This method could be called when accessing children
    # for the first time and no children are loaded yet. However,
    # we are calling it explicitly to test it in case lazy loading
    # fails.
    sample_object.load_children()

    # Check that Object contains all the children of the xml    
    assert(all(child in sample_object.children.keys() for child in children_list)), \
        f"Object does not contain all the children of the xml file.                 \
        Children in xml file: {children_list}                                       \
        Children in object: {sample_object.children.keys()}"
    
def test_generate_xml(sample_object: Object):
    """
    Test Object generate_xml method
    """
    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(sample_object.path)

    # Get xml string from xml file
    expected_xml= (ET.tostring(root,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True).decode())

    # Generate xml
    xml : ET.Element = sample_object.generate_xml()

    # Get xml string from Object
    actual_xml= (ET.tostring(xml,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True).decode())

    # Compare xml strings
    assert(expected_xml == actual_xml)

# TODO: Test clone_object method

def test_set_property(sample_object: Object):
    """
    Test Abstract Object set_property method
    """
    # Create property
    (new_property, name, _) = fixtures.create_property(STRING_PROPERTY_TAG, "name", "general", "Test value")

    # Set property
    sample_object.set_property(new_property)

    # Check that property was set
    assert(sample_object.get_property(name) == new_property),  \
        f"Property was not set. Expected value: {new_property} \
        Actual value: {sample_object.get_property(name)}"
    
