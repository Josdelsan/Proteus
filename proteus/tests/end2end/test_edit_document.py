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

from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import QPoint

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME, PROTEUS_ACRONYM
from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import (
    app,
    load_project,
    get_dialog,
    get_context_menu,
)

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

DOCUMENT_ID = SampleData.get("document_1")

# --------------------------------------------------------------------------
# End to end "edit document" tests
# --------------------------------------------------------------------------


def test_edit_document(app):
    """
    Test the edit document use case. Edit an existing document changing its
    name and acronym. It tests the following steps:
        - Open the edit document dialog (double click)
        - Fill the form (acronym change)

    Checks:
        - Acronym changed in the tab
        - Dialog properties change
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Properties
    # NOTE: These are known existing properties
    NAME_PROP = PROTEUS_NAME
    ACRONYM_PROP = PROTEUS_ACRONYM

    # New values
    new_name = "New name"
    new_acronym = "ACRO"

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Edit document button, double click in the tree item
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )
    document_tree: DocumentTree = documents_container.tabs[DOCUMENT_ID]
    doc_tree_element: QTreeWidgetItem = document_tree.tree_items[DOCUMENT_ID]

    # Create dialog
    dialog: PropertyDialog = get_dialog(
        lambda: document_tree.itemDoubleClicked.emit(doc_tree_element, 0)
    )

    # Change properties
    # NOTE: inputs types are known so we can use setText
    dialog.input_widgets[NAME_PROP].input.setText(new_name)
    dialog.input_widgets[ACRONYM_PROP].input.setText(new_acronym)

    # Accept dialog
    dialog.accept_button.click()
    dialog.deleteLater()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Get dialog again
    assert_dialog: PropertyDialog = get_dialog(
        lambda: document_tree.itemDoubleClicked.emit(doc_tree_element, 0)
    )

    # Check properties changed
    current_name = assert_dialog.input_widgets[NAME_PROP].get_value()
    current_acronym = assert_dialog.input_widgets[ACRONYM_PROP].get_value()

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

    # Get tabbar index
    tab_index = documents_container.indexOf(document_tree)

    # Check tab acronym changed
    assert (
        documents_container.tabBar().tabText(tab_index) == new_acronym
    ), f"Document tab acronym must be '{new_acronym}' but it is '{documents_container.tabBar().tabText(tab_index)}'"


def test_edit_document_contextmenu(app):
    """
    Test the edit document use case using context menu button. Edit an existing document changing its
    name and acronym. It tests the following steps:
        - Open the edit document dialog
        - Fill the form (acronym change)

    Checks:
        - Acronym changed in the tab
        - Dialog properties change
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Properties
    # NOTE: These are known existing properties
    NAME_PROP = PROTEUS_NAME
    ACRONYM_PROP = PROTEUS_ACRONYM

    # New values
    new_name = "New name"
    new_acronym = "ACRO"

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Edit document button, double click in the tree item
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    document_tree: DocumentTree = documents_container.tabs[DOCUMENT_ID]
    doc_tree_element: QTreeWidgetItem = document_tree.tree_items[DOCUMENT_ID]
    document_tree.itemPressed.emit(doc_tree_element, 0)

    # Trigger context menu
    element_position: QPoint = document_tree.visualItemRect(doc_tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    # Create dialog
    dialog: PropertyDialog = get_dialog(context_menu.action_edit_object.trigger)

    # Change properties
    # NOTE: inputs types are known so we can use setText
    dialog.input_widgets[NAME_PROP].input.setText(new_name)
    dialog.input_widgets[ACRONYM_PROP].input.setText(new_acronym)

    # Accept dialog
    dialog.accept_button.click()
    dialog.deleteLater()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Trigger context menu
    element_position: QPoint = document_tree.visualItemRect(doc_tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    # Create dialog
    assert_dialog: PropertyDialog = get_dialog(context_menu.action_edit_object.trigger)

    # Check properties changed
    current_name = assert_dialog.input_widgets[NAME_PROP].get_value()
    current_acronym = assert_dialog.input_widgets[ACRONYM_PROP].get_value()

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

    # Get tabbar index
    tab_index = documents_container.indexOf(document_tree)

    # Check tab acronym changed
    assert (
        documents_container.tabBar().tabText(tab_index) == new_acronym
    ), f"Document tab acronym must be '{new_acronym}' but it is '{documents_container.tabBar().tabText(tab_index)}'"
