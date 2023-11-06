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
from PyQt6.QtWidgets import QTreeWidgetItem, QTreeWidget, QApplication, QDialogButtonBox
from PyQt6.QtCore import QPoint, QTimer

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME
from proteus.views.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "example_project"

# --------------------------------------------------------------------------
# End to end "clone object" tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "object_id, document_id",
    [
        ("64xM8FLyxtaB", "3fKhMAkcEe2C"),
        ("7s63wvxgekU6", "3fKhMAkcEe2D"),
    ],
)
def test_edit_object(app, object_id, document_id):
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

    NAME_PROP = PROTEUS_NAME
    NEW_NAME = "new name"

    # --------------------------------------------
    # Act
    # --------------------------------------------

    def handle_menu():
        menu: ContextMenu = QApplication.activePopupWidget()
        while menu is None:
            menu = QApplication.activePopupWidget()

        # Click the clone action
        QTimer.singleShot(5, handle_dialog)  # Wait for the dialog to be created
        menu.action_edit_object.trigger()

        # Manual trigger of actions does not close the menu
        menu.close()

    def handle_dialog():
        dialog: PropertyDialog = QApplication.activeModalWidget()
        while not dialog:
            dialog = QApplication.activeModalWidget()

        # Change properties
        # NOTE: inputs types are known so we can use setText
        dialog.input_widgets[NAME_PROP].input.setText(NEW_NAME)

        # Accept dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()

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

    # Check tree item was updated
    assert (
        tree_element.text(0) == NEW_NAME
    ), f"Tree item name must be '{NEW_NAME}' but it is '{tree_element.text(0)}'"
