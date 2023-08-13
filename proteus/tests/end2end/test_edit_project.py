# ==========================================================================
# File: test_edit_project.py
# Description: pytest file for the PROTEUS pyqt edit project use case
# Date: 13/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/37
# QApplication instace cannot be deleted. This might cause tests failures.

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/256
# Dialog handling can interfere with running tests together. Workaround
# listed in the issue with 5ms delay in QTimer seems to work. Since
# dialogs are an important part of the app, this might be a problem
# in the future. No complete solution found yet.

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialogButtonBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.main_window import MainWindow
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# End to end "edit project" tests
# --------------------------------------------------------------------------


def test_edit_project(qtbot, app):
    """
    Test the edit project use case. Edit an existing project changing its
    name and other properties. It tests the following steps:
        - Open the edit project dialog
        - Fill the form (name change)
        - Check project name change
        - Check dialog properties change
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app.activeWindow()

    load_project(main_window=main_window)

    # Store previous title
    old_window_title = main_window.windowTitle()

    # Properties
    # NOTE: These are known existing properties
    NAME_PROP = "name"
    VERSION_PROP = "version"
    DESCRIPTION_PROP = "description"

    # old name value
    old_name = None

    # New values
    new_name = "New name"
    new_version = "New version"
    new_description = "New description"

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Handle form filling
    def handle_dialog():
        dialog: PropertyDialog = main_window.current_dialog
        while not dialog:
            dialog = main_window.current_dialog

        # Get old name
        nonlocal old_name
        old_name = dialog.input_widgets[NAME_PROP].get_value()

        # Change properties
        # NOTE: inputs types are known so we can use setText and setPlainText
        dialog.input_widgets[NAME_PROP].input.setText(new_name)
        dialog.input_widgets[VERSION_PROP].input.setText(new_version)
        dialog.input_widgets[DESCRIPTION_PROP].input.setPlainText(new_description)

        # Accept dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()

    # Open project button click
    edit_project_button = main_window.main_menu.project_properties_button
    QTimer.singleShot(5, handle_dialog)  # Wait for the dialog to be created
    qtbot.mouseClick(edit_project_button, Qt.MouseButton.LeftButton)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Variable to store current values
    # NOTE: Assertion cannot be done in nested functions
    current_name = None
    current_version = None
    current_description = None

    def handle_dialog_assert():
        dialog: PropertyDialog = main_window.current_dialog
        while not dialog:
            dialog = main_window.current_dialog

        # Check properties changed
        nonlocal current_name, current_version, current_description
        current_name = dialog.input_widgets[NAME_PROP].get_value()
        current_version = dialog.input_widgets[VERSION_PROP].get_value()
        current_description = dialog.input_widgets[DESCRIPTION_PROP].get_value()
        # Close the dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Cancel).click()

    # Access properties post edit
    QTimer.singleShot(5, handle_dialog_assert)  # Wait for the dialog to be created
    qtbot.mouseClick(edit_project_button, Qt.MouseButton.LeftButton)

    # Check title changed to replace old project name
    assert main_window.windowTitle() == old_window_title.replace(old_name, new_name)

    # Check main menu buttons new state
    assert main_window.main_menu.save_button.isEnabled()

    # Check properties changed
    assert current_name == new_name
    assert current_version == new_version
    assert current_description == new_description


