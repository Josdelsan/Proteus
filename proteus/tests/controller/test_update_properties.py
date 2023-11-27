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

from proteus.model import ProteusID
from proteus.model.abstract_object import ProteusState
from proteus.model.properties import Property
from proteus.model.trace import Trace
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.services.project_service import ProjectService
from proteus.views.utils.event_manager import EventManager, Event
from proteus.controller.commands.update_properties import (
    UpdatePropertiesCommand,
)

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


@pytest.fixture
def mock_object(mocker):
    """
    Fixture to create a mock object. The object has two properties and two
    traces, its state is CLEAN.
    """
    # Create the mock object
    object_mock = mocker.MagicMock(spec=Object)
    object_mock.id = ProteusID("dummy_id")
    object_mock.properties = {}
    object_mock.traces = {}
    # Object state
    object_mock.state = ProteusState.CLEAN

    # Create mock properties
    property_1 = mocker.MagicMock(spec=Property)
    property_1.name = "property_1"
    property_2 = mocker.MagicMock(spec=Property)
    property_2.name = "property_2"
    for p in [property_1, property_2]:
        object_mock.properties[p.name] = p

    # Create mock traces
    trace_1 = mocker.MagicMock(spec=Trace)
    trace_1.name = "trace_1"
    trace_2 = mocker.MagicMock(spec=Trace)
    trace_2.name = "trace_2"
    for t in [trace_1, trace_2]:
        object_mock.traces[t.name] = t

    return object_mock


@pytest.fixture
def mock_project_service(mocker, mock_object):
    """
    Fixture to create a mock project service. Mocks the _get_element_by_id
    method to return the mock object fixture.
    """
    # Create the mock project service
    project_service_mock = mocker.MagicMock(spec=ProjectService)
    project_service_mock._get_element_by_id.return_value = mock_object
    project_service_mock.update_properties.return_value = None
    project_service_mock.update_traces.return_value = None

    return project_service_mock


# --------------------------------------------------------------------------
# Unit tests
# --------------------------------------------------------------------------
def test_update_properties_command_init_empty_properties(
    mock_object, mock_project_service
):
    """
    Test the initialization of the update properties command using an
    empty list as input
    """
    # Arrange --------------------
    # Create empty list
    new_properties = []

    # Act ------------------------
    # Create the update properties command
    update_properties_command = UpdatePropertiesCommand(
        ProteusID("dummy_id"), new_properties, mock_project_service
    )

    # Assert ---------------------
    # Check that the command has been created
    assert isinstance(
        update_properties_command, UpdatePropertiesCommand
    ), f"The command has not been created correctly, it should be an instance of {UpdatePropertiesCommand} \
        but it is an instance of {type(update_properties_command)}"

    # Check that traces and properties are empty lists
    assert (
        update_properties_command.new_properties == []
    ), f"The new properties list should be empty but it is {update_properties_command.new_properties}"
    assert (
        update_properties_command.new_traces == []
    ), f"The new traces list should be empty but it is {update_properties_command.new_traces}"

    # Check _get_element_by_id has been called once with the provided id
    mock_project_service._get_element_by_id.assert_called_once_with(
        ProteusID("dummy_id")
    )

    # Check that the element is the one provided
    assert (
        update_properties_command.element == mock_object
    ), f"The element should be {mock_object} but it is {update_properties_command.element}"


def test_update_properties_command_init(mocker, mock_object, mock_project_service):
    """
    Test the initialization of the update properties command, providing a list of properties
    and traces to modify the object. Check that the old properties and traces are correctly
    stored.
    """
    # Arrange --------------------
    # Create mock property and trace, using the same names as the mock object so they can be
    # found in the object and 'replaced'
    property_1 = mocker.MagicMock(spec=Property)
    property_1.name = "property_1"
    trace_1 = mocker.MagicMock(spec=Trace)
    trace_1.name = "trace_1"

    # New properties (and traces) list
    new_properties = [property_1, trace_1]

    # Act ------------------------
    # Create the update properties command
    update_properties_command = UpdatePropertiesCommand(
        ProteusID("dummy_id"), new_properties, mock_project_service
    )

    # Assert ---------------------
    # Check that the command has been created
    assert isinstance(
        update_properties_command, UpdatePropertiesCommand
    ), f"The command has not been created correctly, it should be an instance of {UpdatePropertiesCommand} \
        but it is an instance of {type(update_properties_command)}"

    # Check that the new properties and traces are the ones provided
    assert update_properties_command.new_properties == [
        property_1
    ], f"The new properties list should be {property_1} but it is {update_properties_command.new_properties}"
    assert update_properties_command.new_traces == [
        trace_1
    ], f"The new traces list should be {trace_1} but it is {update_properties_command.new_traces}"

    # Check _get_element_by_id has been called once with the provided id
    mock_project_service._get_element_by_id.assert_called_once_with(
        ProteusID("dummy_id")
    )

    # Check that the element is the one provided
    assert (
        update_properties_command.element == mock_object
    ), f"The element should be {mock_object} but it is {update_properties_command.element}"

    # Check that the old properties and traces are the ones provided
    assert update_properties_command.old_properties == [
        mock_object.properties["property_1"]
    ], f"The old properties list should be {mock_object.properties['property_1']} but it is {update_properties_command.old_properties}"
    assert update_properties_command.old_traces == [
        mock_object.traces["trace_1"]
    ], f"The old traces list should be {mock_object.traces['trace_1']} but it is {update_properties_command.old_traces}"


