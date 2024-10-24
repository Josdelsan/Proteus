# ==========================================================================
# File: test_clone_archetype.py
# Description: pytest file for the PROTEUS pyqt clone archetype use case
# Date: 16/08/2023
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
from PyQt6.QtWidgets import QTreeWidgetItem

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.archetypes_menu_dropdown import ArchetypesMenuDropdown
from proteus.application.state.manager import StateManager
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# End to end "clone archetype" tests
# --------------------------------------------------------------------------
# TODO: Tests archetype cloning from context menu (use case steps, objectives, etc.)


@pytest.mark.parametrize(
    "archetype_id, archetype_class, parent_name, document_name",
    [
        (
            "local-figure",
            "figure",
            "document_1",
            "document_1",
        ),  # Local figure into document
        (
            "local-figure",
            "figure",
            "simple_section",
            "document_1",
        ),  # Local figure into section
        (
            "remote-figure",
            "figure",
            "simple_section",
            "document_1",
        ),  # Remote figure into section
    ],
)
def test_clone_archetype_dropdown_menu(app, archetype_id, archetype_class, parent_name, document_name):
    """
    Test the clone archetype use case. Clone an archetype in an existing
    object/document. It tests the following steps:
        - Select an existing object/document
        - Press the desired archetype button from the dropdown menu

    Checks:
        - Archetype is cloned
        - Buttons are enabled
        - Selected object is correctly set and remains selected
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    parent_id = SampleData.get(parent_name)
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

    # Click the object tree item
    document_tree: DocumentTree = documents_container.tabs[document_id]
    tree_element: QTreeWidgetItem = document_tree.tree_items[parent_id]
    document_tree.itemPressed.emit(tree_element, 0)

    # Store the old number of objects in the document
    old_objects_number = len(document_tree.tree_items)
    old_parent_children_number = tree_element.childCount()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click the archetype button
    archetype_button = main_window.main_menu.archetype_buttons.get(archetype_class)
    archetype_class_menu: ArchetypesMenuDropdown = archetype_button.menu()
    archetype_class_menu.actions[archetype_id].triggered.emit()

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

    # Check the new number of objects in the document -----------------------
    assert (
        len(document_tree.tree_items) == old_objects_number + 1
    ), f"Number of objects in the document must be '{old_objects_number} + 1' but it is '{len(document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        tree_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + 1' but it is '{tree_element.childCount()}'"

    # Check current document and object in state manager ---------------------
    assert (
        StateManager().get_current_document() == document_id
    ), f"Current document must be '{document_id}' but it is '{StateManager().current_document}'"

    assert (
        StateManager().get_current_object() == parent_id
    ), f"Current object must be '{parent_id}' but it is '{StateManager().current_object}'"



@pytest.mark.parametrize(
    "archetype_class, parent_name, document_name",
    [
        (
            "section",
            "document_1",
            "document_1",
        ),  # Empty paragraph into document
        (
            "section",
            "simple_section",
            "document_1",
        ),  # Section into section
        # (
        #     "objective",
        #     "simple_objective",
        #     "document_1",
        # ),  # Objective into objective
        # FIX: temporary disabled because test data changed
    ],
)
def test_clone_archetype_no_dropdown_menu(app, archetype_class, parent_name, document_name):
    """
    Test the clone archetype use case. Clone an archetype in an existing
    object/document. It tests the following steps:
        - Select an existing object/document
        - Press the desired archetype class button

    Checks:
        - Archetype is cloned
        - Buttons are enabled
        - Selected object is correctly set and remains selected
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    parent_id = SampleData.get(parent_name)
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

    # Click the object tree item
    document_tree: DocumentTree = documents_container.tabs[document_id]
    tree_element: QTreeWidgetItem = document_tree.tree_items[parent_id]
    document_tree.itemPressed.emit(tree_element, 0)

    # Store the old number of objects in the document
    old_objects_number = len(document_tree.tree_items)
    old_parent_children_number = tree_element.childCount()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click the archetype button
    archetype_class_button = main_window.main_menu.archetype_buttons.get(archetype_class)
    archetype_class_button.clicked.emit()

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

    # Check the new number of objects in the document -----------------------
    assert (
        len(document_tree.tree_items) == old_objects_number + 1
    ), f"Number of objects in the document must be '{old_objects_number} + 1' but it is '{len(document_tree.tree_items)}'"

    # Check the new object was added to the parent tree item
    assert (
        tree_element.childCount() == old_parent_children_number + 1
    ), f"Number of children in the parent tree item must be '{old_parent_children_number} + 1' but it is '{tree_element.childCount()}'"

    # Check current document and object in state manager ---------------------
    assert (
        StateManager().get_current_document() == document_id
    ), f"Current document must be '{document_id}' but it is '{StateManager().current_document}'"

    assert (
        StateManager().get_current_object() == parent_id
    ), f"Current object must be '{parent_id}' but it is '{StateManager().current_object}'"
