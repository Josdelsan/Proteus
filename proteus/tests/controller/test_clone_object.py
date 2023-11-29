# ==========================================================================
# File: test_clone_object.py
# Description: pytest file for the PROTEUS clone_object command.
# Date: 29/11/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.controller.commands.clone_object import (
    CloneObjectCommand,
)
from proteus.tests import PROTEUS_SAMPLE_DATA_PATH
from proteus.tests.fixtures import SampleData

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

SAMPLE_PROJECT_PATH = PROTEUS_SAMPLE_DATA_PATH / "example_project"


@pytest.fixture
def sample_project_service():
    sample_project_service = ProjectService()
    sample_project_service.load_project(SAMPLE_PROJECT_PATH)
    return sample_project_service


# --------------------------------------------------------------------------
# Integration tests
# --------------------------------------------------------------------------
# NOTE: We take a black box approach to test the command outcoming results.
#       Implementation is tricky because undo will mark the object as deleted
#       and will force redo to behave different in the second run.


@pytest.mark.parametrize(
    "object_name",
    [
        ("simple_paragraph"),
        ("section_dl_1"),
        ("section_dl_2"),
    ],
)
def test_clone_object_command_redo(sample_project_service: ProjectService, object_name):
    """
    Test that the redo method of the CloneObjectCommand class works
    as expected.

    Check the object was cloned just after the original object position.
    Check parent state was updated.

    Comparison is done by comparing :Proteus-name property, this depends on
    the sample data used. Test is parametrized to test different depths.

    NOTE: Object clone_object method is tested in object test suite.
    We assume it works as expected.
    """
    # Arrange -------------------------
    object_id = SampleData.get(object_name)
    original_object = sample_project_service._get_element_by_id(object_id)
    parent = original_object.parent

    # Act -----------------------------
    delete_object_command = CloneObjectCommand(object_id, sample_project_service)

    delete_object_command.redo()

    # Assert --------------------------
    # Check parent state was updated to DIRTY (project just loaded, it is always CLEAN)
    assert (
        parent.state == ProteusState.DIRTY
    ), f"Parent state should be DIRTY, but it is {parent.state}"

    # Check object was cloned just after the original object position
    original_object_index = parent.get_descendants().index(original_object)
    cloned_object = parent.get_descendants()[original_object_index + 1]
    assert (
        cloned_object.get_property(PROTEUS_NAME).value
        == original_object.get_property(PROTEUS_NAME).value
    ), f"Cloned object name should be {original_object.get_property(PROTEUS_NAME).value}, but it is {cloned_object.get_property(PROTEUS_NAME).value}. \
            The new object should be just after the original object in position {original_object_index + 1}."

    # Check the new object and its children are FRESH state
    for id in cloned_object.get_ids():
        assert (
            sample_project_service._get_element_by_id(id).state == ProteusState.FRESH
        ), f"Object {id} should be FRESH, but it is {sample_project_service._get_element_by_id(id).state}"


@pytest.mark.parametrize(
    "object_name",
    [
        ("simple_paragraph"),
        ("section_dl_1"),
        ("section_dl_2"),
    ],
)
def test_clone_object_command_undo(sample_project_service: ProjectService, object_name):
    """
    Test that the undo method of the CloneObjectCommand class works
    as expected.

    Check the object was marked as DEAD.
    Check parent state was reverted.

    Comparison is done by comparing :Proteus-name property, this depends on
    the sample data used. Test is parametrized to test different depths.

    NOTE: Object clone_object method is tested in object test suite.
    We assume it works as expected.
    """
    # Arrange -------------------------
    object_id = SampleData.get(object_name)
    original_object = sample_project_service._get_element_by_id(object_id)
    parent = original_object.parent

    # Store old parent state
    old_parent_state = parent.state

    # Act -----------------------------
    delete_object_command = CloneObjectCommand(object_id, sample_project_service)

    delete_object_command.redo()
    delete_object_command.undo()

    # Assert --------------------------
    # Check parent state was reverted to its original state
    assert (
        parent.state == old_parent_state
    ), f"Parent state should be {old_parent_state}, but it is {parent.state}"

    # Calculate new object position (we do not check if the name is the same, it is done in redo test)
    original_object_index = parent.get_descendants().index(original_object)
    cloned_object = parent.get_descendants()[original_object_index + 1]

    # Check the new object and its children are DEAD state
    for id in cloned_object.get_ids():
        assert (
            sample_project_service._get_element_by_id(id).state == ProteusState.DEAD
        ), f"Object {id} should be DEAD, but it is {sample_project_service._get_element_by_id(id).state}"


@pytest.mark.parametrize(
    "object_name",
    [
        ("simple_paragraph"),
        ("section_dl_1"),
        ("section_dl_2"),
    ],
)
def test_clone_object_command_redo_after_undo(
    sample_project_service: ProjectService, object_name
):
    """
    Test that the undo method of the CloneObjectCommand class works
    as expected.

    Check the object was marked as FRESH again.
    Check parent state was set to DIRTY.

    Comparison is done by comparing :Proteus-name property, this depends on
    the sample data used. Test is parametrized to test different depths.

    NOTE: Object clone_object method is tested in object test suite.
    We assume it works as expected.
    """
    # Arrange -------------------------
    object_id = SampleData.get(object_name)
    original_object = sample_project_service._get_element_by_id(object_id)
    parent = original_object.parent

    # Act -----------------------------
    delete_object_command = CloneObjectCommand(object_id, sample_project_service)

    delete_object_command.redo()
    delete_object_command.undo()
    delete_object_command.redo()

    # Assert --------------------------
    # Check parent state was updated to DIRTY (project just loaded, it is always CLEAN)
    assert (
        parent.state == ProteusState.DIRTY
    ), f"Parent state should be DIRTY, but it is {parent.state}"

    # Calculate new object position (we do not check if the name is the same, it is done in redo test)
    original_object_index = parent.get_descendants().index(original_object)
    cloned_object = parent.get_descendants()[original_object_index + 1]

    # Check the new object and its children are FRESH state
    for id in cloned_object.get_ids():
        assert (
            sample_project_service._get_element_by_id(id).state == ProteusState.FRESH
        ), f"Object {id} should be FRESH, but it is {sample_project_service._get_element_by_id(id).state}"
