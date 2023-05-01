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
SAMPLE_OBJECT_ID = "64xM8FLyxtaE"
SAMPLE_DOCUMENT_ID = "3fKhMAkcEe2C"

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

@pytest.fixture
def sample_document(sample_project) -> Object:
    """
    Fixture that returns a PROTEUS sample document.
    """
    return Object.load(SAMPLE_DOCUMENT_ID, sample_project)

# TODO: For rich tests we need sample archetype objects. This is a temporary
#       based on the current archetype repository content (16/04/2023)
#       solution. Sample archetype objects should have children to test
#       lazy loading and loading of children completely.
@pytest.fixture
def sample_archetype_document() -> Object:
    """
    Fixture that returns a PROTEUS sample archetype document object.
    """
    archetype_list : list[Object] = ArchetypeManager.load_document_archetypes()
    return archetype_list[1]

# --------------------------------------------------------------------------
# Object unit tests
# NOTE: Some methods are not tested with Archetype Objects because they
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
        ["sample_object", "sample_archetype_document"],
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
        ["sample_object", "sample_archetype_document"],
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

# TODO: Test clone object -> object
#                  arch_object -> object
@pytest.mark.parametrize(
        "sample_object_to_clone_fixture, sample_parent_fixture",
        [
            ("sample_object", "sample_document"),
            ("sample_document", "sample_project"),
            ("sample_archetype_document", "sample_project")
        ],
)
def test_clone_object(sample_object_to_clone_fixture: str, sample_parent_fixture: str, sample_project: Project, request):
    """
    Test Object clone_object method
    """
    sample_object_to_clone = request.getfixturevalue(sample_object_to_clone_fixture)
    sample_parent = request.getfixturevalue(sample_parent_fixture)

    # Clone object
    new_object = sample_object_to_clone.clone_object(sample_parent, sample_project)

    # Check that object was cloned
    assert isinstance(new_object, Object), \
        f"Object was not cloned. It is of type {type(new_object)}"
    
    # Check that object is in fresh state
    assert new_object.state == ProteusState.FRESH, \
        f"Object state is not {ProteusState.FRESH} but {new_object.state}"
    
    # Check the object is in the parent children
    # TODO: Should this be in a separate test?
    match sample_parent.__class__.__name__:
            case "Object":
                assert new_object.id in sample_parent.children.keys(), \
                    f"Object {new_object.id} was not found in {sample_parent.children.keys()}"
            case "Project":
                assert new_object.id in sample_parent.documents.keys(), \
                    f"Object {new_object.id} was not found in {sample_parent.documents.keys()}"

    
    # Check the children are in the new object
    # NOTE: This will not work if we clone an object into itself
    # however, this is not a valid use case at the moment
    assert sample_object_to_clone.children.__len__() == new_object.children.__len__(), \
        f"Object {new_object.id} does not have the same number of children as \
        the original object {sample_object_to_clone.id}"

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

def test_delete(sample_document: Object):
    """
    Test Object delete method
    """
    sample_document.delete()

    # Check that object was marked as DEAD
    assert(sample_document.state == ProteusState.DEAD), \
        f"Object was not marked as DEAD. State: {sample_document.state}"
    
    # Check object children were marked as DEAD
    for child in sample_document.children.values():
        assert(child.state == ProteusState.DEAD), \
            f"Object child was not marked as DEAD. State: {child.state}"

# NOTE save method is tested with the save_project method in test_project.py
