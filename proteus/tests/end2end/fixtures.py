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

from typing import Callable
import pytest
import time
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import QTimer

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.tests import PROTEUS_SAMPLE_DATA_PATH
from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.utils.state_manager import StateManager
from proteus.controller.command_stack import Controller

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

TEST_PROJECT_NAME = "example_project"

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/37
# QApplication instace cannot be deleted. This might cause tests failures.

@pytest.fixture(scope="function")
def app(qtbot, mocker):
    """
    Handle the creation of the QApplication instance and the main window.
    """
    # NOTE: Its important to restore the singleton instances when
    # running tests together, otherwise stored information might
    # screw up the tests
    restore_app_singleton_instances()

    # Call the mock_views_container function to mock the ViewsContainer methods
    mock_views_container(mocker)

    # Create the main window
    main_window = MainWindow(parent=None, controller=Controller())

    # Mock closeEvent to avoid the dialog asking for saving the project
    main_window.closeEvent = lambda event: event.accept()
    main_window.show()
    qtbot.addWidget(main_window)

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
        "proteus.views.components.views_container.ViewsContainer.update_view",
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


# NOTE: https://github.com/pytest-dev/pytest-qt/issues/256
# Dialog handling can interfere with running tests together. Workaround
# listed in the issue with 5ms delay in QTimer seems to work. Since
# dialogs are an important part of the app, this might be a problem
# in the future. No complete solution found yet.
    
def get_dialog(dialog_trigger: Callable, time_out: int = 5) -> QDialog:
    """
    Returns the current dialog (active modal widget). If there is no
    dialog, it waits until one is created for a maximum of 5 seconds (by
    default).

    This function is multithreaded, it creates a thread to get the dialog
    instance and hide it so it does not interrupt the tests execution. Main
    thread continues executing waiting for the dialog instance to be created.
    Timeout applies to both threads.

    :param dialog_trigger: Callable that triggers the dialog creation.
    :param time_out: Maximum time (seconds) to wait for the dialog creation.
    """

    dialog: QDialog = None
    start_time = time.time()

    # Helper function to catch the dialog instance and hide it
    def dialog_creation():
        # Wait for the dialog to be created or timeout
        nonlocal dialog
        while dialog is None and time.time() - start_time < time_out:
            dialog = QApplication.activeModalWidget()

        # Avoid errors when dialog is not created
        if dialog is not None:
            # Hide dialog to avoid interrupting the tests execution
            # It has the same effect as close()
            dialog.hide()

    # Create a thread to get the dialog instance and call dialog_creation trigger
    QTimer.singleShot(1, dialog_creation)  
    dialog_trigger()

    # Wait for the dialog to be created or timeout
    while dialog is None and time.time() - start_time < time_out:
        continue

    assert isinstance(
        dialog, QDialog
    ), f"No dialog was created after {time_out} seconds. Dialog type: {type(dialog)}"

    return dialog


def get_context_menu(dialog_trigger: Callable, time_out: int = 5) -> ContextMenu:
    """
    Returns the current context menu (active popup widget). If there is no
    context menu, it waits until one is created for a maximum of 5 seconds (by
    default).

    This function is multithreaded, it creates a thread to get the context menu
    instance and hide it so it does not interrupt the tests execution. Main
    thread continues executing waiting for the context menu instance to be created.
    Timeout applies to both threads.

    :param dialog_trigger: Callable that triggers the context menu creation.
    :param time_out: Maximum time (seconds) to wait for the context menu creation.
    """

    context_menu: ContextMenu = None
    start_time = time.time()

    # Helper function to catch the context menu instance and hide it
    def context_menu_creation():
        # Wait for the context menu to be created or timeout
        nonlocal context_menu
        while context_menu is None and time.time() - start_time < time_out:
            context_menu = QApplication.activePopupWidget()

        # Avoid errors when context menu is not created
        if context_menu is not None:
            # Hide context menu to avoid interrupting the tests execution
            # It has the same effect as close()
            context_menu.hide()

    # Create a thread to get the context menu instance and call context_menu_creation trigger
    QTimer.singleShot(1, context_menu_creation)  
    dialog_trigger()

    # Wait for the context menu to be created or timeout
    while context_menu is None and time.time() - start_time < time_out:
        continue

    assert isinstance(
        context_menu, ContextMenu
    ), f"No context menu was created after {time_out} seconds. Context menu type: {type(context_menu)}"

    return context_menu