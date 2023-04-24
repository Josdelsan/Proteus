# ==========================================================================
# File: test_project.py
# Description: pytest file for PROTEUS project class
# Date: 15/10/2022
# Version: 0.2
# Author: José María Delgado Sánchez
#         Pablo Rivera Jiménez
# ==========================================================================
# Update: 12/04/2023 (José María)
# Description:
# - Created tests for different Project methods and lazy load of documents.
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
import pathlib
import shutil

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_APP_PATH
from proteus.model import PROJECT_FILE_NAME
from proteus.model.abstract_object import ProteusState
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.project import Project
from proteus.model.properties import Property, STRING_PROPERTY_TAG
from proteus.tests import PROTEUS_TEST_SAMPLE_DATA_PATH
from proteus.tests import fixtures

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

# NOTE: This is a sample project that is used for testing purposes.
SAMPLE_PROJECT_PATH = PROTEUS_TEST_SAMPLE_DATA_PATH / "example_project"
ARCHETYPE_REPOSITORY_PATH = PROTEUS_APP_PATH / "archetypes"

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
def sample_archetype_project() -> Project:
    """
    Fixture that returns a PROTEUS sample archetype project.
    """
    project_arquetypes : list(Project) = ArchetypeManager.load_project_archetypes()
    return project_arquetypes[0]


# --------------------------------------------------------------------------
# Project tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize('path',
    [
        SAMPLE_PROJECT_PATH
    ]
)

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

# --------------------------------------------------------------------------
# Project unit tests
# NOTE: Some methods are not testes with Archetype Projects because they
# are not meant to be used with them.
# --------------------------------------------------------------------------

@pytest.mark.parametrize('path',
    [
        SAMPLE_PROJECT_PATH / PROJECT_FILE_NAME,
        ARCHETYPE_REPOSITORY_PATH / "projects" / "madeja" / "project.xml"
    ],
)
def test_init(path):
    """
    It tests the init method of the Project class.
    """
    # Create a project using the constructor
    test_project = Project(SAMPLE_PROJECT_PATH / PROJECT_FILE_NAME)

    # Check type of the project
    assert(isinstance(test_project, Project)), \
        f"Project is not an instance of Project class. It is {type(test_project)}"

    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(SAMPLE_PROJECT_PATH / PROJECT_FILE_NAME)

    # Compare ET element id with the project id
    assert(root.attrib["id"] == test_project.id), \
        f"Project id {test_project.id} is not equal to the id of the root element {root.attrib['id']}"

def test_load():
    """
    It tests the load method of the Project class.
    """

    # Load the project
    test_project = Project.load(SAMPLE_PROJECT_PATH)

    # Check type of the project
    assert(isinstance(test_project, Project)), \
        f"Project is not an instance of Project class. It is {type(test_project)}"

    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(SAMPLE_PROJECT_PATH / PROJECT_FILE_NAME)

    # Compare ET element id with the project id
    assert(root.attrib["id"] == test_project.id), \
        f"Project id {test_project.id} is not equal to the id of the root element {root.attrib['id']}"

@pytest.mark.parametrize(
        "sample_project_fixture",
        ["sample_project", "sample_archetype_project"],
)
def test_documents_lazy_load(sample_project_fixture: str, request):
    """
    Test Project documents property lazy loading
    """
    # Get sample project
    # NOTE: using parameterized fixtures to get the sample project
    # https://engineeringfordatascience.com/posts/pytest_fixtures_with_parameterize/
    sample_project = request.getfixturevalue(sample_project_fixture)

    # Check that documents are not loaded yet checking private
    # variable _documents
    assert(sample_project._documents == None), \
        "Documents should not be loaded if the 'documents' property is not accessed"

    # Check that documents are loaded when accessing documents
    # property for the first time
    assert(type(sample_project.documents) == dict),                     \
        f"Documents should have been loaded when accessing 'documents'  \
        property but they are of type {type(sample_project.documents)}"
    assert(type(sample_project._documents) == dict),                    \
        f"Documents private var should have been loaded when accessing  \
        'documents' property but they are of type {type(sample_project._documents)}"

