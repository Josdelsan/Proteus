# ==========================================================================
# File: test_copy_object.py
# Description: pytest file for the PROTEUS pyqt copy object use case
# Date: 16/07/2024
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
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QTreeWidgetItem, QApplication
from PyQt6.QtGui import QKeySequence

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.object import Object
from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.views.components.dialogs.base_dialogs import MessageBox
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import (
    app,
    load_project,
    get_context_menu,
    get_dialog,
)
from proteus.application.resources.translator import translate as _

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# End to end "copy object" tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "object_name, document_name",
    [
        ("simple_section", "document_1"),
        ("section_dl_1", "document_1"),
        ("section_dl_2", "document_1"),
    ],
)
def test_copy_object_same_parent(app, object_name, document_name):
    """
    Test the copy object use case. Copy an existing object.
    It tests the following steps:
        - Select an existing object
        - Open the object context menu and click the copy action
        - Open the parent object context menu and click the paste action

    Checks:
        - Object is copied
        - Buttons are enabled (save, undo)
        - Actions are enabled (copy, paste)
        - Clipboard content is the object id
        - Current selected object is the parent
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    object_id = SampleData.get(object_name)
    document_id = SampleData.get(document_name)

    load_project(main_window=main_window)

    # Clear clipboard
    QApplication.clipboard().clear()

    # Buttons that should change state when archetype is cloned
    save_button_state = main_window.main_menu.save_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document tab
    tab = documents_container.tabs.get(document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    document_tree: DocumentTree = documents_container.tabs[document_id]
    tree_element: QTreeWidgetItem = document_tree.tree_items[object_id]

    # Store the old number of objects in the document
    old_objects_number = len(document_tree.tree_items)
    parent_element: QTreeWidgetItem = tree_element.parent()
    old_parent_children_number = parent_element.childCount()

    # Calculate number of objects copied (including children)
    object_to_copy: Object = main_window._controller.get_element(object_id)
    objects_cloned_number = len(object_to_copy.get_ids())

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click the object in the tree
    document_tree.itemPressed.emit(tree_element, 0)
    # Get element position and trigger context menu
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    # Click copy action
    context_menu.action_copy_object.trigger()

    # Click the parent tree item
    document_tree.itemPressed.emit(parent_element, 0)

    # Get parent element position and trigger context menu
    parent_element_position: QPoint = document_tree.visualItemRect(
        parent_element
    ).center()
    parent_context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(parent_element_position)
    )

    # Click paste action
    parent_context_menu.action_paste_object.trigger()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check copy and paste actions are enabled
    assert context_menu.action_copy_object.isEnabled(), "Copy action should be enabled"

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

    # Check the new number of objects in the document --------------------------------------------
    assert (
        len(document_tree.tree_items) == old_objects_number + objects_cloned_number
    ), f"Number of objects in the document must be '{old_objects_number} + {objects_cloned_number}' but it is '{len(document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + {1}' but it is '{parent_element.childCount()}'"

    # Check the clipboard content is the object id
    assert (
        QApplication.clipboard().text() == object_id
    ), f"Clipboard content should be '{object_id}' but it is '{QApplication.clipboard().text()}'"

    # Check current selected object is the parent --------------------------------------------
    parent_id = parent_element.data(1, Qt.ItemDataRole.UserRole)
    assert (
        main_window._state_manager.get_current_object() == parent_id
    ), f"Current selected object should be '{parent_id}' but it is '{main_window._state_manager.get_current_object()}'"

    # Check document tree current item is the parent tree element
    assert (
        document_tree.currentItem() == parent_element
    ), "Current item in the document tree should be the parent tree element"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------

    QApplication.clipboard().clear()


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
def test_copy_object_different_parent(
    app, object_name, document_name, parent_name, parent_document_name
):
    """
    Test the copy object use case. Copy an existing object to a different parent.
    It tests the following steps:
        - Select an existing object
        - Open the object context menu and click the copy action
        - Change the document tab if needed
        - Open the parent object context menu and click the paste action
    
    Checks:
        - Object is copied
        - Buttons are enabled (save, undo)
        - Actions are enabled (copy, paste)
        - Clipboard content is the object id
        - Current selected document is the parent document
        - Current selected object is the parent
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
    QApplication.clipboard().clear()

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

    # Store the old number of objects in the document
    old_objects_number = len(parent_document_tree.tree_items)
    old_parent_children_number = parent_tree_element.childCount()

    # Calculate number of objects copied (including children)
    object_to_copy: Object = main_window._controller.get_element(object_id)
    objects_cloned_number = len(object_to_copy.get_ids())

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

    # Click copy action
    context_menu.action_copy_object.trigger()

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

    # Check copy and paste actions are enabled
    assert context_menu.action_copy_object.isEnabled(), "Copy action should be enabled"

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

    # Check the new number of objects in the document --------------------------------------------
    assert (
        len(parent_document_tree.tree_items)
        == old_objects_number + objects_cloned_number
    ), f"Number of objects in the document must be '{old_objects_number} + {objects_cloned_number}' but it is '{len(parent_document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_tree_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + {1}' but it is '{parent_tree_element.childCount()}'"

    # Check the clipboard content is the object id
    assert (
        QApplication.clipboard().text() == object_id
    ), f"Clipboard content should be '{object_id}' but it is '{QApplication.clipboard().text()}'"

    # Check current selected document is the parent document --------------------------------------------
    assert (
        main_window._state_manager.get_current_document() == parent_document_id
    ), f"Current selected document should be '{parent_document_id}' but it is '{main_window._state_manager.get_current_document()}'"

    # Check current selected object is the parent
    assert (
        main_window._state_manager.get_current_object() == parent_id
    ), f"Current selected object should be '{parent_id}' but it is '{main_window._state_manager.get_current_object()}'"

    # Check document tree current item is the parent tree element
    assert (
        parent_document_tree.currentItem() == parent_tree_element
    ), "Current item in the document tree should be the parent tree element"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------
    QApplication.clipboard().clear()


