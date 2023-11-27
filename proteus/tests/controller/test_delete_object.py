# ==========================================================================
# File: test_update_properties.py
# Description: pytest file for the PROTEUS update properties command
# Date: 27/11/2023
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

from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.views.utils.state_manager import StateManager
from proteus.controller.commands.delete_object import DeleteObjectCommand
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
@pytest.mark.parametrize(
    "object_name, expected_update_traces_calls",
    [
        ("simple_paragraph", 0),
        ("section_dl_1", 0),
        ("section_dl_2", 0),
        ("target_with_2_sources_1", 2),
        ("section_with_2_children_targeted", 2), # Should not count sources inside the section
    ],
)
def test_update_properties_command_redo(
    mocker, sample_project_service: ProjectService, object_name, expected_update_traces_calls
):
    """
    Test that the redo method of the UpdatePropertiesCommand class works as
    expected.

    Parametrized with multiple objects to test different children depths and
    traces dependencies.
    """
    # Arrange -------------------------
    object_id = SampleData.get(object_name)

    # Store ids of the object and its children to check their state later
    object = sample_project_service._get_element_by_id(object_id)
    ids = object.get_ids()

    # Mock the update_traces method to check if it has been called
    mocker.patch.object(sample_project_service, "update_traces")

    # Mock state manager to check if deselect object has been called
    mocker.patch.object(StateManager, "deselect_object")

    # Act -----------------------------
    delete_object_command = DeleteObjectCommand(object_id, sample_project_service)

    delete_object_command.redo()

    # Assert --------------------------
    # Check all states are DEAD
    assert all(
        [
            sample_project_service._get_element_by_id(id).state == ProteusState.DEAD
            for id in ids
        ]
    ), "All objects states must be DEAD"

    # Check parent state is DIRTY
    assert (
        object.parent.state == ProteusState.DIRTY
    ), f"Parent object state must be DIRTY but it is {object.parent.state}"

    # Check that the update_traces method has been called the expected number
    # of times
    assert (
        sample_project_service.update_traces.call_count == expected_update_traces_calls
    ), f"Trace.update_traces method has been called {sample_project_service.update_traces.call_count} times but it should be called {expected_update_traces_calls} times"

    # Check that the deselect_object method has been called
    StateManager().deselect_object.assert_called_once_with(object_id)
