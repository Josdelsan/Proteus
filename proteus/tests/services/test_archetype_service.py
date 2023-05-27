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
# Tests
# --------------------------------------------------------------------------
def test_project_archetypes_lazy_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the project archetypes.
    """
    # Check that the project archetypes are not loaded
    assert archetype_service._project_archetypes is None, \
        "ArchetypeService._project_archetypes should be None"

    # Load the project archetypes calling the property
    project_archetypes : List[Project] = archetype_service.get_project_archetypes()

    # Check that the project archetypes are loaded
    assert isinstance(project_archetypes, list), \
        f"ArchetypeService.project_archetypes should be a list, not {type(project_archetypes)}"
    assert archetype_service._project_archetypes == project_archetypes, \
        "ArchetypeService._project_archetypes should be equal to ArchetypeService.project_archetypes"
    
def test_document_archetypes_lazy_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the document archetypes.
    """
    # Check that the document archetypes are not loaded
    assert archetype_service._document_archetypes is None, \
        "ArchetypeService._document_archetypes should be None"

    # Load the document archetypes calling the property
    document_archetypes : List[Object] = archetype_service.get_document_archetypes()

    # Check that the document archetypes are loaded
    assert isinstance(document_archetypes, list), \
        f"ArchetypeService.document_archetypes should be a list, not {type(document_archetypes)}"
    assert archetype_service._document_archetypes == document_archetypes, \
        "ArchetypeService._document_archetypes should be equal to ArchetypeService.document_archetypes"

def test_object_arquetypes_lazy_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the object archetypes.
    """
    # Check that the object archetypes are not loaded
    assert archetype_service._object_archetypes is None, \
        "ArchetypeService._object_archetypes should be None"

    # Load the object archetypes calling the property
    object_archetypes : Dict[str, List[Object]] = archetype_service.get_object_archetypes()

    # Check that the object archetypes are loaded
    assert isinstance(object_archetypes, dict), \
        f"ArchetypeService.object_archetypes should be a dict, not {type(object_archetypes)}"
    assert archetype_service._object_archetypes == object_archetypes, \
        "ArchetypeService._object_archetypes should be equal to ArchetypeService.object_archetypes"

def test_archetype_index_load(archetype_service: ArchetypeService):
    """
    It tests the lazy load of the archetype index.
    """
    
    # Load the archetypes calling the properties
    project_archetypes  : List[Project]           = archetype_service.get_project_archetypes()
    document_archetypes : List[Object]            = archetype_service.get_document_archetypes()
    object_archetypes   : Dict[str, List[Object]] = archetype_service.get_object_archetypes()

    # Get ids of the archetypes
    project_archetypes_ids  : List[ProteusID] = set(project.id for project in project_archetypes)
    document_archetypes_ids : List[ProteusID] = set(document.id for document in document_archetypes)
    object_archetypes_ids   : List[ProteusID] = set()
    for object_class_list in object_archetypes.values():
        object_archetypes_ids.update(object.id for object in object_class_list)

    archetypes_ids = project_archetypes_ids.union(document_archetypes_ids).union(object_archetypes_ids)

    # Get the keys from the archetype_index
    archetype_index_keys    : List[ProteusID] = set(archetype_service.archetype_index.keys())

    # Check that the archetype_index is updated
    assert archetypes_ids == archetype_index_keys, \
        "ArchetypeService.archetype_index should contain the all archetypes"

def test_get_project_archetypes(archetype_service: ArchetypeService):
    """
    It tests the get_project_archetypes method.
    """
    # Load the project archetypes list
    project_archetypes : List[Project] = archetype_service.get_project_archetypes()

    # Check that the project archetypes are loaded
    assert isinstance(project_archetypes, list), \
        f"ArchetypeService.project_archetypes should be a list, not {type(project_archetypes)}"

def test_get_document_archetypes(archetype_service: ArchetypeService):
    """
    It tests the get_document_archetypes method.
    """
    # Load the document archetypes list
    document_archetypes : List[Object] = archetype_service.get_document_archetypes()

    # Check that the document archetypes are loaded
    assert isinstance(document_archetypes, list), \
        f"ArchetypeService.document_archetypes should be a list, not {type(document_archetypes)}"
    
def test_get_object_archetypes_classes(archetype_service: ArchetypeService):
    """
    It tests the get_object_archetypes_classes method.
    """
    # Load the object archetypes classes list
    object_archetypes_classes : List[str] = archetype_service.get_object_archetypes_classes()

    # Check that the object archetypes are loaded
    assert isinstance(object_archetypes_classes, list), \
        f"ArchetypeService.object_archetypes should be a list, not {type(object_archetypes_classes)}"
    
def test_get_object_archetypes_by_class(archetype_service: ArchetypeService):
    """
    It tests the get_object_archetypes_by_class method.
    """
    # Fixture
    OBJECT_CLASS = "general"

    # Load the object archetypes list
    object_archetypes_by_class : List[Object] = archetype_service.get_object_archetypes_by_class(OBJECT_CLASS)

    # Check that the object archetypes are loaded
    assert isinstance(object_archetypes_by_class, list), \
        f"ArchetypeService.object_archetypes should be a list, not {type(object_archetypes_by_class)}"

@pytest.mark.parametrize("id", ["empty-paragraph", "madeja-project-id", "empty-document-01"])
def test_get_archetype_by_id(id: str, archetype_service: ArchetypeService):
    """
    It tests the get_archetype_by_id method.
    """
    # Fixture
    ARCHETYPE_ID = ProteusID(id)

    # Lazy load the archetypes
    archetype_service.get_project_archetypes()
    archetype_service.get_document_archetypes()
    archetype_service.get_object_archetypes()

    # Load the archetype by id
    archetype : Union[Project, Object] = archetype_service._get_archetype_by_id(ARCHETYPE_ID)

    # Check that the archetype is loaded
    assert isinstance(archetype, (Project, Object)), \
        f"ArchetypeService.object_archetypes should be a dict, not {type(archetype)}"

