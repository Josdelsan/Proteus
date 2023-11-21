# ==========================================================================
# File: test_open_project.py
# Description: pytest file for the PROTEUS pyqt main window
# Date: 11/08/2023
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

from PyQt6.QtCore import QTimer

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.tests import PROTEUS_SAMPLE_DATA_PATH
from proteus.views.main_window import MainWindow
from proteus.tests.end2end.fixtures import app

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

SAMPLE_PROJECT_PATH = PROTEUS_SAMPLE_DATA_PATH / "example_project"


# --------------------------------------------------------------------------
# End to end "open project" tests
# --------------------------------------------------------------------------


def test_open_project(mocker, app):
    """
    Test the open project use case. Opens a project with documents and objects.
    It tests the following:
        - The main window title changes to include the project name
        - The main window central widget changes to a ProjectContainer
        - The expected buttons become enabled/disabled
        - Documents container is created and populated
        - Document trees are created and populated
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    # Mock the QFileDialog response and handle the dialog life cycle
    mocker.patch(
        "PyQt6.QtWidgets.QFileDialog.getExistingDirectory",
        return_value=str(SAMPLE_PROJECT_PATH),
    )

    def handle_dialog():
        dialog = main_window.main_menu.directory_dialog
        while not dialog:
            dialog = main_window.main_menu.directory_dialog
        dialog.close()
        dialog.deleteLater()

    # Store previous information
    old_window_title = main_window.windowTitle()
    old_central_widget = main_window.centralWidget()

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Open project button click
    open_project_button = main_window.main_menu.open_button
    QTimer.singleShot(5, handle_dialog)  # Wait for the dialog to be created
    open_project_button.click()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check title changed to include project name
    assert (
        main_window.windowTitle() != old_window_title
    ), f"Expected window title to change from {old_window_title}"
    assert old_window_title in main_window.windowTitle(), (
        f"Expected window title to include {old_window_title} as prefix"
        f"current title {main_window.windowTitle()}"
    )

    # Check central widget change to project container
    assert (
        main_window.centralWidget() != old_central_widget
    ), "Central widget should have been deleted and replaced by a new one"
    assert (
        main_window.centralWidget().__class__.__name__ == "ProjectContainer"
    ), f"Expected central widget to be a ProjectContainer, got {main_window.centralWidget().__class__.__name__}"

    # Check main menu buttons new state
    assert (
        main_window.main_menu.project_properties_button.isEnabled()
    ), "Expected edit project properties button to be enabled"
    assert (
        main_window.main_menu.add_document_button.isEnabled()
    ), "Expected add document button to be enabled"
    assert (
        main_window.main_menu.delete_document_button.isEnabled()
    ), "Expected delete document button to be enabled"
    assert (
        main_window.main_menu.export_document_button.isEnabled()
    ), "Expected export document button to be enabled"

    # Check documents container
    documents_container = main_window.project_container.documents_container
    assert (
        documents_container.__class__.__name__ == "DocumentsContainer"
    ), f"Expected documents container to be a DocumentsContainer, got {documents_container.__class__.__name__}"

    # Check documents container tabs and tree chidlren correspond
    assert (
        documents_container.tabs.keys().__len__() == 4
    ), f"Expected 3 tabs, got {documents_container.tabs.keys().__len__()}"

    # Check each document tree has at least one tree item
    for document_tree in documents_container.tabs.values():
        assert (
            document_tree.__class__.__name__ == "DocumentTree"
        ), f"Expected document tree to be a DocumentTree, got {document_tree.__class__.__name__}"
        assert (
            document_tree.tree_items.keys().__len__() >= 1
        ), f"Expected at least one tree item, got {document_tree.tree_items.keys().__len__()}"