@pytest.mark.parametrize(
    "object_name, document_name",
    [
        ("simple_section", "document_1"),
        ("section_dl_1", "document_1"),
    ],
)
def test_copy_object_ctrl_c_v_same_parent(
    qtbot: QtBot, app, object_name, document_name
):
    """
    Test the copy object use case. Copy an existing object using ctrl+c and ctrl+v.
    It tests the following steps:
        - Select an existing object
        - Press ctrl+c
        - Open the parent object context menu and click the paste action

    Checks:
        - Object is copied
        - Buttons are enabled (save, undo)
        - Clipboard content
        - Current selected object is the parent
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    object_id = SampleData.get(object_name)
    document_id = SampleData.get(document_name)

    load_project(main_window=main_window)

    # Clear clipboard
    QApplication.clipboard().clear()

    # Buttons that should change state when archetype is cloned
    save_button_state = main_window.main_menu.save_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # Get document container
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Click the document tab
    tab = documents_container.tabs.get(document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Object tree element
    document_tree: DocumentTree = documents_container.tabs[document_id]
    tree_element: QTreeWidgetItem = document_tree.tree_items[object_id]

    # Store the old number of objects in the document
    old_objects_number = len(document_tree.tree_items)
    parent_element: QTreeWidgetItem = tree_element.parent()
    old_parent_children_number = parent_element.childCount()

    # Calculate number of objects copied (including children)
    object_to_copy: Object = main_window._controller.get_element(object_id)
    objects_cloned_number = len(object_to_copy.get_ids())

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Ctrl+C the object
    document_tree.itemPressed.emit(tree_element, 0)
    qtbot.keySequence(document_tree, QKeySequence.StandardKey.Copy)

    # Ctrl+V in the parent
    document_tree.itemPressed.emit(parent_element, 0)
    qtbot.keySequence(document_tree, QKeySequence.StandardKey.Paste)

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

    # Check the new number of objects in the document --------------------------------------------
    assert (
        len(document_tree.tree_items) == old_objects_number + objects_cloned_number
    ), f"Number of objects in the document must be '{old_objects_number} + {objects_cloned_number}' but it is '{len(document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + {1}' but it is '{parent_element.childCount()}'"

    # Check the clipboard content is the object id
    assert (
        QApplication.clipboard().text() == object_id
    ), f"Clipboard content should be '{object_id}' but it is '{QApplication.clipboard().text()}'"

    # Check current selected object is the parent --------------------------------------------
    parent_id = parent_element.data(1, Qt.ItemDataRole.UserRole)
    assert (
        main_window._state_manager.get_current_object() == parent_id
    ), f"Current selected object should be '{parent_id}' but it is '{main_window._state_manager.get_current_object()}'"

    # Check document tree current item is the parent tree element
    assert (
        document_tree.currentItem() == parent_element
    ), "Current item in the document tree should be the parent tree element"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------

    QApplication.clipboard().clear()


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
def test_copy_object_ctrl_c_v_different_parent(
    qtbot: QtBot, app, object_name, document_name, parent_name, parent_document_name
):
    """
    Test the copy object use case. Copy an existing object to a different parent using ctrl+c and ctrl+v.
    It tests the following steps:
        - Select an existing object
        - Press ctrl+c
        - Change the document tab if needed
        - Open the parent object context menu and click the paste action

    Checks:
        - Object is copied
        - Buttons are enabled (save, undo)
        - Clipboard content
        - Current selected document is the parent document
        - Current selected object is the parent
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
    QApplication.clipboard().clear()

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

    # Object tree element and parent tree element
    object_document_tree: DocumentTree = documents_container.tabs[object_document_id]
    object_tree_element: QTreeWidgetItem = object_document_tree.tree_items[object_id]

    parent_document_tree: DocumentTree = documents_container.tabs[parent_document_id]
    parent_tree_element: QTreeWidgetItem = parent_document_tree.tree_items[parent_id]

    # Store the old number of objects in the document
    old_objects_number = len(parent_document_tree.tree_items)
    old_parent_children_number = parent_tree_element.childCount()

    # Calculate number of objects copied (including children)
    object_to_copy: Object = main_window._controller.get_element(object_id)
    objects_cloned_number = len(object_to_copy.get_ids())

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Ctrl+C the object
    object_document_tree.itemPressed.emit(object_tree_element, 0)
    qtbot.keySequence(object_document_tree, QKeySequence.StandardKey.Copy)

    # Change document tab
    tab = documents_container.tabs.get(parent_document_id)
    document_tab_index: int = documents_container.indexOf(tab)
    documents_container.currentChanged.emit(document_tab_index)

    # Ctrl+V in the parent
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

    # Check the new number of objects in the document --------------------------------------------
    assert (
        len(parent_document_tree.tree_items)
        == old_objects_number + objects_cloned_number
    ), f"Number of objects in the document must be '{old_objects_number} + {objects_cloned_number}' but it is '{len(parent_document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_tree_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + {1}' but it is '{parent_tree_element.childCount()}'"

    # Check the clipboard content is the object id
    assert (
        QApplication.clipboard().text() == object_id
    ), f"Clipboard content should be '{object_id}' but it is '{QApplication.clipboard().text()}'"

    # Check current selected document is the parent document --------------------------------------------
    assert (
        main_window._state_manager.get_current_document() == parent_document_id
    ), f"Current selected document should be '{parent_document_id}' but it is '{main_window._state_manager.get_current_document()}'"

    # Check current selected object is the parent
    assert (
        main_window._state_manager.get_current_object() == parent_id
    ), f"Current selected object should be '{parent_id}' but it is '{main_window._state_manager.get_current_object()}'"

    # Check document tree current item is the parent tree element
    assert (
        parent_document_tree.currentItem() == parent_tree_element
    ), "Current item in the document tree should be the parent tree element"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------
    QApplication.clipboard().clear()


