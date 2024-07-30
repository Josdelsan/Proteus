# ==========================================================================
# File: test_cut_object.py
# Description: pytest file for the PROTEUS pyqt cut object use case
# Date: 30/07/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================


# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from pytestqt.qtbot import QtBot
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtGui import QKeySequence

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.application.clipboard import Clipboard, ClipboardStatus
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import (
    app,
    load_project,
    get_context_menu,
)
from proteus.application.resources.translator import translate as _

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# End to end "cut object" tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "object_name, document_name, parent_name, parent_document_name",
    [
        (
            "simple_section",
            "document_1",
            "empty_document",
            "empty_document",
        ),  # different parent different document
        ("section_dl_1", "document_1", "empty_document", "empty_document"),
        ("section_dl_2", "document_1", "empty_document", "empty_document"),
        (
            "section_dl_1",
            "document_1",
            "simple_section",
            "document_1",
        ),  # different parent same document
        ("section_dl_2", "document_1", "simple_section", "document_1"),
    ],
)
def test_cut_object(app, object_name, document_name, parent_name, parent_document_name):
    """
    Test the cut object use case. The test steps are:
        - Select an existing object
        - Open the object context menu and click the cut action
        - Change the document tab if needed
        - Open the parent object context menu and click the paste action

    Checks:
        - Object is moved
        - Buttons are enabled (save, undo)
        - Actions are enabled (cut, paste)
        - Clipboard content is the object id before paste
        - Clipboard content is cleared after paste
        - Current selected document is the parent document
        - Current selected object is the moved object
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    object_id = SampleData.get(object_name)
    object_document_id = SampleData.get(document_name)
    parent_id = SampleData.get(parent_name)
    parent_document_id = SampleData.get(parent_document_name)

    load_project(main_window=main_window)

    # Clear clipboard
    Clipboard().clear()

    # Buttons that should change state when archetype is cloned
    save_button_state = main_window.main_menu.save_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document tab
    tab = documents_container.tabs.get(object_document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Object right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    object_document_tree: DocumentTree = documents_container.tabs[object_document_id]
    object_tree_element: QTreeWidgetItem = object_document_tree.tree_items[object_id]

    parent_document_tree: DocumentTree = documents_container.tabs[parent_document_id]
    parent_tree_element: QTreeWidgetItem = parent_document_tree.tree_items[parent_id]

    # Store the number of children of the current parent and new parent for later comparison
    old_parent_tree_element = object_tree_element.parent()
    old_parent_children_number = old_parent_tree_element.childCount()
    new_parent_children_number = parent_tree_element.childCount()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click the object in the tree
    object_document_tree.itemPressed.emit(object_tree_element, 0)
    # Get element position and trigger context menu
    element_position: QPoint = object_document_tree.visualItemRect(
        object_tree_element
    ).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: object_document_tree.customContextMenuRequested.emit(element_position)
    )

    # Click cut action
    context_menu.action_cut_object.trigger()

    # Change document tab
    tab = documents_container.tabs.get(parent_document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Click the parent tree item
    parent_document_tree.itemPressed.emit(parent_tree_element, 0)
    # Get parent element position and trigger context menu
    parent_element_position: QPoint = parent_document_tree.visualItemRect(
        parent_tree_element
    ).center()
    parent_context_menu: ContextMenu = get_context_menu(
        lambda: parent_document_tree.customContextMenuRequested.emit(
            parent_element_position
        )
    )

    # Click paste action
    parent_context_menu.action_paste_object.trigger()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check cut and paste actions are enabled
    assert context_menu.action_cut_object.isEnabled(), "Copy action should be enabled"

    assert (
        parent_context_menu.action_paste_object.isEnabled()
    ), "Paste action should be enabled"

    # Check buttons state changed
    assert save_button_state != main_window.main_menu.save_button.isEnabled(), (
        "Save button state should change from DISABLED to ENABLED when an archetype is copied"
        f"Current state: {main_window.main_menu.save_button.isEnabled()}"
    )

    assert undo_button_state != main_window.main_menu.undo_button.isEnabled(), (
        "Undo button state should change from DISABLED to ENABLED when an archetype is copied"
        f"Current state: {main_window.main_menu.undo_button.isEnabled()}"
    )

    # Check the new number of objects in the old parent tree --------------------------------------------
    assert (
        old_parent_children_number - 1 == old_parent_tree_element.childCount()
    ), f"Number of children in the old parent tree item must be '{old_parent_children_number} - {1}' but it is '{object_tree_element.parent().childCount()}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_tree_element.childCount() == new_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{new_parent_children_number} + {1}' but it is '{parent_tree_element.childCount()}'"

    # Check the clipboard content is empty and the state is CLEAR ---------------------------------------
    assert (
        Clipboard()._clipboard == ""
    ), f"Clipboard should be empty but it is '{Clipboard()._clipboard}'"

    assert (
        Clipboard()._status == ClipboardStatus.CLEAR
    ), f"Clipboard status should be CLEAR but it is '{Clipboard()._status}'"

    # Check current selected document is the parent document --------------------------------------------
    assert (
        main_window._state_manager.get_current_document() == parent_document_id
    ), f"Current selected document should be '{parent_document_id}' but it is '{main_window._state_manager.get_current_document()}'"

    # Check current selected object is the pasted object
    assert (
        main_window._state_manager.get_current_object() == object_id
    ), f"Current selected object should be '{object_id}' but it is '{main_window._state_manager.get_current_object()}'"

    # Check document tree current item is the parent tree element
    assert (
        parent_document_tree.currentItem() == parent_document_tree.tree_items[object_id]
    ), "Current item in the document tree should be the parent tree element"


@pytest.mark.parametrize(
    "object_name, document_name, parent_name, parent_document_name",
    [
        (
            "simple_section",
            "document_1",
            "empty_document",
            "empty_document",
        ),  # different parent different document
        (
            "section_dl_1",
            "document_1",
            "simple_section",
            "document_1",
        ),  # different parent same document
    ],
)
def test_cut_object_ctrl_x_v(
    qtbot: QtBot, app, object_name, document_name, parent_name, parent_document_name
):
    """
    Test the cut object use case. The test steps are:
        - Select an existing object
        - Press Ctrl+X to cut the object
        - Change the document tab if needed
        - Press Ctrl+V to paste the object in the selected parent

    Checks:
        - Object is moved
        - Buttons are enabled (save, undo)
        - Actions are enabled (cut, paste)
        - Clipboard content is the object id before paste
        - Clipboard content is cleared after paste
        - Current selected document is the parent document
        - Current selected object is the moved object
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    object_id = SampleData.get(object_name)
    object_document_id = SampleData.get(document_name)
    parent_id = SampleData.get(parent_name)
    parent_document_id = SampleData.get(parent_document_name)

    load_project(main_window=main_window)

    # Clear clipboard
    Clipboard().clear()

    # Buttons that should change state when archetype is cloned
    save_button_state = main_window.main_menu.save_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document tab
    tab = documents_container.tabs.get(object_document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Object right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    object_document_tree: DocumentTree = documents_container.tabs[object_document_id]
    object_tree_element: QTreeWidgetItem = object_document_tree.tree_items[object_id]

    parent_document_tree: DocumentTree = documents_container.tabs[parent_document_id]
    parent_tree_element: QTreeWidgetItem = parent_document_tree.tree_items[parent_id]

    # Store the number of children of the current parent and new parent for later comparison
    old_parent_tree_element = object_tree_element.parent()
    old_parent_children_number = old_parent_tree_element.childCount()
    new_parent_children_number = parent_tree_element.childCount()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click the object in the tree
    object_document_tree.itemPressed.emit(object_tree_element, 0)
    qtbot.keySequence(object_document_tree, QKeySequence.StandardKey.Cut)

    # Change document tab
    tab = documents_container.tabs.get(parent_document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Click the parent tree item
    parent_document_tree.itemPressed.emit(parent_tree_element, 0)
    qtbot.keySequence(parent_document_tree, QKeySequence.StandardKey.Paste)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check buttons state changed
    assert save_button_state != main_window.main_menu.save_button.isEnabled(), (
        "Save button state should change from DISABLED to ENABLED when an archetype is copied"
        f"Current state: {main_window.main_menu.save_button.isEnabled()}"
    )

    assert undo_button_state != main_window.main_menu.undo_button.isEnabled(), (
        "Undo button state should change from DISABLED to ENABLED when an archetype is copied"
        f"Current state: {main_window.main_menu.undo_button.isEnabled()}"
    )

    # Check the new number of objects in the old parent tree --------------------------------------------
    assert (
        old_parent_children_number - 1 == old_parent_tree_element.childCount()
    ), f"Number of children in the old parent tree item must be '{old_parent_children_number} - {1}' but it is '{object_tree_element.parent().childCount()}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_tree_element.childCount() == new_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{new_parent_children_number} + {1}' but it is '{parent_tree_element.childCount()}'"

    # Check the clipboard content is empty and the state is CLEAR ---------------------------------------
    assert (
        Clipboard()._clipboard == ""
    ), f"Clipboard should be empty but it is '{Clipboard()._clipboard}'"

    assert (
        Clipboard()._status == ClipboardStatus.CLEAR
    ), f"Clipboard status should be CLEAR but it is '{Clipboard()._status}'"

    # Check current selected document is the parent document --------------------------------------------
    assert (
        main_window._state_manager.get_current_document() == parent_document_id
    ), f"Current selected document should be '{parent_document_id}' but it is '{main_window._state_manager.get_current_document()}'"

    # Check current selected object is the pasted object
    assert (
        main_window._state_manager.get_current_object() == object_id
    ), f"Current selected object should be '{object_id}' but it is '{main_window._state_manager.get_current_object()}'"

    # Check document tree current item is the parent tree element
    assert (
        parent_document_tree.currentItem() == parent_document_tree.tree_items[object_id]
    ), "Current item in the document tree should be the parent tree element"


def test_cut_disable_for_document(app):
    """
    Test the cut object use case. Cut action is disabled for documents.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    document_id = SampleData.get("document_1")

    # Clear clipboard
    Clipboard().clear()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document tab
    tab = documents_container.tabs.get(document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Object tree element and parent tree element
    document_tree: DocumentTree = documents_container.tabs[document_id]
    tree_element: QTreeWidgetItem = document_tree.tree_items[document_id]

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Get element position and trigger context menu
    document_tree.itemPressed.emit(tree_element, 0)
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check the cut action is disabled
    assert (
        not context_menu.action_cut_object.isEnabled()
    ), "Cut action should be disabled"


