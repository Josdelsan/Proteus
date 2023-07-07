# ==========================================================================
# File: test_achetype_service.py
# Description: pytest file for the PROTEUS archetype service
# Date: 02/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict, Union

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
from proteus.model.archetype_manager import ArchetypeManager
from proteus.services.archetype_service import ArchetypeService

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def archetype_service():
    """
    It returns a new instance of the ArchetypeService class.
    """
    return ArchetypeService()

# --------------------------------------------------------------------------
# Integration tests
# --------------------------------------------------------------------------

# test_project_archetypes_lazy_load ----------------------------------------
def test_project_archetypes_lazy_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the project archetypes.

    Depends on the archetypes folder content.
    """
    # Arrange -------------------------
    # Check that the project archetypes are not loaded
    assert (
        archetype_service._project_archetypes is None
    ), "ArchetypeService._project_archetypes should be None"

    # Act -----------------------------
    # Load the project archetypes calling the property
    project_archetypes: List[Project] = archetype_service.get_project_archetypes()

    # Assert --------------------------
    # Check that the project archetypes are loaded
    assert isinstance(
        project_archetypes, list
    ), f"ArchetypeService.project_archetypes should be a list, not {type(project_archetypes)}"
    assert (
        archetype_service._project_archetypes == project_archetypes
    ), "ArchetypeService._project_archetypes should be equal to ArchetypeService.project_archetypes"


# test_document_archetypes_lazy_load ---------------------------------------
def test_document_archetypes_lazy_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the document archetypes.

    Depends on the archetypes folder content.
    """
    # Check that the document archetypes are not loaded
    # Arrange -------------------------
    assert (
        archetype_service._document_archetypes is None
    ), "ArchetypeService._document_archetypes should be None"

    # Act -----------------------------
    # Load the document archetypes calling the property
    document_archetypes: List[Object] = archetype_service.get_document_archetypes()

    # Assert --------------------------
    # Check that the document archetypes are loaded
    assert isinstance(
        document_archetypes, list
    ), f"ArchetypeService.document_archetypes should be a list, not {type(document_archetypes)}"
    assert (
        archetype_service._document_archetypes == document_archetypes
    ), "ArchetypeService._document_archetypes should be equal to ArchetypeService.document_archetypes"


# test_object_arquetypes_lazy_load -----------------------------------------
def test_object_arquetypes_lazy_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the object archetypes.

    Depends on the archetypes folder content.
    """
    # Arrange -------------------------
    # Check that the object archetypes are not loaded
    assert (
        archetype_service._object_archetypes is None
    ), "ArchetypeService._object_archetypes should be None"

    # Act -----------------------------
    # Load the object archetypes calling the property
    object_archetypes: Dict[
        str, List[Object]
    ] = archetype_service.get_object_archetypes()

    # Assert --------------------------
    # Check that the object archetypes are loaded
    assert isinstance(
        object_archetypes, dict
    ), f"ArchetypeService.object_archetypes should be a dict, not {type(object_archetypes)}"
    assert (
        archetype_service._object_archetypes == object_archetypes
    ), "ArchetypeService._object_archetypes should be equal to ArchetypeService.object_archetypes"


# test_archetype_index_load ------------------------------------------------
def test_archetype_index_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the archetype index.

    Depends on the archetypes folder content.
    """
    # Arrange | Act -------------------
    # Load the archetypes calling the properties
    project_archetypes: List[Project] = archetype_service.get_project_archetypes()
    document_archetypes: List[Object] = archetype_service.get_document_archetypes()
    object_archetypes: Dict[
        str, List[Object]
    ] = archetype_service.get_object_archetypes()

    # Get ids of the archetypes
    project_archetypes_ids: List[ProteusID] = set(
        project.id for project in project_archetypes
    )
    document_archetypes_ids: List[ProteusID] = set(
        document.id for document in document_archetypes
    )
    object_archetypes_ids: List[ProteusID] = set()
    for object_class_list in object_archetypes.values():
        object_archetypes_ids.update(object.id for object in object_class_list)

    archetypes_ids = project_archetypes_ids.union(document_archetypes_ids).union(
        object_archetypes_ids
    )

    # Get the keys from the archetype_index
    archetype_index_keys: List[ProteusID] = set(
        archetype_service.archetype_index.keys()
    )

    # Assert --------------------------
    # Check that the archetype_index is updated
    assert (
        archetypes_ids == archetype_index_keys
    ), "ArchetypeService.archetype_index should contain the all archetypes"