@pytest.mark.parametrize(
    "clipboard_content",
    [
        "",
        "12 34",
        "true",
    ],
)
def test_paste_disable_when_clipboard_content_is_not_valid(app, clipboard_content):
    """
    Test the copy object use case. Paste action is disabled when clipboard content is not valid.
    It tests the following steps:
        - Set the clipboard content to an invalid value
        - Open the parent object context menu and check the paste action is disabled

    Checks:
        - Paste action is disabled
        - Current selected object in document tree is correct
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    document_id = SampleData.get("document_1")

    # Clear clipboard
    QApplication.clipboard().clear()

    # Set clipboard content
    QApplication.clipboard().setText(clipboard_content)

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
    parent_tree_element: QTreeWidgetItem = document_tree.tree_items[
        document_id
    ]  # Documents accepts any object

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Get parent element position and trigger context menu
    document_tree.itemPressed.emit(parent_tree_element, 0)
    parent_element_position: QPoint = document_tree.visualItemRect(
        parent_tree_element
    ).center()
    parent_context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(parent_element_position)
    )

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check the paste action is disabled
    assert (
        not parent_context_menu.action_paste_object.isEnabled()
    ), "Paste action should be disabled"

    # Check the document tree current item is the parent tree element
    assert (
        document_tree.currentItem() == parent_tree_element
    ), "Current item in the document tree should be the parent tree element"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------
    QApplication.clipboard().clear()


def test_paste_disable_for_invalid_parent(qtbot: QtBot, app):
    """
    Test the copy object use case. Paste action is disabled for invalid parent.

    It tests the following steps:
        - Select an existing object
        - Open the object context menu and click the copy action

    Checks:
        - Open the parent object context menu and check the paste action is disabled
          (invalid parent)
    """

    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    # NOTE: Copying a section into an objective is not allowed
    object_id = SampleData.get("simple_section")
    document_id = SampleData.get("document_1")
    parent_id = SampleData.get("objective_dl_1")

    load_project(main_window=main_window)

    # Clear clipboard
    QApplication.clipboard().clear()

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
    object_tree_element: QTreeWidgetItem = document_tree.tree_items[object_id]
    parent_tree_element: QTreeWidgetItem = document_tree.tree_items[parent_id]

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Ctrl+C the object
    document_tree.itemPressed.emit(object_tree_element, 0)
    qtbot.keySequence(document_tree, QKeySequence.StandardKey.Copy)

    # Get parent element position and trigger context menu
    document_tree.itemPressed.emit(parent_tree_element, 0)
    parent_element_position: QPoint = document_tree.visualItemRect(
        parent_tree_element
    ).center()
    parent_context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(parent_element_position)
    )

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check the paste action is disabled
    assert (
        not parent_context_menu.action_paste_object.isEnabled()
    ), "Paste action should be disabled"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------
    QApplication.clipboard().clear()


def test_copy_disable_for_document(app):
    """
    Test the copy object use case. Copy action is disabled for documents.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    document_id = SampleData.get("document_1")

    # Clear clipboard
    QApplication.clipboard().clear()

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

    # Check the copy action is disabled
    assert (
        not context_menu.action_copy_object.isEnabled()
    ), "Copy action should be disabled"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------
    QApplication.clipboard().clear()


