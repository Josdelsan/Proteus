# ==========================================================================
# File: test_create_project.py
# Description: pytest file for the PROTEUS pyqt create project use case
# Date: 13/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================


# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
import shutil

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtWidgets import QDialogButtonBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.tests import PROTEUS_SAMPLE_DATA_PATH
from proteus.utils.translator import Translator
from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.new_project_dialog import NewProjectDialog
from proteus.tests.end2end.fixtures import app, get_dialog

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "Aceptance test dummy empty project"
PROJECT_PATH = PROTEUS_SAMPLE_DATA_PATH

# --------------------------------------------------------------------------
# End to end "create project" tests
# --------------------------------------------------------------------------


def test_create_project(app):
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
    main_window: MainWindow = app

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

    # Open project button click
    create_project_button = main_window.main_menu.new_button
    dialog: NewProjectDialog = get_dialog(create_project_button.click)

    # Select empty-project archetype
    # NOTE: archetypes might be loaded in different order, this is a workaround
    # to select the correct archetype
    dialog._archetype_id = "empty-project"
    dialog.name_input.setText(PROJECT_NAME)
    dialog.path_input.setDirectory(str(PROJECT_PATH))
    dialog.accept_button.click()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check project folder creation
    assert os.path.exists(
        PROJECT_PATH / PROJECT_NAME
    ), f"Project folder {PROJECT_PATH / PROJECT_NAME} does not exist"

    # Check title changed to include project name
    assert (
        main_window.windowTitle() != old_window_title
    ), "Window title has not changed after project creation"
    assert (
        old_window_title in main_window.windowTitle()
    ), f"Window title does not include project name after project creation, '{main_window.windowTitle()}'"

    # Check central widget change to project container
    assert (
        main_window.centralWidget() != old_central_widget
    ), "Central widget has not changed after project creation"
    assert (
        main_window.centralWidget().__class__.__name__ == "ProjectContainer"
    ), f"Central widget is not a project container after project creation, '{main_window.centralWidget().__class__.__name__}'"

    # Check main menu buttons new state
    assert (
        main_window.main_menu.project_properties_button.isEnabled()
    ), "Project edit properties button is not enabled after project creation"
    assert (
        main_window.main_menu.add_document_button.isEnabled()
    ), "Add document button is not enabled after project creation"
    assert (
        main_window.main_menu.delete_document_button.isEnabled()
    ), "Delete document button is not enabled after project creation"
    assert (
        main_window.main_menu.export_document_button.isEnabled()
    ), "Export document button is not enabled after project creation"

    # Check documents container
    documents_container = main_window.project_container.documents_container
    assert (
        documents_container.__class__.__name__ == "DocumentsContainer"
    ), f"Documents container is not a DocumentsContainer, '{documents_container.__class__.__name__}'"

    # Check documents container tabs and tree chidlren correspond
    assert (
        documents_container.tabs.keys().__len__() == 1
    ), f"Documents container has not only one tab, number of tabs: '{documents_container.tabs.keys().__len__()}'"

    # Check each document tree has at least one tree item
    for document_tree in documents_container.tabs.values():
        assert (
            document_tree.__class__.__name__ == "DocumentTree"
        ), f"Document tree is not a DocumentTree, '{document_tree.__class__.__name__}'"
        assert (
            document_tree.tree_items.keys().__len__() >= 1
        ), f"Document tree has not at least one tree item, number of tree items: '{document_tree.tree_items.keys().__len__()}'"

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
        (PROJECT_PATH, "", "new_project_dialog.error.invalid_folder_name"),
        (PROJECT_PATH, None, "new_project_dialog.error.invalid_folder_name"),
        (PROJECT_PATH, "/test", "new_project_dialog.error.invalid_folder_name"),
        (PROJECT_PATH, "1:0test", "new_project_dialog.error.invalid_folder_name"),
        (PROJECT_PATH, "test?", "new_project_dialog.error.invalid_folder_name"),
        (
            PROJECT_PATH,
            "example_project",
            "new_project_dialog.error.folder_already_exists",
        ),  # Existing project
    ],
)
def test_create_project_negative(app, project_path, project_name, expected_error):
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
    main_window: MainWindow = app

    # Translator instace to translate error messages
    translator = Translator()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Open project button click
    create_project_button = main_window.main_menu.new_button
    dialog: NewProjectDialog = get_dialog(create_project_button.click)

    dialog.archetype_combo.setCurrentIndex(0)  # Select "empty project" archetype
    dialog.name_input.setText(project_name)
    dialog.path_input.setDirectory(str(project_path))
    dialog.accept_button.click()

    # --------------------------------------------
    # Assert
    # --------------------------------------------
    assert isinstance(
        dialog, NewProjectDialog
    ), f"Dialog is not a NewProjectDialog, '{dialog.__class__.__name__}'"

    assert dialog.error_label.text() == translator.text(expected_error), (
        f"Error label text is not the expected"
        f"current: '{dialog.error_label.text()}'"
        f"expected: '{translator.text(expected_error)}'"
    )
