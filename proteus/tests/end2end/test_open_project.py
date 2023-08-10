# ==========================================================================
# File: test_open_project.py
# Description: pytest file for the PROTEUS pyqt main window
# Date: 11/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/37
# QApplication instace cannot be deleted. This causes subsequent tests
# to fail. It also occurs with the main window instance. Due to the
# nature of the end2end tests, they will be executed manually.

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QPushButton

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.tests import PROTEUS_TEST_SAMPLE_DATA_PATH
from proteus.views.main_window import MainWindow
from proteus.tests.end2end.fixtures import app

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

SAMPLE_PROJECT_PATH = PROTEUS_TEST_SAMPLE_DATA_PATH / "example_project"


# --------------------------------------------------------------------------
# End to end "open project" tests
# --------------------------------------------------------------------------


# NOTE: This test is skipped because it must be executed manually
# (see the note at the top of this file)
@pytest.mark.skip
def test_open_project(qtbot, mocker, app):
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
    main_window: MainWindow = app.activeWindow()

    # Mock the QFileDialog response and handle the dialog life cycle
    mocker.patch(
        "PyQt6.QtWidgets.QFileDialog.getExistingDirectory",
        return_value=str(SAMPLE_PROJECT_PATH),
    )

    def handle_dialog():
        main_window.main_menu.directory_dialog.close()
        main_window.main_menu.directory_dialog.deleteLater()

    # Store previous information
    old_window_title = main_window.windowTitle()
    old_central_widget = main_window.centralWidget()

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Open project button click
    open_project_button = main_window.main_menu.open_button
    QTimer.singleShot(1000, handle_dialog)  # Wait for the dialog to be created
    qtbot.mouseClick(open_project_button, Qt.MouseButton.LeftButton)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

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
    assert documents_container.tabs.keys().__len__() == 3
    assert documents_container.tabs.keys() == documents_container.tab_children.keys()

    # Check each document tree has at least one tree item
    for document_tree in documents_container.tab_children.values():
        assert document_tree.__class__.__name__ == "DocumentTree"
        assert document_tree.tree_items.keys().__len__() >= 1