@pytest.mark.parametrize(
        "sample_project_fixture",
        ["sample_project", "sample_archetype_project"],
)
def test_load_documents(sample_project_fixture: str, request):
    """
    Test Project load_documents method
    """
    # Get sample project
    # NOTE: using parameterized fixtures to get the sample project
    # https://engineeringfordatascience.com/posts/pytest_fixtures_with_parameterize/
    sample_project = request.getfixturevalue(sample_project_fixture)

    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(sample_project.path)

    # Get documents of the xml file and store them in a list
    documents = root.find("documents")
    documents_list : list = []
    for document in documents:
        documents_list.append(document.attrib["id"] )

    # Call method to load documents
    # NOTE: This method could be called when accessing documents
    # for the first time and no documents are loaded yet. However,
    # we are calling it explicitly to test it in case lazy loading
    # fails.
    sample_project.load_documents()

    # Check that Object contains all the documents of the xml    
    assert(all(document in sample_project.documents.keys() for document in documents_list)), \
        f"Project does not contain all the documents of the xml file.                        \
        Documents in xml file: {documents_list}                                              \
        Documents in Project: {sample_project.documents.keys()}"

def test_generate_xml(sample_project: Project):
    """
    Test Project generate_xml method
    """
    # Get root element of the xml file
    root : ET.Element = fixtures.get_root(sample_project.path)

    # Get xml string from xml file
    expected_xml= (ET.tostring(root,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True).decode())

    # Generate xml
    xml : ET.Element = sample_project.generate_xml()

    # Get xml string from Object
    actual_xml= (ET.tostring(xml,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True).decode())

    # Compare xml strings
    assert(expected_xml == actual_xml), \
        f"XML strings are not equal. Expected: {expected_xml} Actual: {actual_xml}"

@pytest.mark.parametrize(
        "sample_project_fixture",
        ["sample_project", "sample_archetype_project"],
)
def test_clone(sample_project_fixture: str, request):
    """
    Test Project clone method
    """
    # Path to the cloned project
    new_project_dir_name = "cloned_project"
    clone_path = PROTEUS_TEST_SAMPLE_DATA_PATH
    cloned_project_path = clone_path / new_project_dir_name

    # Remove cloned project if it exists
    if os.path.exists(cloned_project_path):
        shutil.rmtree(cloned_project_path)

    # Get sample project
    # NOTE: using parameterized fixtures to get the sample project
    # https://engineeringfordatascience.com/posts/pytest_fixtures_with_parameterize/
    sample_project = request.getfixturevalue(sample_project_fixture)

    # Clone project
    new_project = sample_project.clone_project(clone_path, new_project_dir_name)

    # Check that the project has been cloned
    assert(isinstance(new_project, Project)), \
        f"Project type is not Project. Type: {type(new_project)}"

    # Compare project id
    assert(sample_project.id == new_project.id), \
        f"Project id is not equal.               \
        Expected: {sample_project.id} Actual: {new_project.id}"

    # Compare project path
    assert(cloned_project_path == pathlib.Path(new_project.path).parent.resolve()), \
        f"Project path is not equal.                                                \
        Expected: {cloned_project_path} Actual: {new_project.path}"

    # Clean up cloned project directory
    if os.path.exists(cloned_project_path):
        os.chdir(PROTEUS_TEST_SAMPLE_DATA_PATH)
        shutil.rmtree(cloned_project_path)

# TODO: Test Project save_project method

def test_set_property(sample_project: Project):
    """
    Test Abstract Object set_property method
    """
    # Create property
    (new_property, name, _) = fixtures.create_property(STRING_PROPERTY_TAG, "name", "general", "Test value")

    # Set property
    sample_project.set_property(new_property)

    # Check that property was set
    assert(sample_project.get_property(name) == new_property),  \
        f"Property was not set. Expected value: {new_property} \
        Actual value: {sample_project.get_property(name)}"
    

def test_get_ids_from_project(sample_project: Project):
    """
    Test Project get_ids_from_project method
    """
    # Expected ids in sample_project
    expected_len = 5

    # Get ids from project
    ids = sample_project.get_ids_from_project()

    # Check that ids are equal
    assert(len(ids) == expected_len), \
        f"Ids are not equal. Expected: {expected_len}, Actual: {ids}"