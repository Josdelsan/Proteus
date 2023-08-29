# ==========================================================================
# File: test_property_input_validation.py
# Description: pytest file for the PROTEUS pyqt property input validation
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
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QDialogButtonBox, QApplication

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.main_window import MainWindow
from proteus.views.utils.translator import Translator
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.end2end.fixtures import app, load_project

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "example_project"

# --------------------------------------------------------------------------
# End to end property input validation tests
# --------------------------------------------------------------------------


# NOTE: PropertyInputWidget would need a set_value() method to be able to
# test validation of different property types in the same test. This would
# only be use in testing.
@pytest.mark.parametrize(
    "property_name, property_value, expected_error",
    [
        ("name", "", "string_property_input.validator.error"),  # stringProperty
        ("name", None, "string_property_input.validator.error"),
        ("version", "", "float_property_input.validator.error"),  # floatProperty
        ("version", None, "float_property_input.validator.error"),
        ("version", "a", "float_property_input.validator.error"),
        ("version", "1.2.3", "float_property_input.validator.error"),
        ("version", "1.2a", "float_property_input.validator.error"),
        ("numberOfUsers", "", "integer_property_input.validator.error"),  # intProperty
        ("numberOfUsers", None, "integer_property_input.validator.error"),
        ("numberOfUsers", "a", "integer_property_input.validator.error"),
        ("numberOfUsers", "1.2", "integer_property_input.validator.error"),
        ("numberOfUsers", "1a", "integer_property_input.validator.error"),
    ],
)
def test_property_input_validation(app, property_name, property_value, expected_error):
    """
    Test the property input validation in the property dialog.
    This tests covers PropertyDialog so it is not necessary to test
    project, document and object dialogs separately.

    This test is parametrized to test different properties types that
    peform validation. Other property types might not perform validation
    or use PyQt6 built-in validation for their input widgets.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window, project_name=PROJECT_NAME)

    # Error message variable
    error_message: str = None

    # --------------------------------------------
    # Act
    # --------------------------------------------
    # Handle form filling
    def handle_dialog():
        dialog: PropertyDialog = QApplication.activeModalWidget()
        while not dialog:
            dialog = QApplication.activeModalWidget()

        # Change properties
        # NOTE: we can use setText() because we are using QLineEdit
        dialog.input_widgets[property_name].input.setText(property_value)

        # Accept dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()

        # Store error message
        nonlocal error_message
        error_message = dialog.input_widgets[property_name].error_label.text()

        # Close the dialog
        dialog.button_box.button(QDialogButtonBox.StandardButton.Cancel).click()

    # Edit project properties
    QTimer.singleShot(5, handle_dialog)  # Wait for the dialog to be created
    main_window.main_menu.project_properties_button.click()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check error message exists
    assert error_message is not None, "Error message not found"

    # Check error message is correct
    assert (
        Translator().text(expected_error) == error_message
    ), f"Error message is '{error_message}' but should be '{Translator().text(expected_error)}'"
