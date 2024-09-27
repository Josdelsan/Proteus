# ==========================================================================
# File: test_sort_children.py
# Description: pytest file for the PROTEUS pyqt sort children use case
# Date: 19/06/2024
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
from PyQt6.QtCore import QPoint

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME, PROTEUS_CODE
from proteus.views.components.main_window import MainWindow
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.dialogs.context_menu import ContextMenu
from proteus.tests.fixtures import SampleData
from proteus.tests.end2end.fixtures import (
    app,
    load_project,
    get_context_menu,
)

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

DOCUMENT_ID = SampleData.get("document_1")
SECTION_OBJECT_1 = SampleData.get("section_with_unsorted_children")
SECTION_OBJECT_2 = SampleData.get("section_with_unsorted_children_2")

# --------------------------------------------------------------------------
# End to end "sort children" tests
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "object_id, expected_order",
    [
        # NOTE: Names and number of children is defined in test sample data
        (SECTION_OBJECT_1, ['a', 'b', 'c', 'd']),
        (SECTION_OBJECT_2, ['A', 'CRQ-003 A', 'CRQ-004 A', 'D']),
    ],
)
def test_sort_children_alphabetically(app, object_id, expected_order):
    """
    Test the sort children use case. Sort children of a parent object
    alphabetically. It tests the following steps:
        - Select a parent object
        - Open the context menu
        - Select the sort children action
        - Check the children are sorted alphabetically
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    current_order = []
    section_object = main_window._controller.get_element(object_id)
    for child in section_object.get_descendants():
        current_order.append(child.get_property(PROTEUS_NAME).value)


    # --------------------------------------------
    # Act
    # --------------------------------------------
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    document_tree: DocumentTree = documents_container.tabs[DOCUMENT_ID]
    tree_element: QTreeWidgetItem = document_tree.tree_items[object_id]
    document_tree.setCurrentItem(tree_element)

    # Trigger context menu
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    context_menu.action_children_sort.trigger()

    # --------------------------------------------
    # Assert
    # --------------------------------------------
    
    # Check children are sorted alphabetically
    new_order = []
    for child in section_object.get_descendants():
        child_name: str = ""

        # Include proteus code if found
        if child.get_property(PROTEUS_CODE):
            child_name = child.get_property(PROTEUS_CODE).value.to_string() + " "

        child_name += child.get_property(PROTEUS_NAME).value

        new_order.append(child_name)

    assert new_order == expected_order, (
        "Children should be sorted alphabetically"
        f"Current order: {new_order}"
        f"Expected order: {expected_order}"
    )

    # Check the children changed their order
    assert current_order != new_order, (
        "Children should change their order"
        f"Current order: {new_order}"
        f"Expected order: {expected_order}"
    )

    assert main_window.main_menu.save_button.isEnabled(), (
        "Save button should be enabled after sorting children"
    )



@pytest.mark.parametrize(
    "object_id, expected_order",
    [
        # NOTE: Names and number of children is defined in test sample data
        (SECTION_OBJECT_1, ['d', 'c', 'b', 'a']),
        (SECTION_OBJECT_2, ['D', 'CRQ-004 A', 'CRQ-003 A', 'A']),
    ],
)
def test_sort_children_alphabetically_reverse(app, object_id, expected_order):
    """
    Test the sort children use case. Sort children of a parent object
    alphabetically reverse. It tests the following steps:
        - Select a parent object
        - Open the context menu
        - Select the sort children action
        - Check the children are sorted alphabetically
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    current_order = []
    section_object = main_window._controller.get_element(object_id)
    for child in section_object.get_descendants():
        current_order.append(child.get_property(PROTEUS_NAME).value)


    # --------------------------------------------
    # Act
    # --------------------------------------------
    documents_container: DocumentsContainer = (
        main_window.project_container.documents_container
    )

    # Right click arrange
    # NOTE: Clicking in a QMenu is not supported by pytest-qt
    # https://github.com/pytest-dev/pytest-qt/issues/195
    document_tree: DocumentTree = documents_container.tabs[DOCUMENT_ID]
    tree_element: QTreeWidgetItem = document_tree.tree_items[object_id]
    document_tree.setCurrentItem(tree_element)

    # Trigger context menu
    element_position: QPoint = document_tree.visualItemRect(tree_element).center()
    context_menu: ContextMenu = get_context_menu(
        lambda: document_tree.customContextMenuRequested.emit(element_position)
    )

    context_menu.action_children_sort_reverse.trigger()

    # --------------------------------------------
    # Assert
    # --------------------------------------------
    
    # Check children are sorted alphabetically
    new_order = []
    for child in section_object.get_descendants():
        child_name: str = ""

        # Include proteus code if found
        if child.get_property(PROTEUS_CODE):
            child_name = child.get_property(PROTEUS_CODE).value.to_string() + " "

        child_name += child.get_property(PROTEUS_NAME).value

        new_order.append(child_name)

    assert new_order == expected_order, (
        "Children should be sorted alphabetically reverse"
        f"Current order: {new_order}"
        f"Expected order: {expected_order}"
    )

    # Check the children changed their order
    assert current_order != new_order, (
        "Children should change their order"
        f"Current order: {new_order}"
        f"Expected order: {expected_order}"
    )

    assert main_window.main_menu.save_button.isEnabled(), (
        "Save button should be enabled after sorting children"
    )
