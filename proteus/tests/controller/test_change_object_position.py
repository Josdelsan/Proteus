# ==========================================================================
# File: test_change_object_position.py
# Description: pytest file for the PROTEUS change_object_position command.
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
from proteus.controller.commands.change_object_position import (
    ChangeObjectPositionCommand,
)
from proteus.tests import PROTEUS_SAMPLE_PROJECTS_PATH
from proteus.tests.fixtures import SampleData

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

SAMPLE_PROJECT_PATH = PROTEUS_SAMPLE_PROJECTS_PATH / "example_project"


@pytest.fixture
def sample_project_service():
    sample_project_service = ProjectService()
    sample_project_service.load_project(SAMPLE_PROJECT_PATH.as_posix())
    return sample_project_service


# --------------------------------------------------------------------------
# Unit tests
# --------------------------------------------------------------------------
# NOTE: For redo method, we only need to test project service methods are
# called correctly since the method is completely dependent on the project
# service implementation which is already tested.


@pytest.mark.parametrize(
    "object_name, new_parent_name, new_position",
    [
        ("simple_paragraph", "document_1", None),
        ("simple_paragraph", "document_1", 8),
        ("simple_objective", "document_1", 0),
    ],
)
def test_change_object_position_command_redo(
    mocker,
    sample_project_service: ProjectService,
    object_name: str,
    new_parent_name: str,
    new_position: int,
):
    """
    Test that the redo method of the ChangeObjectPositionCommand class works by
    ensuring that the project service methods are called correctly.

    Depends on _get_element_by_id method of the project service and get_descendants
    method of the object class.
    """
    # Arrange -------------------------
    # Mock project service methods
    mocker.patch.object(
        sample_project_service, "change_object_position", return_value=None
    )

    # Get real ids
    object_id = SampleData.get(object_name)
    new_parent_id = SampleData.get(new_parent_name)

    # Act -----------------------------
    change_object_position_command = ChangeObjectPositionCommand(
        object_id, new_position, new_parent_id, sample_project_service
    )

    change_object_position_command.redo()

    # Assert --------------------------
    # Check project service method is called once with the correct arguments
    sample_project_service.change_object_position.assert_called_once_with(
        object_id, new_parent_id, new_position
    )


# --------------------------------------------------------------------------
# Integration tests
# --------------------------------------------------------------------------
# NOTE: Redo method heavily depends on the project service implementation.
#       Undo method is completely independent from the project service.
#       To test undo method completely, we create a black box integration test


@pytest.mark.parametrize(
    "object_name, new_parent_name, new_position",
    [
        ("simple_paragraph", "document_1", 1),
        ("simple_paragraph", "document_1", 2),
        ("simple_paragraph", "document_1", 8),
        ("simple_objective", "document_1", 0),
        (
            "simple_paragraph",
            "section_dl_1",
            None,
        ),
        (
            "simple_paragraph",
            "section_dl_1",
            0,
        ),
        (
            "simple_paragraph",
            "section_dl_1",
            1,
        ),
        (
            "simple_objective",
            "section_dl_1",
            None,
        ),
    ],
)
def test_change_object_position_command_undo(
    sample_project_service: ProjectService,
    object_name: str,
    new_parent_name: str,
    new_position: int,
):
    """
    Test that the undo method of the ChangeObjectPositionCommand class works
    as expected.

    Check that old and new parent states are restored to the previous state.
    Check that old and new parent descendants are restored to the previous order.
    """
    # Arrange -------------------------
    # Object
    object_id = SampleData.get(object_name)
    object = sample_project_service._get_element_by_id(object_id)
    old_parent = object.parent

    # New parent
    new_parent_id = SampleData.get(new_parent_name)
    new_parent = sample_project_service._get_element_by_id(new_parent_id)

    # Store old and new parent states
    old_parent_state = old_parent.state
    new_parent_state = new_parent.state

    # Store old and new parent descendants
    old_parent_descendants = old_parent.get_descendants().copy()
    new_parent_descendants = new_parent.get_descendants().copy()

    # Act -----------------------------
    change_object_position_command = ChangeObjectPositionCommand(
        object_id, new_position, new_parent_id, sample_project_service
    )

    change_object_position_command.redo()
    change_object_position_command.undo()

    # Assert --------------------------
    # Check old and new parent states are restored to the previous state
    assert (
        old_parent.state == old_parent_state
    ), f"Old parent state expected to be {old_parent_state} but was {old_parent.state}"
    assert (
        new_parent.state == new_parent_state
    ), f"New parent state expected to be {new_parent_state} but was {new_parent.state}"

    # Check old and new parent descendants are restored to the previous order
    assert (
        old_parent.get_descendants() == old_parent_descendants
    ), f"Old parent descendants expected to be {old_parent_descendants} but was {old_parent.get_descendants()}"
    assert (
        new_parent.get_descendants() == new_parent_descendants
    ), f"New parent descendants expected to be {new_parent_descendants} but was {new_parent.get_descendants()}"
