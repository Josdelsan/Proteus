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
    It returns a new instance of the ProjectService class.
    """
    return ProjectService(SAMPLE_PROJECT_PATH)

# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

def test_project_service_init(project_service : ProjectService):
    """
    It tests the initialization of the project service.
    """
    # Check that the project service is initialized
    assert isinstance(project_service.project, Project), \
        "Project should be instance of Project"
    
    # Get all ids from the project
    project_ids : List[ProteusID] = project_service.project.get_ids_from_project()
    project_ids.append(project_service.project.id)

    # Get ids present in the index
    index_ids : List[ProteusID] = project_service.project_index.keys()

    # Check that all ids are present in the index
    assert set(index_ids) == set(project_ids),   \
        f"Some ids are not present in the index" \
        f"\n\tProject ids: {project_ids}"        \
        f"\n\tIndex ids: {index_ids}"
    
def test_get_project_structure(project_service : ProjectService):
    """
    It tests the get_project_structure method.
    """
    # Get project structure
    project_structure : List[ProteusID] = project_service.get_project_structure()

    # Get project documents ids
    project_document_ids : List[ProteusID] = project_service.project.documents.keys()

    # Check that the project structure is correct
    assert set(project_document_ids) == set(project_structure),                 \
        f"Project structure is not correct"                                     \
        f"\n\tProject structure: {project_structure}"                           \
        f"\n\tProject service structure: {project_service.project_structure}"

# TODO: improve readability
def test_get_object_structure(project_service : ProjectService):
    """
    It tests the get_object_structure method.
    """
    # Get object structure
    object_structure : Dict[ProteusID, List] = project_service.get_object_structure(SAMPLE_OBJECT_ID)

    # TODO: Check structure in all depth levels

    # Check that the object structure has 1 element in first depth level
    assert len(object_structure.keys()) == 1, \
        f"Object structure should have 1 element in first depth level"
    
    # Get object id
    object_id : ProteusID = list(object_structure.keys())[0]

    # Get object children ids
    object : Object = project_service._get_element_by_id(object_id)
    object_children_ids : List[ProteusID] = set(object.children.keys())

    # Get object structure children ids
    children_dicts : List[Dict] = object_structure[object_id]
    object_structure_children_ids : List[ProteusID] = set([ list(d.keys())[0] for d in children_dicts ])

    # Check that the object structure is correct second depth level
    assert object_children_ids == object_structure_children_ids,                \
        f"Object structure is not correct"                                      \
        f"\n\tObject children ids: {object_children_ids}"                       \
        f"\n\tObject structure children ids: {object_structure_children_ids}"

# TODO: test populate index
# TODO: test get properties
# TODO: test update properties
# TODO: test save project
# TODO: test delete object

# NOTE: Some tests might not be necessary if the project service methods
# are tested in the project model tests.
