# ==========================================================================
# File: test_clone_archetype.py
# Description: pytest file for the PROTEUS pyqt clone archetype use case
# Date: 16/08/2023
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
from PyQt6.QtWidgets import QTreeWidgetItem

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.utils.state_manager import StateManager
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "example_project"

# --------------------------------------------------------------------------
# End to end "clone archetype" tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "archetype_id, parent_id, document_id",
    [
        ("empty-section", "3fKhMAkcEe2C", "3fKhMAkcEe2C"),  # Section into document 1
        ("empty-section", "3fKhMAkcEe2D", "3fKhMAkcEe2D"),  # Section into document 2
        (
            "empty-section",
            "7s63wvxgekU6",
            "3fKhMAkcEe2D",
        ),  # Section into section document 2
    ],
)
def test_clone_archetype(app, archetype_id, parent_id, document_id):
    """
    Test the clone archetype use case. Clone an archetype in an existing
    object/document. It tests the following steps:
        - Select an existing object/document
        - Press the desired archetype button
        - Check the archetype is cloned
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

    # Click the object tree item
    document_tree: DocumentTree = documents_container.tabs[document_id]
    tree_element: QTreeWidgetItem = document_tree.tree_items[parent_id]
    document_tree.itemClicked.emit(tree_element, 0)

    # Check application state
    # NOTE: This is done to detect StateManager inconsistencies and test correct behaviour
    assert (
        StateManager.get_current_document() == document_id
    ), f"Current document must be '{document_id}' but it is '{StateManager.current_document}'"

    assert (
        StateManager.get_current_object() == parent_id
    ), f"Current object must be '{parent_id}' but it is '{StateManager.current_object}'"

    # Store the old number of objects in the document
    old_objects_number = len(document_tree.tree_items)
    old_parent_children_number = tree_element.childCount()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click the archetype button
    archetype_button = main_window.main_menu.archetype_buttons.get(archetype_id)
    archetype_button.click()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check buttons state changed
    assert save_button_state != main_window.main_menu.save_button.isEnabled(), (
        "Save button state should change from DISABLED to ENABLED when an archetype is cloned"
        f"Current state: {main_window.main_menu.save_button.isEnabled()}"
    )
    assert (
        undo_button_state != main_window.main_menu.undo_button.isEnabled()
    ), (
        "Undo button state should change from DISABLED to ENABLED when an archetype is cloned"
        f"Current state: {main_window.main_menu.undo_button.isEnabled()}"
    )


    # Check the new number of objects in the document
    assert (
        len(document_tree.tree_items) == old_objects_number + 1
    ), f"Number of objects in the document must be '{old_objects_number} + 1' but it is '{len(document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        tree_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + 1' but it is '{tree_element.childCount()}'"
