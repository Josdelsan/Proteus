# ==========================================================================
# File: test_change_object_position.py
# Description: pytest file for the PROTEUS pyqt change object position action
# Date: 25/08/2023
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

from PyQt6.QtWidgets import QTreeWidgetItem, QTreeWidget, QApplication
from PyQt6.QtCore import QPoint, QTimer

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "example_project"
DOCUMENT_ID = "56i4dHSDSppX" # 'EXAMPLE' document from example project
OBJECT_ID = "4Etjfs7bAYgX" # 'Objective' object from 'EXAMPLE' document

# --------------------------------------------------------------------------
# End to end "change object position" tests
# --------------------------------------------------------------------------
# NOTE: Move up and down actions are tested. Drag and drop testing is not
# implemented yet.

def test_change_object_position_up(app):
    """
    Test change object position up action. Steps:
        - Select object
        - Click on move up action
        - Check object position
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window, project_name=PROJECT_NAME)

    # Buttons that should change state when an object is moved
    save_button_state = main_window.main_menu.save_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document tab
    tab = documents_container.tabs.get(DOCUMENT_ID)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    document_tree: DocumentTree = documents_container.tabs[DOCUMENT_ID]
    tree_element: QTreeWidgetItem = document_tree.tree_items[OBJECT_ID]
    # Emit set current item, accessed in context menu
    document_tree.setCurrentItem(tree_element)

    # Store tree element position relative to its siblings
    tree_element_position = document_tree.indexFromItem(tree_element).row()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    def handle_menu():
        menu: ContextMenu = QApplication.activePopupWidget()
        while menu is None:
            menu = QApplication.activePopupWidget()

        # Click the clone action
        menu.action_move_up_object.trigger()

        # Manual trigger of actions does not close the menu
        menu.close()

    # Get element position
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    QTimer.singleShot(5, handle_menu)  # Wait for the menu to be created
    document_tree.customContextMenuRequested.emit(element_position)  


    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check buttons state changed
    assert save_button_state != main_window.main_menu.save_button.isEnabled(), (
        "Save button state should change from DISABLED to ENABLED when an archetype is cloned"
        f"Current state: {main_window.main_menu.save_button.isEnabled()}"
    )
    assert undo_button_state != main_window.main_menu.undo_button.isEnabled(), (
        "Undo button state should change from DISABLED to ENABLED when an archetype is cloned"
        f"Current state: {main_window.main_menu.undo_button.isEnabled()}"
    )

    # Check element position changed
    new_element_position = document_tree.indexFromItem(tree_element).row()
    assert tree_element_position-1 != new_element_position, (
        "Element position should change when moved up"
        f"Current position: {new_element_position}"
        f"Expected position: {tree_element_position-1}"
    )

def test_change_object_position_down(app):
    """
    Test change object position down action. Steps:
        - Select object
        - Click on move down action
        - Check object position
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window, project_name=PROJECT_NAME)

    # Buttons that should change state when an object is moved
    save_button_state = main_window.main_menu.save_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document tab
    tab = documents_container.tabs.get(DOCUMENT_ID)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    document_tree: DocumentTree = documents_container.tabs[DOCUMENT_ID]
    tree_element: QTreeWidgetItem = document_tree.tree_items[OBJECT_ID]
    # Emit set current item, accessed in context menu
    document_tree.setCurrentItem(tree_element)

    # Store tree element position relative to its siblings
    tree_element_position = document_tree.indexFromItem(tree_element).row()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    def handle_menu():
        menu: ContextMenu = QApplication.activePopupWidget()
        while menu is None:
            menu = QApplication.activePopupWidget()

        # Click the clone action
        menu.action_move_down_object.trigger()

        # Manual trigger of actions does not close the menu
        menu.close()

    # Get element position
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    QTimer.singleShot(5, handle_menu)  # Wait for the menu to be created
    document_tree.customContextMenuRequested.emit(element_position)  


    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check buttons state changed
    assert save_button_state != main_window.main_menu.save_button.isEnabled(), (
        "Save button state should change from DISABLED to ENABLED when an archetype is cloned"
        f"Current state: {main_window.main_menu.save_button.isEnabled()}"
    )
    assert undo_button_state != main_window.main_menu.undo_button.isEnabled(), (
        "Undo button state should change from DISABLED to ENABLED when an archetype is cloned"
        f"Current state: {main_window.main_menu.undo_button.isEnabled()}"
    )

    # Check element position changed
    new_element_position = document_tree.indexFromItem(tree_element).row()
    assert tree_element_position+1 != new_element_position, (
        "Element position should change when moved up"
        f"Current position: {new_element_position}"
        f"Expected position: {tree_element_position+1}"
    )