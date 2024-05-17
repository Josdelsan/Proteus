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

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME
from proteus.views.components.main_window import MainWindow
from proteus.application.resources.translator import translate
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.end2end.fixtures import app, load_project, get_dialog

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# End to end property input validation tests
# --------------------------------------------------------------------------


# Property input validation is performed in views tests. This tests goal is to
# check the error messages are correctly handled and displayed in the UI.
@pytest.mark.parametrize(
    "property_name, property_value, expected_error",
    [
        ("string input", "]]>", "string_property_input.validator.error.cdata"),
        ("required string input", "", "property_input.validator.error.required"),
    ],
)
def test_property_input_validation(app, property_name, property_value, expected_error):
    """
    Test property input validation. Check that the error message is correctly
    displayed in the UI.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window)

    # Error message variable
    error_message: str = None

    # --------------------------------------------
    # Act
    # --------------------------------------------

    project_properties_button = main_window.main_menu.project_properties_button
    dialog: PropertyDialog = get_dialog(project_properties_button.click)

    # Change properties
    # NOTE: we can use setText() because we are using QLineEdit
    property_input = dialog.input_widgets[property_name]
    property_input.input.setText(property_value)

    # Store error label visibility before validation
    previous_label_hidden_state = property_input.error_label.isHidden()

    # Accept dialog
    dialog.accept_button.click()

    # Store error message and label visibility after validation
    error_message = dialog.input_widgets[property_name].error_label.text()
    current_label_hidden_state = property_input.error_label.isHidden()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check error message exists
    assert error_message is not None, "Error message not found"

    # Check error message is correct
    assert (
        translate(expected_error) == error_message
    ), f"Error message is '{error_message}' but should be '{translate(expected_error)}'"

    # Check error label visibility
    assert (
        previous_label_hidden_state is True
    ), "Error label is not hidden before validation"

    assert (
        current_label_hidden_state is False
    ), "Error label is hidden after validation"