# test_get_project_archetypes ----------------------------------------------
def test_get_project_archetypes(archetype_service: ArchetypeService):
    """
    It tests the get_project_archetypes method.

    Depends on the archetypes folder content.
    """
    # Act -----------------------------
    # Load the project archetypes list
    project_archetypes: List[Project] = archetype_service.get_project_archetypes()

    # Assert --------------------------
    # Check that the project archetypes are loaded
    assert isinstance(
        project_archetypes, list
    ), f"ArchetypeService.project_archetypes should be a list, not {type(project_archetypes)}"


# test_get_document_archetypes ---------------------------------------------
def test_get_document_archetypes(archetype_service: ArchetypeService):
    """
    It tests the get_document_archetypes method.

    Depends on the archetypes folder content.
    """
    # Act -----------------------------
    # Load the document archetypes list
    document_archetypes: List[Object] = archetype_service.get_document_archetypes()

    # Assert --------------------------
    # Check that the document archetypes are loaded
    assert isinstance(
        document_archetypes, list
    ), f"ArchetypeService.document_archetypes should be a list, not {type(document_archetypes)}"


# test_get_object_archetypes_classes ---------------------------------------
def test_get_object_archetypes_classes(archetype_service: ArchetypeService):
    """
    It tests the get_object_archetypes_classes method.

    Depends on the archetypes folder content.
    """
    # Act -----------------------------
    # Load the object archetypes classes list
    object_archetypes_classes: List[
        str
    ] = archetype_service.get_object_archetypes_classes()

    # Assert --------------------------
    # Check that the object archetypes are loaded
    assert isinstance(
        object_archetypes_classes, list
    ), f"ArchetypeService.object_archetypes should be a list, not {type(object_archetypes_classes)}"


# test_get_object_archetypes_by_class --------------------------------------
def test_get_object_archetypes_by_class(archetype_service: ArchetypeService):
    """
    It tests the get_object_archetypes_by_class method.

    Depends on the archetypes folder content.
    """
    # Arrange -------------------------
    OBJECT_CLASS = "General"

    # Act -----------------------------
    # Load the object archetypes list
    object_archetypes_by_class: List[
        Object
    ] = archetype_service.get_object_archetypes_by_class(OBJECT_CLASS)

    # Assert --------------------------
    # Check that the object archetypes are loaded
    assert isinstance(
        object_archetypes_by_class, list
    ), f"ArchetypeService.object_archetypes should be a list, not {type(object_archetypes_by_class)}"

# test_get_archetype_by_id -------------------------------------------------
@pytest.mark.parametrize(
    "id", ["empty-paragraph", "madeja-project-id", "empty-document-01"]
)
def test_get_archetype_by_id(id: str, archetype_service: ArchetypeService):
    """
    It tests the get_archetype_by_id method.

    Depends on the archetypes folder content.
    """
    # Arrange -------------------------
    ARCHETYPE_ID = ProteusID(id)

    # Lazy load the archetypes
    archetype_service.get_project_archetypes()
    archetype_service.get_document_archetypes()
    archetype_service.get_object_archetypes()

    # Act -----------------------------
    # Load the archetype by id
    archetype: Union[Project, Object] = archetype_service._get_archetype_by_id(
        ARCHETYPE_ID
    )

    # Assert --------------------------
    # Check that the archetype is loaded
    assert isinstance(
        archetype, (Project, Object)
    ), f"ArchetypeService.object_archetypes should be a dict, not {type(archetype)}"


# --------------------------------------------------------------------------
# Unit tests
# --------------------------------------------------------------------------

# test_get_project_archetypes ----------------------------------------------
def test_get_project_archetypes_invalid_archetypes(
    mocker, archetype_service: ArchetypeService
):
    """
    Test that an assertion error is raised when the archetypes are not a list.
    """
    # Arrange -------------------------
    # Set the project archetypes to None to ensure that the archetypes are loaded
    ArchetypeService._project_archetypes = None

    # Mock the load_project_archetypes function to return an invalid value (not a list)
    mock_archetypes = "invalid archetypes"
    mocker.patch.object(
        ArchetypeManager, "load_project_archetypes", return_value=mock_archetypes
    )

    # Act & Assert --------------------
    # Check that an assertion error is raised when the archetypes are not a list
    with pytest.raises(AssertionError):
        archetype_service.get_project_archetypes()

