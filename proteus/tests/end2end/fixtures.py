# ==========================================================================
# File: fixtures.py
# Description: pytest fixtures for end2end testing PROTEUS
# Date: 12/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/37
# QApplication instace cannot be deleted. This causes subsequent tests
# to fail (in the same module). qtbot fixture forces function scope.
# If parametrization is used or multiple tests are in the same module,
# they must be executed manually one by one.

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtWidgets import QApplication

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.tests import PROTEUS_SAMPLE_DATA_PATH
from proteus.views.components.main_window import MainWindow
from proteus.utils.event_manager import EventManager
from proteus.utils.state_manager import StateManager
from proteus.controller.command_stack import Controller

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

TEST_PROJECT_NAME = "example_project"

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


@pytest.fixture(scope="function")
def app(qtbot, mocker):
    """
    Handle the creation of the QApplication instance and the main window.
    """
    # NOTE: Its important to restore the singleton instances when
    # running tests together, otherwise stores information might
    # screw up the tests
    restore_app_singleton_instances()

    # Call the mock_views_container function to mock the ViewsContainer methods
    mock_views_container(mocker)

    # Create the main window
    main_window = MainWindow(parent=None, controller=Controller())
    
    # Mock closeEvent to avoid the dialog asking for saving the project
    main_window.closeEvent = lambda event: event.accept()
    main_window.show()
    qtbot.addWidget(main_window) # Cannot use waitExposed with addWidget

    # Return the main window when it is exposed
    with qtbot.waitExposed(main_window):
        return main_window



def load_project(
    main_window: MainWindow,
    project_path: str = PROTEUS_SAMPLE_DATA_PATH,
    project_name: str = TEST_PROJECT_NAME,
):
    """
    Handle the creation of the app and example project opening.

    By default, 'example_project' is loaded.

    NOTE: Avoids opening the project using the dialog. Instead, uses
    the controller method directly.
    """
    controller: Controller = main_window._controller

    # Open the example project
    controller.load_project(f"{project_path}/{project_name}")


def restore_app_singleton_instances():
    """
    Restores the singleton instances of the app.
    """
    EventManager().clear()
    StateManager().current_document = None
    StateManager().current_object = {}
    StateManager().current_view = None


def mock_views_container(mocker):
    """
    Mocks ViewsContainer methods to avoid the creation of the QWebEngineView
    and QWebEnginePage instances. This is necessary because the QWebEngineView
    class is not supported by the pytest-qt plugin.
    """

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.create_component",
        lambda *args, **kwargs: None,
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_component",
        lambda *args, **kwargs: None,
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.delete_component",
        lambda *args, **kwargs: None,
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_on_add_view",
        lambda *args, **kwargs: None,
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_on_select_object",
        lambda *args, **kwargs: None,
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_on_delete_view",
        lambda *args, **kwargs: None,
    )
