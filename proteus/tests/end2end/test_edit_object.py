# ==========================================================================
# File: test_edit_object.py
# Description: pytest file for the PROTEUS pyqt edit object use case
# Date: 18/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
# NOTE: Edit properties form dialog is the same for objects, documents
# and projects. This test aims to test dialog access from the context
# menu, access from double click is tested in test_edit_document.py
# ==========================================================================


# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtWidgets import QTreeWidgetItem, QDialogButtonBox
from PyQt6.QtCore import QPoint

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME
from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import app, load_project, get_context_menu, get_dialog

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# End to end "clone object" tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "object_name, document_name",
    [
        ("simple_paragraph", "document_1"),
    ],
)
def test_edit_object(app, object_name, document_name):
    """
    Test the edit object use case. Edit an existing object
    accessing the dialog from the context menu.
    It tests the following steps:
        - Select an existing object
        - Open the context menu and click the edit action
        - Check the archetype was edited
        - Check buttons are enabled
    
    NOTE: Do not double check the properties are updated in the dialog.
    This is tested in test_edit_document.py, this is focused on the
    context menu access and tree item update.
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

    NAME_PROP = PROTEUS_NAME
    NEW_NAME = "new name"

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Get element position
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()

    context_menu: ContextMenu = get_context_menu(lambda: document_tree.customContextMenuRequested.emit(element_position))
    first_dialog: PropertyDialog = get_dialog(context_menu.action_edit_object.trigger)

    # Change properties
    # NOTE: inputs types are known so we can use setText
    first_dialog.input_widgets[NAME_PROP].input.setText(NEW_NAME)

    # Accept dialog
    first_dialog.accept_button.click()
    first_dialog.deleteLater()
    
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

    # Check tree item was updated
    assert (
        tree_element.text(0) == NEW_NAME
    ), f"Tree item name must be '{NEW_NAME}' but it is '{tree_element.text(0)}'"

    # Open dialog again to check properties were updated
    assert_dialog: PropertyDialog = get_dialog(context_menu.action_edit_object.trigger)

    # Check properties changed
    current_name = str(assert_dialog.input_widgets[NAME_PROP].get_value())

    assert (
        current_name == NEW_NAME
    ), f"Expected name to be '{NEW_NAME}' but it is '{current_name}'"
