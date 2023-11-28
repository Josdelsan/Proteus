# ==========================================================================
# File: test_clone_archetype_object.py
# Description: pytest file for the PROTEUS clone_archetype_object command.
# Date: 28/11/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.trace import Trace
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.services.archetype_service import ArchetypeService
from proteus.views.utils.state_manager import StateManager
from proteus.controller.commands.clone_archetype_object import (
    CloneArchetypeObjectCommand,
)
from proteus.tests import PROTEUS_SAMPLE_DATA_PATH
from proteus.tests.fixtures import SampleData

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

SAMPLE_PROJECT_PATH = PROTEUS_SAMPLE_DATA_PATH / "example_project"
SAMPLE_PARENT_ID = SampleData.get("simple_section")
SAMPLE_ARCHETYPE_ID = "empty-paragraph"


@pytest.fixture
def sample_project_service():
    sample_project_service = ProjectService()
    sample_project_service.load_project(SAMPLE_PROJECT_PATH)
    return sample_project_service


@pytest.fixture
def sample_archetype_service():
    service = ArchetypeService()
    # Force load of object archetypes
    service.get_object_archetypes()
    return service


# --------------------------------------------------------------------------
# Integration tests
# --------------------------------------------------------------------------
# NOTE: We take a black box approach to test the command outcoming results.
#       Implementation is tricky because undo will mark the object as deleted
#       and will force redo to behave different in the second run.


def test_clone_archetype_object_command_redo(
    sample_project_service: ProjectService,
    sample_archetype_service: ArchetypeService,
):
    """
    Test that the redo method of the CloneArchetypeObjectCommand class works
    as expected.

    Check archetype was cloned inside parent in the last position.
    Check parent and object states

    Comparison is done by comparing :Proteus-name property, this depends on
    the sample data used. There are no object archetypes with children, so
    the test is not parametrized to tests different depths.

    NOTE: Object clone_object method is tested in object test suite.
    We assume it works as expected.
    """
    # Arrange -------------------------
    parent = sample_project_service._get_element_by_id(SAMPLE_PARENT_ID)
    object_archetype = sample_archetype_service._get_archetype_by_id(
        SAMPLE_ARCHETYPE_ID
    )

    # Act -----------------------------
    command = CloneArchetypeObjectCommand(
        SAMPLE_ARCHETYPE_ID,
        SAMPLE_PARENT_ID,
        sample_project_service,
        sample_archetype_service,
    )

    command.redo()

    # Assert --------------------------
    # Check parent state is DIRTY (project was just loaded, will never be FRESH)
    assert (
        parent.state == ProteusState.DIRTY
    ), f"Parent state is not DIRTY. State: {parent.state}"

    # Check the last object in parent is equal to the archetype (compare names)
    last_object = parent.get_descendants()[-1]
    assert (
        last_object.get_property(PROTEUS_NAME).value
        == object_archetype.get_property(PROTEUS_NAME).value
    ), f"Last object in parent is not equal to archetype. \
        Last object: {last_object.get_property(PROTEUS_NAME).value}, \
        Archetype: {object_archetype.get_property(PROTEUS_NAME).value}"

    # Check object state is FRESH
    assert (
        last_object.state == ProteusState.FRESH
    ), f"Object state is not FRESH. State: {last_object.state}"


def test_clone_archetype_object_command_undo(
    sample_project_service: ProjectService,
    sample_archetype_service: ArchetypeService,
):
    """
    Test that the undo method of the CloneArchetypeObjectCommand class works
    as expected.

    Check the cloned object (last object in parent) is marked as deleted and
    also its children.
    Check parent state is previous to clone.

    NOTE: Object clone_object method is tested in object test suite.
    We assume it works as expected.
    """
    # Arrange -------------------------
    parent = sample_project_service._get_element_by_id(SAMPLE_PARENT_ID)

    # Store parent state before clone
    before_clone_parent_state = parent.state

    # Act -----------------------------
    command = CloneArchetypeObjectCommand(
        SAMPLE_ARCHETYPE_ID,
        SAMPLE_PARENT_ID,
        sample_project_service,
        sample_archetype_service,
    )

    command.redo()
    command.undo()

    # Assert --------------------------
    # Check parent state is previous to clone
    assert (
        parent.state == before_clone_parent_state
    ), f"Parent state is not previous to clone. State: {parent.state}"

    # Check the last object in parent (and object children) is marked as deleted
    last_object = parent.get_descendants()[-1]
    for id in last_object.get_ids():
        assert (
            sample_project_service._get_element_by_id(id).state == ProteusState.DEAD
        ), f"Object {id} is not marked as deleted. State: {sample_project_service._get_element_by_id(id).state}"


def test_clone_archetype_object_command_redo_after_undo(
    sample_project_service: ProjectService,
    sample_archetype_service: ArchetypeService,
):
    """
    Test that the redo method of the CloneArchetypeObjectCommand class works
    as expected after undo was performed. Redo will restore the object and
    children state to FRESH instead cloning again the archetype.

    Check archetype was cloned inside parent in the last position.
    Check parent and object states

    Comparison is done by comparing :Proteus-name property, this depends on
    the sample data used. There are no object archetypes with children, so
    the test is not parametrized to tests different depths.

    NOTE: Object clone_object method is tested in object test suite.
    We assume it works as expected.
    """
    # Arrange -------------------------
    parent = sample_project_service._get_element_by_id(SAMPLE_PARENT_ID)
    object_archetype = sample_archetype_service._get_archetype_by_id(
        SAMPLE_ARCHETYPE_ID
    )

    # Act -----------------------------
    command = CloneArchetypeObjectCommand(
        SAMPLE_ARCHETYPE_ID,
        SAMPLE_PARENT_ID,
        sample_project_service,
        sample_archetype_service,
    )

    command.redo()
    command.undo()
    command.redo()

    # Assert --------------------------
    # Check parent state is DIRTY (project was just loaded, will never be FRESH)
    assert (
        parent.state == ProteusState.DIRTY
    ), f"Parent state is not DIRTY. State: {parent.state}"

    # Check the last object in parent is equal to the archetype (compare names)
    last_object = parent.get_descendants()[-1]
    assert (
        last_object.get_property(PROTEUS_NAME).value
        == object_archetype.get_property(PROTEUS_NAME).value
    ), f"Last object in parent is not equal to archetype. \
        Last object: {last_object.get_property(PROTEUS_NAME).value}, \
        Archetype: {object_archetype.get_property(PROTEUS_NAME).value}"

    # Check object state is FRESH
    assert (
        last_object.state == ProteusState.FRESH
    ), f"Object state is not FRESH. State: {last_object.state}"
