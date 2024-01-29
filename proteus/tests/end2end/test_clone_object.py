# ==========================================================================
# File: test_clone_object.py
# Description: pytest file for the PROTEUS pyqt clone object use case
# Date: 18/08/2023
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
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import QPoint

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import app, load_project, get_context_menu

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# End to end "clone object" tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "object_name, document_name",
    [
        ("simple_section", "document_1"),
        ("section_dl_1", "document_1"),
        ("section_dl_2", "document_1"),
    ],
)
def test_clone_object(app, object_name, document_name):
    """
    Test the clone object use case. Clone an existing object.
    It tests the following steps:
        - Select an existing object
        - Open the context menu and click the clone action
        - Check the archetype is cloned
        - Check buttons are enabled
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    object_id = SampleData.get(object_name)
    document_id = SampleData.get(document_name)

    load_project(main_window=main_window)

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

    # Calculate number of objects cloned (including children)
    object_to_clone_id: ProteusID = tree_element.data(1, Qt.ItemDataRole.UserRole)
    object_to_clone: Object = main_window._controller.get_element(object_to_clone_id)
    objects_cloned_number = len(object_to_clone.get_ids())

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Get element position and trigger context menu
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    # Click clone action
    context_menu.action_clone_object.trigger()

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
        len(document_tree.tree_items) == old_objects_number + objects_cloned_number
    ), f"Number of objects in the document must be '{old_objects_number} + {objects_cloned_number}' but it is '{len(document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        parent_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + {1}' but it is '{parent_element.childCount()}'"