# TODO: Find a more consistent way to check application state
@pytest.mark.parametrize(
    "clipboard_content",
    [
        "",
        "12 34",
        "true",
    ],
)
def test_ignore_paste_ctrl_v_with_invalid_clipboard_content(
    qtbot: QtBot, app, clipboard_content
):
    """
    Test the copy object use case. Paste action is ignored when clipboard content is not valid.
    It tests the following steps:
        - Set the clipboard content to an invalid value
        - Select a parent object and press ctrl+v
        - No copy action is performed and no error is shown
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    document_id = SampleData.get("document_1")

    # Clear clipboard
    QApplication.clipboard().clear()

    # Set clipboard content
    QApplication.clipboard().setText(clipboard_content)

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
    parent_tree_element: QTreeWidgetItem = document_tree.tree_items[document_id]

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Ctrl+V in the parent
    document_tree.itemPressed.emit(parent_tree_element, 0)
    qtbot.keySequence(document_tree, QKeySequence.StandardKey.Paste)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check no popup window is shown
    assert not QApplication.activeModalWidget(), "No popup window should be shown"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------

    QApplication.clipboard().clear()


def test_paste_error_message_when_ctrl_v_in_invalid_parent(qtbot: QtBot, app):
    """
    Test the copy object use case. Error message is shown when ctrl+v in an invalid parent.
    It tests the following steps:
        - Select an existing object
        - Press ctrl+c
        - Select an invalid parent and press ctrl+v

    Checks:
        - An error message is shown
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    # NOTE: Copying a section into an objective is not allowed
    object_id = SampleData.get("simple_section")
    document_id = SampleData.get("document_1")
    parent_id = SampleData.get("objective_dl_1")

    load_project(main_window=main_window)

    # Clear clipboard
    QApplication.clipboard().clear()

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
    object_tree_element: QTreeWidgetItem = document_tree.tree_items[object_id]
    parent_tree_element: QTreeWidgetItem = document_tree.tree_items[parent_id]

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Ctrl+C the object
    document_tree.itemPressed.emit(object_tree_element, 0)
    qtbot.keySequence(document_tree, QKeySequence.StandardKey.Copy)

    # Ctrl+V in the parent
    document_tree.itemPressed.emit(parent_tree_element, 0)
    error_dialog: MessageBox = get_dialog(
        lambda: qtbot.keySequence(document_tree, QKeySequence.StandardKey.Paste)
    )

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    object_name = (
        main_window._controller.get_element(object_id).get_property(PROTEUS_NAME).value
    )

    # Check the title of the error message
    assert error_dialog.windowTitle() == _(
        "document_tree.paste_action.message_box.error.title", object_name
    ), f"Error message title should be '{_('document_tree.paste_action.message_box.error.title', object_name)}' but it is '{error_dialog.windowTitle()}'"

    # Check the error message
    assert error_dialog.text() == _(
        "document_tree.paste_action.message_box.error.text", object_name
    ), f"Error message should be '{_('document_tree.paste_action.message_box.error.text', object_name)}' but it is '{error_dialog.text()}'"

    # --------------------------------------------
    # Clean up
    # --------------------------------------------

    QApplication.clipboard().clear()
