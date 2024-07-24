# ==========================================================================
# File: test_change_object_position.py
# Description: pytest file for the PROTEUS pyqt change object position action
# Date: 25/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================


# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import QPoint, Qt

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import app, load_project, get_context_menu

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

DOCUMENT_ID = SampleData.get("document_1")
OBJECT_ID = SampleData.get("simple_section")

# --------------------------------------------------------------------------
# End to end "change object position" tests
# --------------------------------------------------------------------------
# NOTE: Move up and down actions are tested using a section placed in the
# second position of the document.
# TODO: Drag and drop actions (limited by pytest-qt)
# TODO: Move while dead objects between target position


def test_change_object_position_up(app):
    """
    Test change object position up action. Steps:
        - Select object
        - Click on move up action

    Checks:
        - Main menu buttons state
        - Object position
        - Selected object in state manager
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Buttons that should change state when an object is moved
    save_button_state = main_window.main_menu.save_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document
    tab = documents_container.tabs.get(DOCUMENT_ID)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    document_tree: DocumentTree = documents_container.tabs[DOCUMENT_ID]
    tree_element: QTreeWidgetItem = document_tree.tree_items[OBJECT_ID]

    # Click the object in the tree
    document_tree.itemPressed.emit(tree_element, 0)

    # Store tree element position relative to its siblings
    tree_element_position = document_tree.indexFromItem(tree_element).row()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Get element position and emit context menu
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    # Click the move up action
    context_menu.action_move_up_object.trigger()

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

    # Check element position changed -------------------------------------------
    new_element_position = document_tree.indexFromItem(tree_element).row()
    assert tree_element_position - 1 != new_element_position, (
        "Element position should change when moved up"
        f"Current position: {new_element_position}"
        f"Expected position: {tree_element_position-1}"
    )

    # Check the element is the selected object in state manager ----------------
    assert main_window._state_manager.get_current_object() == OBJECT_ID, (
        "The moved object should be the selected object in the state manager"
        f"Current object: {main_window._state_manager.get_current_object()}"
        f"Expected object: {OBJECT_ID}"
    )

    # Check the tree element data (ProteusID) is the same as the selected object
    current_element_data = document_tree.currentItem().data(1, Qt.ItemDataRole.UserRole)    
    assert current_element_data == OBJECT_ID, (
        "The tree element data should be the same as the selected object"
        f"Current data: {current_element_data}"
        f"Expected data: {OBJECT_ID}"
    )


def test_change_object_position_down(app):
    """
    Test change object position down action. Steps:
        - Select object
        - Click on move down action

    Checks:
        - Main menu buttons state
        - Object position
        - Selected object in state manager
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

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
    
    # Click the object in the tree
    document_tree.itemPressed.emit(tree_element, 0)

    # Store tree element position relative to its siblings
    tree_element_position = document_tree.indexFromItem(tree_element).row()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Get element position and emit context menu
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    # Click the move down action
    context_menu.action_move_down_object.trigger()
    

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

    # Check element position changed -------------------------------------------
    new_element_position = document_tree.indexFromItem(tree_element).row()
    assert tree_element_position + 1 != new_element_position, (
        "Element position should change when moved up"
        f"Current position: {new_element_position}"
        f"Expected position: {tree_element_position+1}"
    )

    # Check the element is the selected object in state manager ----------------
    assert main_window._state_manager.get_current_object() == OBJECT_ID, (
        "The moved object should be the selected object in the state manager"
        f"Current object: {main_window._state_manager.get_current_object()}"
        f"Expected object: {OBJECT_ID}"
    )

    # Check the tree element data (ProteusID) is the same as the selected object
    current_element_data = document_tree.currentItem().data(1, Qt.ItemDataRole.UserRole)    
    assert current_element_data == OBJECT_ID, (
        "The tree element data should be the same as the selected object"
        f"Current data: {current_element_data}"
        f"Expected data: {OBJECT_ID}"
    )
    
