# ==========================================================================
# File: test_delete_object.py
# Description: pytest file for the PROTEUS pyqt delete object use case
# Date: 18/08/2023
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

import pytest
from PyQt6.QtWidgets import QTreeWidgetItem, QTreeWidget, QApplication
from PyQt6.QtCore import QPoint, QTimer

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.abstract_object import ProteusState
from proteus.views.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "example_project"

# --------------------------------------------------------------------------
# End to end "delete object" tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "object_id, document_id",
    [
        ("64xM8FLyxtaB", "3fKhMAkcEe2C"),
        ("7s63wvxgekU6", "3fKhMAkcEe2D"),
    ],
)
def test_delete_object(app, object_id, document_id):
    """
    Test the delete object use case. Delete an existing object.
    It tests the following steps:
        - Select an existing object
        - Open the context menu and click the delete action
        - Check the archetype was deleted
        - Check buttons are enabled
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window, project_name=PROJECT_NAME)

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
    # Emit set current item, accessed in context menu
    document_tree.setCurrentItem(tree_element)

    # Store the old number of objects in the document
    old_objects_number = len(document_tree.tree_items)
    parent_element: QTreeWidgetItem = tree_element.parent()
    old_parent_children_number = parent_element.childCount()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    def handle_menu():
        menu: ContextMenu = QApplication.activePopupWidget()
        while menu is None:
            menu = QApplication.activePopupWidget()

        # Click the clone action
        menu.action_delete_object.trigger()

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

    # Check the new number of objects in the document
    assert (
        len(document_tree.tree_items) == old_objects_number - 1
    ), f"Number of objects in the document must be '{old_objects_number} - 1' but it is '{len(document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_element.childCount() == old_parent_children_number - 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} - 1' but it is '{parent_element.childCount()}'"

    # Check the object was deleted from the tree items dictionary
    assert (
        object_id not in document_tree.tree_items
    ), f"Object with id '{object_id}' should not be in the tree items dictionary"

    # Check the object was marked as DEAD in the service
    object_state: ProteusState = main_window._controller.get_element(object_id).state
    assert (
        object_state == ProteusState.DEAD
    ), f"Object with id '{object_id}' should be marked as DEAD in the service, but it is '{object_state}'"
