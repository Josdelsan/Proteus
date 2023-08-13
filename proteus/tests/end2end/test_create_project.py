# ==========================================================================
# File: test_create_project.py
# Description: pytest file for the PROTEUS pyqt create project use case
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

import os
import shutil

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialogButtonBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.tests import PROTEUS_TEST_SAMPLE_DATA_PATH
from proteus.views.main_window import MainWindow
from proteus.views.components.dialogs.new_project_dialog import NewProjectDialog
from proteus.tests.end2end.fixtures import app

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "Aceptance test dummy empty project"
PROJECT_PATH = PROTEUS_TEST_SAMPLE_DATA_PATH

# --------------------------------------------------------------------------
# End to end "create project" tests
# --------------------------------------------------------------------------

def test_create_project(qtbot, app):
    """
    Test the create project use case. Create a project from an archetype and open it
    automatically. It tests the following steps:
        - Open the create project dialog
        - Fill the form
        - Project creation/load
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app.activeWindow()

    # Check if the project already exists and delete it
    # NOTE: This is a workaround if the test fails and the project is not deleted
    if os.path.exists(PROJECT_PATH / PROJECT_NAME):
        shutil.rmtree(PROJECT_PATH / PROJECT_NAME)


    # Store previous information to check project opening
    old_window_title = main_window.windowTitle()
    old_central_widget = main_window.centralWidget()

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Handle form filling
    def handle_dialog():
        dialog: NewProjectDialog = main_window.current_dialog
        while not dialog:
            dialog = main_window.current_dialog
        
        dialog.archetype_combo.setCurrentIndex(0) # Select "empty project" archetype
        dialog.name_input.setText(PROJECT_NAME)
        dialog.path_input.setText(str(PROJECT_PATH))
        dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()


    # Open project button click
    create_project_button = main_window.main_menu.new_button
    QTimer.singleShot(5, handle_dialog)  # Wait for the dialog to be created
    qtbot.mouseClick(create_project_button, Qt.MouseButton.LeftButton)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check project folder creation
    assert os.path.exists(PROJECT_PATH / PROJECT_NAME)

    # Check title changed to include project name
    assert main_window.windowTitle() != old_window_title
    assert old_window_title in main_window.windowTitle()

    # Check central widget change to project container
    assert main_window.centralWidget() != old_central_widget
    assert main_window.centralWidget().__class__.__name__ == "ProjectContainer"

    # Check main menu buttons new state
    assert main_window.main_menu.project_properties_button.isEnabled()
    assert main_window.main_menu.add_document_button.isEnabled()
    assert main_window.main_menu.delete_document_button.isEnabled()
    assert main_window.main_menu.export_document_button.isEnabled()

    # Check documents container
    documents_container = main_window.project_container.documents_container
    assert documents_container.__class__.__name__ == "DocumentsContainer"

    # Check documents container tabs and tree chidlren correspond
    assert documents_container.tabs.keys().__len__() == 1
    assert documents_container.tabs.keys() == documents_container.tab_children.keys()

    # Check each document tree has at least one tree item
    for document_tree in documents_container.tab_children.values():
        assert document_tree.__class__.__name__ == "DocumentTree"
        assert document_tree.tree_items.keys().__len__() >= 1

    # --------------------------------------------
    # Teardown
    # --------------------------------------------
    if os.path.exists(PROJECT_PATH / PROJECT_NAME):
        # Chdir is changed during project loading, so we need to change it back
        # to avoid permission errors
        os.chdir(PROJECT_PATH)
        shutil.rmtree(PROJECT_PATH / PROJECT_NAME)


@pytest.mark.parametrize(
    "project_path, project_name, expected_error",
    [
        ("", "Project name", "new_project_dialog.error.invalid_path"),
        (None, "Project name", "new_project_dialog.error.invalid_path"),
        (PROJECT_PATH, "", "new_project_dialog.error.invalid_name"),
        (PROJECT_PATH, None, "new_project_dialog.error.invalid_name"),
        (PROJECT_PATH, "example_project", "new_project_dialog.error.folder_already_exists"), # Existing project
    ],
)
def test_create_project_negative(qtbot, app, project_path, project_name, expected_error):
    """
    Test the ocreate project use case. Create a project from an archetype and open it
    automatically. It tests the following steps:
        - Open the create project dialog
        - Fill the form
        - Project creation/load

    NOTE: Archetype combo is not tested because it is not possible to select an invalid
    archetype.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app.activeWindow()

    # Translator instace to translate error messages
    translator = main_window.translator

    # Variables to later checking
    # NOTE: Assertions cannot be done inside nested functions
    dialog: NewProjectDialog = None
    error_label_text = None
    
    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Handle form filling
    def handle_dialog():
        nonlocal dialog, error_label_text
        while not dialog:
            dialog = main_window.current_dialog

        dialog.archetype_combo.setCurrentIndex(0) # Select "empty project" archetype
        dialog.name_input.setText(project_name)
        dialog.path_input.setText(str(project_path))
        dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()

        # Store error label text
        error_label_text = dialog.error_label.text()

        # Close the dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Cancel).click()

    # Open project button click
    create_project_button = main_window.main_menu.new_button
    QTimer.singleShot(5, handle_dialog)  # Wait for the dialog to be created
    qtbot.mouseClick(create_project_button, Qt.MouseButton.LeftButton)

    # --------------------------------------------
    # Assert
    # --------------------------------------------
    assert isinstance(dialog, NewProjectDialog)
    assert dialog.error_label.text() == translator.text(expected_error)