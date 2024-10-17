# ==========================================================================
# File: test_archetype_repository.py
# Description: pytest file for the PROTEUS ArchetypeRepository
# Date: 20/10/2022
# Version: 0.2
# Author: José María Delgado Sánchez
#         Pablo Rivera Jiménez
# ==========================================================================
# Update: 15/04/2023 (José María)
# Description:
# - Tests adapted to the new ArchetypeRepository logic
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.configuration.config import Config
from proteus.model.archetype_repository import ArchetypeRepository
from proteus.model.object import Object
from proteus.model.project import Project

# --------------------------------------------------------------------------
# Fixtures and helpers
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# ArchetypeRepository unit tests
# --------------------------------------------------------------------------


def test_project_archetype():
    # Get the number of projects in archetypes projects
    current_archetype_repository = Config().profile_settings.archetypes_directory
    dir_path = str(current_archetype_repository / "projects")
    number_of_projects: int = len(os.listdir(dir_path))

    # Check if load project function return all the projects
    projects: list[Project] = ArchetypeRepository.load_project_archetypes(
        current_archetype_repository
    )
    assert (
        len(projects) == number_of_projects
    ), f"Number of archetype projects not match with the number of archetype projects in the directory"

    # Check if the projects are Project objects
    for project in projects:
        assert isinstance(
            project, Project
        ), f"Archetype project {project} is not a Project object"


def test_document_archetype():
    # Get the number of documents in archetypes documents
    current_archetype_repository = Config().profile_settings.archetypes_directory
    dir_path = str(current_archetype_repository / "documents")
    number_of_documents = len(os.listdir(dir_path))

    # Check if load document function return all the documents
    documents: list[Object] = ArchetypeRepository.load_document_archetypes(
        current_archetype_repository
    )
    assert (
        len(documents) == number_of_documents
    ), f"Number of archetype documents not match with the number of archetype documents in the directory"

    # Check if the documents are Object objects
    for document in documents:
        assert isinstance(
            document, Object
        ), f"Archetype document {document} is not a Object object"


def test_object_archetype():
    # Get the number of objects arquetypes clases
    current_archetype_repository = Config().profile_settings.archetypes_directory
    dir_path = str(current_archetype_repository / "objects")
    archetype_groups = os.listdir(dir_path)

    # Check if load object function return all the classes
    objects: dict[str, dict[str, List[Object]]] = (
        ArchetypeRepository.load_object_archetypes(current_archetype_repository)
    )
    for archetype_group in archetype_groups:

        # Check if the class is in the objects dictionary (parsed to remove order prefix)
        assert (
            archetype_group[3:] in objects.keys()
        ), f"Archetype group {archetype_group} not found in objects"

        # Parse the objects.xml file of the class
        objects_pointer_xml: ET._ElementTree = ET.parse(
            f"{dir_path}/{archetype_group}/objects.xml"
        )

        # Get the number of objects in the objects.xml file ignoring children objects
        objects_id_list: list[str] = [
            child.attrib["id"] for child in objects_pointer_xml.getroot()
        ]
        number_of_objects_expected = len(objects_id_list)

        # Check if the number of objects in the class is correct
        objects_list: list[Object] = []
        for object in objects[archetype_group[3:]].values():
            objects_list.extend(object)

        assert (
            len(objects_list) == number_of_objects_expected
        ), f"Number of objects in group {archetype_group} do not match with the number of objects in the directory"

        # Check if the objects are Object objects
        for object in objects_list:
            assert isinstance(
                object, Object
            ), f"Archetype object {object} is not a Object object"

    # Check if the number of classes in the directory is correct
    assert len(objects.keys()) == len(
        archetype_groups
    ), f"Number of object archetype groups not match with the number of groups in the directory"

    # Check if the objects groups are stored in the correct order
    archetype_groups.sort(key=lambda x: int(x[:2]))
    correct_order = [name[3:] for name in archetype_groups]
    assert (
        list(objects.keys()) == correct_order
    ), f"Object groups are not stored in the correct order"
