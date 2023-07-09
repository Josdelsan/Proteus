# ==========================================================================
# File: test_project_service.py
# Description: pytest file for the PROTEUS project service
# Date: 07/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.services.project_service import ProjectService
from proteus.tests import PROTEUS_TEST_SAMPLE_DATA_PATH

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

SAMPLE_PROJECT_PATH = PROTEUS_TEST_SAMPLE_DATA_PATH / "example_project"
SAMPLE_OBJECT_ID = "3fKhMAkcEe2C"

@pytest.fixture
def project_service():
    """
    It returns a new instance of the ProjectService class. The project is
    loaded from the SAMPLE_PROJECT_PATH.

    Depends on Project.load method.
    """
    project_service : ProjectService = ProjectService()
    project_service.load_project(SAMPLE_PROJECT_PATH)
    return project_service

@pytest.fixture
def basic_project_service():
    """
    It returns a new instance of the ProjectService class. There is no project
    loaded.
    """
    project_service : ProjectService = ProjectService()
    return project_service

# --------------------------------------------------------------------------
# Integration tests
# --------------------------------------------------------------------------

def test_load_project(project_service : ProjectService):
    """
    It tests the initialization of the project service. check that the project
    is the correct class and that the project index is initialized.

    NOTE: load_project method is called in the project_service fixture.
    """
    # Arrange -------------------------
    # Check that the project service is initialized
    assert isinstance(project_service.project, Project), \
        "Project should be instance of Project"
    
    # Act -----------------------------
    # Get all ids from the project
    project_ids : List[ProteusID] = project_service.project.get_ids()

    # Get ids present in the index
    index_ids : List[ProteusID] = project_service.project_index.keys()

    # Assert --------------------------
    # Check that all ids are present in the index
    assert set(index_ids) == set(project_ids),   \
        f"Some ids are not present in the index" \
        f"\n\tProject ids: {project_ids}"        \
        f"\n\tIndex ids: {index_ids}"
    
def test_get_project_structure(project_service : ProjectService):
    """
    It tests the get_project_structure method.
    """
    # Arrange -------------------------
    # Get project documents ids
    project_document_ids : List[Object] = project_service.project.documents

    # Act -----------------------------
    # Get project structure
    project_structure : List[Object] = project_service.get_project_structure()

    # Assert --------------------------
    # Check that the project structure is correct
    assert set(project_document_ids) == set(project_structure),                 \
        f"Project structure is not correct"                                     \
        f"\n\tProject structure: {project_structure}"                           \
        f"\n\tProject service structure: {project_service.project_structure}"

def test_get_object_structure(project_service : ProjectService):
    """
    It tests the get_object_structure method.
    """
    # Act -----------------------------
    # Get object structure
    object_structure : Dict[ProteusID, List] = project_service.get_object_structure(SAMPLE_OBJECT_ID)

    # Post-actions --------------------
    # Get object
    object : ProteusID = list(object_structure.keys())[0]
    # Get object children
    object_children : List[ProteusID] = set(object.children)
    # Get object structure children ids
    children_dicts : List[Dict] = object_structure[object]
    object_structure_children : List[ProteusID] = set([ list(d.keys())[0] for d in children_dicts ])

    # Assert --------------------------
    # TODO: Check structure in all depth levels
    # Check that the object structure has 1 element in first depth level
    assert len(object_structure.keys()) == 1, \
        f"Object structure should have 1 element in first depth level"

    # Check that the object structure is correct second depth level
    assert object_children == object_structure_children,                \
        f"Object structure is not correct"                              \
        f"\n\tObject children: {object_children}"                       \
        f"\n\tObject structure children: {object_structure_children}"

# --------------------------------------------------------------------------
# Unit tests
# --------------------------------------------------------------------------

def test_update_properties(mocker, basic_project_service: ProjectService):
    """
    Test the update_properties method.
    """
    # Arrange -------------------------
    # Mock the _get_element_by_id method
    mock_element = mocker.MagicMock(spec=Object)
    mocker.patch.object(basic_project_service, "_get_element_by_id", return_value=mock_element)
    mocker.patch.object(mock_element, "set_property", return_value=None)

    # Act -----------------------------
    basic_project_service.update_properties("id", ["property1", "property2"])

    # Assert --------------------------
    assert mock_element.set_property.call_count == 2, \
        f"set_property should be called twice"
    
    assert basic_project_service._get_element_by_id.call_count == 1, \
        f"_get_element_by_id should be called once"

# TODO: test _get_element_by_id
# TODO: test _populate_index
# TODO: test change_state
# TODO: test delete object
# TODO: test clone_object
# TODO: test change_object_position
# TODO: test generate_document_xml
# TODO: test add_project_template
# TODO: test delete_project_template


# NOTE: test save_project might not be necessary because it is a simple call
# to the project save method, which is tested in the project model tests.
# NOTE: test get_properties might not be necessary because it is a simple access
# to the object properties attribute and _get_element_by_id method call.

