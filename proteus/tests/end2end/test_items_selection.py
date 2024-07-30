# ==========================================================================
# File: test_items_selection.py
# Description: pytest file for the PROTEUS pyqt items selection behavior
# Date: 24/07/2024
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
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import (
    app,
    load_project,
)

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Item selection tests
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "object_name, document_name",
    [
        ("simple_paragraph", "document_1"),
        ("document_1", "document_1"),
    ],
)
def test_object_selection_when_pressed(app, object_name, document_name):
    """
    Test that an object is selected in the state manager when it is clicked.
    """

    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    object_id = SampleData.get(object_name)
    document_id = SampleData.get(document_name)

    load_project(main_window=main_window)

    # Get tree element out of the document tree
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )
    document_tree: DocumentTree = documents_container.tabs[document_id]
    tree_element: QTreeWidgetItem = document_tree.tree_items[object_id]

    # Store old state manager object
    old_object = main_window._state_manager.get_current_object()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click on the tree element using the itemPressed signal
    document_tree.itemPressed.emit(tree_element, 0)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check that the object is selected in the state manager
    assert (
        main_window._state_manager.get_current_object() == object_id
    ), "The object was not selected in the state manager"

    # Check that the object is highlighted in the document tree
    assert (
        tree_element.isSelected()
    ), "The object was not highlighted in the document tree"

    # Check document tree current item is the selected object
    assert (
        document_tree.currentItem() == tree_element
    ), "The document tree current item is not the selected object"

    # Check that the old object was different from the new object
    assert old_object != object_id, "The old object was the same as the new object"


def test_archetype_buttons_are_updated_on_object_selection(app):
    """
    Check that the archetype buttons are correctly updated when a new objects is selected.
    Use a document (accepts any children) and a paragraph (accepts no children) to check the buttons
    are correctly disabled/enabled.
    """

    # --------------------------------------------
    # Arrange
    # --------------------------------------------

    main_window: MainWindow = app

    paragraph_id = SampleData.get("simple_paragraph")
    document_id = SampleData.get("document_1")

    load_project(main_window=main_window)

    # Get tree elements out of the document tree
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )
    document_tree: DocumentTree = documents_container.tabs[document_id]
    section_tree_element: QTreeWidgetItem = document_tree.tree_items[document_id]
    paragraph_tree_element: QTreeWidgetItem = document_tree.tree_items[paragraph_id]

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click on the section tree element using the itemPressed signal
    document_tree.itemPressed.emit(section_tree_element, 0)

    # Store buttons state
    archetype_buttons_state_when_section_selected = []

    for _, button in main_window.main_menu.archetype_buttons.items():
        archetype_buttons_state_when_section_selected.append(button.isEnabled())

    # Click on the paragraph tree element using the itemPressed signal
    document_tree.itemPressed.emit(paragraph_tree_element, 0)

    # Store buttons state
    archetype_buttons_state_when_paragraph_selected = []

    for _, button in main_window.main_menu.archetype_buttons.items():
        archetype_buttons_state_when_paragraph_selected.append(button.isEnabled())

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check that the document buttons are enabled and the paragraph buttons are disabled
    assert all(
        [
            is_enabled_flag == True
            for is_enabled_flag in archetype_buttons_state_when_section_selected
        ]
    ), "There are disabled buttons when a section is selected"

    assert all(
        [
            is_enabled_flag == False
            for is_enabled_flag in archetype_buttons_state_when_paragraph_selected
        ]
    ), "There are enabled buttons when a paragraph is selected"


def test_archetype_buttons_selective_update_on_section_selection(app):
    """
    Check that every archetype but appendix is available to clone when a section is selected.

    # NOTE: This test is heavily dependent on the IR profile archetype list.
    """

    # --------------------------------------------
    # Arrange
    # --------------------------------------------

    main_window: MainWindow = app

    section_id = SampleData.get("simple_section")
    document_id = SampleData.get("document_1")

    load_project(main_window=main_window)

    # Get tree elements out of the document tree
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )
    document_tree: DocumentTree = documents_container.tabs[document_id]
    section_tree_element: QTreeWidgetItem = document_tree.tree_items[section_id]

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Click on the section tree element using the itemPressed signal
    document_tree.itemPressed.emit(section_tree_element, 0)

    # Store buttons state
    archetype_buttons_state_when_section_selected = []

    for _, button in main_window.main_menu.archetype_buttons.items():
        archetype_buttons_state_when_section_selected.append(button.isEnabled())

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check that every archetype but one (appendix) is enabled
    enabled_buttons_count = 0
    for is_enabled_flag in archetype_buttons_state_when_section_selected:
        if is_enabled_flag:
            enabled_buttons_count += 1

    assert (
        enabled_buttons_count == len(archetype_buttons_state_when_section_selected) - 1
    ), "There are more than one disabled button when a section is selected."

    # Check that the appendix button is disabled
    assert (
        main_window.main_menu.archetype_buttons["appendix"].isEnabled() == False
    ), "The appendix button is enabled when a section is selected."