def test_get_project_archetypes_duplicate_id(mocker, archetype_service: ArchetypeService):
    # Arrange -------------------------
    # Mock the load_project_archetypes function to return a list with duplicate project IDs
    project_mock = mocker.Mock(spec=Project)
    project_mock.id = "1"
    mock_archetypes = [project_mock, project_mock]
    mocker.patch.object(
        ArchetypeManager, "load_project_archetypes", return_value=mock_archetypes
    )
    # Set _project_archetypes to None to force the reload
    # NOTE: This might not be necessary in future versions of the ArchetypeService
    ArchetypeService._project_archetypes = None

    # Act & Assert --------------------
    # Check that an assertion error is raised when duplicate project IDs are found
    with pytest.raises(AssertionError):
        archetype_service.get_project_archetypes()


# test_get_document_archetypes ---------------------------------------------
def test_get_document_archetypes_invalid_archetypes(
    mocker, archetype_service: ArchetypeService
):
    """
    Test that an assertion error is raised when the archetypes are not a list.
    """
    # Arrange -------------------------
    # Set the document archetypes to None to ensure that the archetypes are loaded
    ArchetypeService._document_archetypes = None

    # Mock the load_document_archetypes function to return an invalid value (not a list)
    mock_archetypes = "invalid archetypes"
    mocker.patch.object(
        ArchetypeManager, "load_document_archetypes", return_value=mock_archetypes
    )

    # Act & Assert --------------------
    # Check that an assertion error is raised when the archetypes are not a list
    with pytest.raises(AssertionError):
        archetype_service.get_document_archetypes()

def test_get_document_archetypes_duplicate_id(mocker, archetype_service: ArchetypeService):
    """
    Test that an assertion error is raised when there are documents with duplicate IDs.
    """
    # Arrange -------------------------
    # Mock the load_document_archetypes function to return a list with duplicate documentIDs
    document_mock = mocker.Mock(spec=Object)
    document_mock.id = "1"
    mock_archetypes = [document_mock, document_mock]
    mocker.patch.object(
        ArchetypeManager, "load_document_archetypes", return_value=mock_archetypes
    )
    # Set _document_archetypes to None to force the reload
    # NOTE: This might not be necessary in future versions of the ArchetypeService
    ArchetypeService._document_archetypes = None

    # Act & Assert --------------------
    # Check that an assertion error is raised when duplicate document IDs are found
    with pytest.raises(AssertionError):
        archetype_service.get_document_archetypes()


# test_get_object_archetypes -----------------------------------------------
def test_get_object_archetypes_invalid_archetypes(
    mocker, archetype_service: ArchetypeService
):
    """
    Test that an assertion error is raised when the archetypes are not a dict.
    """
    # Arrange -------------------------
    # Set the object archetypes to None to ensure that the archetypes are loaded
    ArchetypeService._object_archetypes = None

    # Mock the load_object_archetypes function to return an invalid value (not a dict)
    mock_archetypes = "invalid archetypes"
    mocker.patch.object(
        ArchetypeManager, "load_object_archetypes", return_value=mock_archetypes
    )

    # Act & Assert --------------------
    # Check that an assertion error is raised when the archetypes are not a dict
    with pytest.raises(AssertionError):
        archetype_service.get_object_archetypes()

def test_get_object_archetypes_duplicate_id(mocker, archetype_service: ArchetypeService):
    """
    Test that an assertion error is raised when there are objects with duplicate IDs.
    """
    # Arrange -------------------------
    # Mock the load_object_archetypes function to return a list with duplicate object IDs
    object_mock = mocker.Mock(spec=Object)
    object_mock.id = "1"
    mock_archetypes = {"General": [object_mock, object_mock]}
    mocker.patch.object(
        ArchetypeManager, "load_object_archetypes", return_value=mock_archetypes
    )
    # Set _object_archetypes to None to force the reload
    # NOTE: This might not be necessary in future versions of the ArchetypeService
    ArchetypeService._object_archetypes = None

    # Act & Assert --------------------
    # Check that an assertion error is raised when duplicate object IDs are found
    with pytest.raises(AssertionError):
        archetype_service.get_object_archetypes()

# test_get_archetype_by_id -------------------------------------------------
@pytest.mark.parametrize("id", ["", None, "non-existent-id"])
def test_get_archetype_by_id_negative(id: str, archetype_service: ArchetypeService):
    """
    Tests archetype_service._get_archetype_by_id with negative cases. Check that
    it raises the assert exception.
    """
    # Arrange -------------------------
    ARCHETYPE_ID = ProteusID(id)

    # Act | Assert --------------------
    with pytest.raises(AssertionError):
        archetype_service._get_archetype_by_id(ARCHETYPE_ID)