def test_update_properties_command_redo(mocker, mock_object, mock_project_service):
    """
    Test the redo method of the update properties command for an object. Check that the
    project service method are called correctly.
    """
    # Arrange --------------------
    # Mock EventManager notify method
    mocker.patch.object(EventManager, "notify")

    # Act ------------------------
    # Create the update properties command
    update_properties_command = UpdatePropertiesCommand(
        ProteusID("dummy_id"), [], mock_project_service
    )

    # Call the redo method
    update_properties_command.redo()

    # Assert ---------------------
    # Check that the project service update_properties method has been called once
    mock_project_service.update_properties.assert_called_once_with(mock_object.id, [])

    # Check that the project service update_traces method has been called once
    mock_project_service.update_traces.assert_called_once_with(mock_object.id, [])

    # Check that the event manager notify method has been called once with the correct event
    EventManager().notify.assert_called_once_with(
        event=Event.MODIFY_OBJECT, element_id=mock_object.id
    )


def test_update_properties_command_undo(mocker, mock_object, mock_project_service):
    """
    Test the redo method of the update properties command for an object. Check that the
    project service method are called correctly.
    """
    # Arrange --------------------
    # Mock EventManager notify method
    mocker.patch.object(EventManager, "notify")

    # Act ------------------------
    # Create the update properties command
    update_properties_command = UpdatePropertiesCommand(
        ProteusID("dummy_id"), [], mock_project_service
    )

    # Call the redo method
    update_properties_command.undo()

    # Assert ---------------------
    # Check that the project service update_properties method has been called once
    mock_project_service.update_properties.assert_called_once_with(
        mock_object.id, update_properties_command.old_properties
    )

    # Check that the project service update_traces method has been called once
    mock_project_service.update_traces.assert_called_once_with(
        mock_object.id, update_properties_command.old_traces
    )

    # Check that the event manager notify method has been called once with the correct event
    EventManager().notify.assert_called_once_with(
        event=Event.MODIFY_OBJECT, element_id=mock_object.id
    )


def test_update_properties_command_redo_project(mocker, mock_project_service):
    """
    Test the redo method of the update properties command for a project. Check that the
    project service method are called correctly.

    Update traces should not be called for a project.
    """
    # Arrange --------------------
    # Create the mock project
    project_mock = mocker.MagicMock(spec=Project)
    project_mock.id = ProteusID("dummy_id")
    project_mock.properties = {}
    project_mock.traces = {}
    # Project state
    project_mock.state = ProteusState.CLEAN

    # Mock the _get_element_by_id method to return the mock project
    mock_project_service._get_element_by_id.return_value = project_mock

    # Mock EventManager notify method
    mocker.patch.object(EventManager, "notify")

    # Act ------------------------
    # Create the update properties command
    update_properties_command = UpdatePropertiesCommand(
        ProteusID("dummy_id"), [], mock_project_service
    )

    # Call the redo method
    update_properties_command.redo()

    # Assert ---------------------
    # Check that the project service update_properties method has been called once
    mock_project_service.update_properties.assert_called_once_with(project_mock.id, [])

    # Check that the project service update_traces method has not been called
    mock_project_service.update_traces.assert_not_called()

    # Check that the event manager notify method has been called once with the correct event
    EventManager().notify.assert_called_once_with(
        event=Event.MODIFY_OBJECT, element_id=project_mock.id
    )


def test_update_properties_command_undo_project(mocker, mock_project_service):
    """
    Test the redo method of the update properties command for a project. Check that the
    project service method are called correctly.

    Update traces should not be called for a project.
    """
    # Arrange --------------------
    # Create the mock project
    project_mock = mocker.MagicMock(spec=Project)
    project_mock.id = ProteusID("dummy_id")
    project_mock.properties = {}
    project_mock.traces = {}
    # Project state
    project_mock.state = ProteusState.CLEAN

    # Mock the _get_element_by_id method to return the mock project
    mock_project_service._get_element_by_id.return_value = project_mock

    # Mock EventManager notify method
    mocker.patch.object(EventManager, "notify")

    # Act ------------------------
    # Create the update properties command
    update_properties_command = UpdatePropertiesCommand(
        ProteusID("dummy_id"), [], mock_project_service
    )

    # Call the redo method
    update_properties_command.undo()

    # Assert ---------------------
    # Check that the project service update_properties method has been called once
    mock_project_service.update_properties.assert_called_once_with(
        project_mock.id, update_properties_command.old_properties
    )

    # Check that the project service update_traces method has not been called
    mock_project_service.update_traces.assert_not_called()

    # Check that the event manager notify method has been called once with the correct event
    EventManager().notify.assert_called_once_with(
        event=Event.MODIFY_OBJECT, element_id=project_mock.id
    )
