# ==========================================================================
# File: test_info_dialog.py
# Description: pytest file for the PROTEUS pyqt new view dialog
# Date: 04/04/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.new_view_dialog import NewViewDialog
from proteus.tests.end2end.fixtures import app, get_dialog, load_project


# --------------------------------------------------------------------------
# End to end "new view dialog" tests
# --------------------------------------------------------------------------
# NOTE: ViewsContainer class is mostly mocked due to QWebEngine issues with pytest


def test_new_view_dialog(app):
    """
    Test the new view dialog opening and closing.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------

    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Get add view button
    views_container = main_window.project_container.views_container
    add_view_button = views_container.add_view_button

    # --------------------------------------------
    # Act
    # --------------------------------------------
    dialog: NewViewDialog = get_dialog(add_view_button.click)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    assert dialog.view_combo.count() > 0, "No views available in the combo box."

    dialog.reject_button.click()

@pytest.mark.skip("Temporary disabled because test data changed")
def test_new_view_dialog_add_view(app):
    """
    Test adding a new view to the views container using the new view dialog.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------

    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Get add view button
    views_container = main_window.project_container.views_container
    add_view_button = views_container.add_view_button

    # NOTE: It is known that the example_project has 'remus' view and current
    # profile has 'figures' view available.
    NEW_VIEW_NAME = "figures"
    previous_tabs: List[str] = list(views_container.tabs.keys())

    # --------------------------------------------
    # Act
    # --------------------------------------------
    dialog: NewViewDialog = get_dialog(add_view_button.click)

    data_index = dialog.view_combo.findData(NEW_VIEW_NAME)
    dialog.view_combo.setCurrentIndex(data_index)

    dialog.accept_button.click()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    new_tabs_list: List[str] = list(views_container.tabs.keys())

    assert (
        NEW_VIEW_NAME in views_container.tabs
    ), f"View '{NEW_VIEW_NAME}' not added to views container."

    assert (
        len(new_tabs_list) == len(previous_tabs) + 1
    ), f"Number of views did not increase by 1."

    assert (
        new_tabs_list[-1] == NEW_VIEW_NAME
    ), f"New view '{NEW_VIEW_NAME}' not added at the end of the tabs list."

    assert all(
        tab in views_container.tabs for tab in previous_tabs
    ), "Previous tabs were not preserved."


@pytest.mark.skip("Temporary disabled because test data changed")
def test_new_view_dialog_view_description_change(app):
    """
    Test changing the view description in the new view dialog.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------

    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Get add view button
    views_container = main_window.project_container.views_container
    add_view_button = views_container.add_view_button

    dialog: NewViewDialog = get_dialog(add_view_button.click)

    old_description = str(dialog.description_content_label.text())

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Change view to another one
    # Tests will fail if less than 2 views or both has no description/same description
    # This is not supposed to happen in the example project/ profile
    current_index = dialog.view_combo.currentIndex()
    if current_index == 0:
        dialog.view_combo.setCurrentIndex(1)
    else:
        dialog.view_combo.setCurrentIndex(0)

    new_description = str(dialog.description_content_label.text())

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check both descriptions are not empty
    assert old_description, "Old description is empty."
    assert new_description, "New description is empty."

    # Check both descriptions are different
    assert (
        old_description != new_description
    ), f"Descriptions are the same. '{old_description}' == '{new_description}'"

    dialog.reject_button.click()