# test_create_project ------------------------------------------------------
@pytest.mark.parametrize(
    "archetype_id, project_name, save_path",
    [("archetype_id_1", "project_name_1", "/path/to/save_1")],
)
def test_create_project(mocker, archetype_id, project_name, save_path):
    """
    Test the create_project method. Positive case. Test that the _get_archetype_by_id
    and clone_project methods are called once with the correct parameters.
    """
    # Arrange -------------------------
    # Mock the _get_archetype_by_id method of ArchetypeService
    # return a mock project
    mock_project = mocker.Mock(spec=Project)
    mocker.patch.object(
        ArchetypeService, "_get_archetype_by_id", return_value=mock_project
    )
    # Mock the clone_project method of the mock project to do nothing
    mocker.patch.object(mock_project, "clone_project", return_value=None)

    # Act -----------------------------
    # Call the create_project method
    ArchetypeService.create_project(archetype_id, project_name, save_path)

    # Assert --------------------------
    # Assert that _get_archetype_by_id and mock_project.clone_project are called
    # once with the correct parameters
    ArchetypeService._get_archetype_by_id.assert_called_once_with(archetype_id)
    mock_project.clone_project.assert_called_once_with(save_path, project_name)


@pytest.mark.parametrize(
    "project_name, archetype_type",
    [
        ("", Project),  # Empty project name
        (None, Project),  # None project name
        ("Valid name", Object),  # Invalid archetype type
        ("Valid name", None),  # None archetype type
        (None, None),  # Invalid parameters
    ],
)
def test_create_project_negative(mocker, project_name, archetype_type):
    """
    Test the create_project method. Negative case. Test that assert is raised
    when passing incorrect parameters.
    """
    # Arrange -------------------------
    # Mock the _get_archetype_by_id method so we can
    mock_project = mocker.Mock(spec=archetype_type)
    mocker.patch.object(
        ArchetypeService, "_get_archetype_by_id", return_value=mock_project
    )
    archetype_id: str = "archetype_id_dummy"
    save_path: str = "/path/to/save/dummy"

    # Act | Assert --------------------
    # Call the create_project method
    with pytest.raises(AssertionError):
        ArchetypeService.create_project(archetype_id, project_name, save_path)


# test_create_object -------------------------------------------------------
@pytest.mark.parametrize(
    "archetype_id, parent, project",
    [("dummy_id", "dummy_parent", "dummy_project")],
)
def test_create_object(mocker, archetype_id, parent, project):
    """
    Test the create_object method. Positive case. Test that the _get_archetype_by_id
    and clone_project methods are called once with the correct parameters.
    """
    # Arrange -------------------------
    # Mock the _get_archetype_by_id method of ArchetypeService
    # return a mock object
    mock_object = mocker.Mock(spec=Object)
    mocker.patch.object(
        ArchetypeService, "_get_archetype_by_id", return_value=mock_object
    )
    # Mock the clone_object method of the mock project to do nothing
    mocker.patch.object(mock_object, "clone_object", return_value=None)

    # Act -----------------------------
    # Call the create_project method
    ArchetypeService.create_object(archetype_id, parent, project)

    # Assert --------------------------
    # Assert that _get_archetype_by_id and mock_project.clone_project are called
    # once with the correct parameters
    ArchetypeService._get_archetype_by_id.assert_called_once_with(archetype_id)
    mock_object.clone_object.assert_called_once_with(parent, project)


@pytest.mark.parametrize(
    "archetype_type",
    [(Project), (None)],
)
def test_create_object_negative(mocker, archetype_type):
    """
    Test the create_object method. Negative case. Test that assert is raised
    when passing incorrect parameters.
    """
    # Arrange -------------------------
    # Mock the _get_archetype_by_id method so we can
    mock_object = mocker.Mock(spec=archetype_type)
    mocker.patch.object(
        ArchetypeService, "_get_archetype_by_id", return_value=mock_object
    )
    archetype_id: str = "archetype_id_dummy"
    parent: str = "parent_dummy"
    project: str = "project_dummy"

    # Act | Assert --------------------
    # Call the create_project method
    with pytest.raises(AssertionError):
        ArchetypeService.create_object(archetype_id, parent, project)
