# ==========================================================================
# File: test_edit_document.py
# Description: pytest file for the PROTEUS pyqt edit document use case
# Date: 15/08/2023
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
from PyQt6.QtWidgets import QDialogButtonBox, QTreeWidgetItem, QTreeWidget, QApplication

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "one_doc_project"
DOCUMENT_ID = "3fKhMAkcEe2C"  # Known document id from one_doc_project

# --------------------------------------------------------------------------
# End to end "edit document" tests
# --------------------------------------------------------------------------


def test_edit_document(app):
    """
    Test the edit document use case. Edit an existing document changing its
    name and acronym. It tests the following steps:
        - Open the edit document dialog
        - Fill the form (acronym change)
        - Check the acronym changed in the tab
        - Check dialog properties change
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window, project_name=PROJECT_NAME)

    # Properties
    # NOTE: These are known existing properties
    NAME_PROP = "name"
    ACRONYM_PROP = "acronym"

    # New values
    new_name = "New name"
    new_acronym = "ACRO"

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Handle form filling
    def handle_dialog():
        dialog: PropertyDialog = QApplication.activeModalWidget()
        while not dialog:
            dialog = QApplication.activeModalWidget()

        # Change properties
        # NOTE: inputs types are known so we can use setText
        dialog.input_widgets[NAME_PROP].input.setText(new_name)
        dialog.input_widgets[ACRONYM_PROP].input.setText(new_acronym)

        # Accept dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()

    # Edit document button, double click in the tree item
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )
    document_tree: DocumentTree = documents_container.tabs[
        DOCUMENT_ID
    ]
    doc_tree_element: QTreeWidgetItem = documents_container.tabs[
        DOCUMENT_ID
    ].tree_items[DOCUMENT_ID]

    # Wait for the dialog to be created
    QTimer.singleShot(5, handle_dialog)
    # Double click in the tree item cannot be done using qbot
    document_tree.itemDoubleClicked.emit(doc_tree_element, 0)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Variable to store current values
    # NOTE: Assertion cannot be done in nested functions
    current_name = None
    current_acronym = None

    def handle_dialog_assert():
        dialog: PropertyDialog = QApplication.activeModalWidget()
        while not dialog:
            dialog = QApplication.activeModalWidget()

        # Check properties changed
        nonlocal current_name, current_acronym
        current_name = dialog.input_widgets[NAME_PROP].get_value()
        current_acronym = dialog.input_widgets[ACRONYM_PROP].get_value()
        # Close the dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Cancel).click()

    # Access properties post edit
    QTimer.singleShot(5, handle_dialog_assert)  # Wait for the dialog to be created
    # Double click in the tree item cannot be done using qbot
    document_tree.itemDoubleClicked.emit(doc_tree_element, 0)

    # Check properties changed
    assert (
        current_name == new_name
    ), f"Project name must be '{new_name}' but it is '{current_name}'"
    assert (
        current_acronym == new_acronym
    ), f"Project acronym must be '{new_acronym}' but it is '{current_acronym}'"

    # Check the QTreeWidgetItem name changed
    assert (
        doc_tree_element.text(0) == new_name
    ), f"Document tree item name must be '{new_name}' but it is '{doc_tree_element.text(0)}'"

    # Check tab acronym changed
    assert (
        documents_container.tabBar().tabText(0) == new_acronym
    ), f"Document tab acronym must be '{new_acronym}' but it is '{documents_container.tabBar().tabText(0)}'"
