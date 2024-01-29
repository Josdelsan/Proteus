# ==========================================================================
# File: test_edit_project.py
# Description: pytest file for the PROTEUS pyqt edit project use case
# Date: 13/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QDialogButtonBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME
from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.end2end.fixtures import app, load_project, get_dialog

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# End to end "edit project" tests
# --------------------------------------------------------------------------


def test_edit_project(app):
    """
    Test the edit project use case. Edit an existing project changing its
    name and other properties. It tests the following steps:
        - Open the edit project dialog
        - Fill the form (name change)
        - Check project name change
        - Check dialog properties change
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Store previous title
    old_window_title = main_window.windowTitle()

    # Properties
    # NOTE: These are known existing properties
    NAME_PROP = PROTEUS_NAME
    VERSION_PROP = "version"
    DESCRIPTION_PROP = "description"

    # New values
    new_name = "New name"
    new_version = "3.0"
    new_description = "New description"

    # --------------------------------------------
    # Act
    # --------------------------------------------
    

    # Open project button click
    edit_project_button = main_window.main_menu.project_properties_button
    first_dialog: PropertyDialog = get_dialog(edit_project_button.click)

    # Store old name to compare window title
    old_name = first_dialog.input_widgets[NAME_PROP].get_value()

    # Change properties
    # NOTE: inputs types are known so we can use setText and setPlainText
    first_dialog.input_widgets[NAME_PROP].input.setText(new_name)
    first_dialog.input_widgets[VERSION_PROP].input.setText(new_version)
    first_dialog.input_widgets[DESCRIPTION_PROP].input.setMarkdown(new_description)

    # Accept dialog
    first_dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()
    first_dialog.deleteLater()


    # --------------------------------------------
    # Assert
    # --------------------------------------------

    assert_dialog: PropertyDialog = get_dialog(edit_project_button.click)

    # Check properties changed
    current_name = str(assert_dialog.input_widgets[NAME_PROP].get_value())
    current_version = str(assert_dialog.input_widgets[VERSION_PROP].get_value())
    current_description = str(assert_dialog.input_widgets[DESCRIPTION_PROP].get_value())

    assert_dialog.deleteLater()


    # Check title changed to replace old project name
    assert main_window.windowTitle() == old_window_title.replace(old_name, new_name), (
        f"Window title must include the new project name '{new_name}'"
        f"Current window title is'{main_window.windowTitle()}'"
    )

    # Check main menu buttons new state
    assert main_window.main_menu.save_button.isEnabled(), (
        "Save button must be enabled after editing a project"
        f"Current state is isEnabled() -> {main_window.main_menu.save_button.isEnabled()}"
    )

    # Check properties changed
    assert (
        current_name == new_name
    ), f"Project name must be '{new_name}' but it is '{current_name}'"
    assert (
        current_version == new_version
    ), f"Project version must be '{new_version}' but it is '{current_version}'"
    assert (
        current_description == new_description
    ), f"Project description must be '{new_description}' but it is '{current_description}'"
