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
from PyQt6.QtWidgets import QDialogButtonBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME
from proteus.views.components.main_window import MainWindow
from proteus.utils.translator import Translator
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.tests.end2end.fixtures import app, load_project, get_dialog

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# End to end property input validation tests
# --------------------------------------------------------------------------


# NOTE: PropertyInput would need a set_value() method to be able to
# test validation of different property types in the same test. This would
# only be use in testing.
# TODO: This validation must not be performed as an end2end test. This has to
# be implement as PropertyInput unit test mocking input widgets if necessary.
@pytest.mark.parametrize(
    "property_name, property_value, expected_error",
    [
        (PROTEUS_NAME, "", "property_input.validator.error.required"),  # stringProperty
        (PROTEUS_NAME, None, "property_input.validator.error.required"),
        ("string input", "]]>", "string_property_input.validator.error.cdata"),
        ("string input", "<![CDATA[", "string_property_input.validator.error.cdata"),
        ("string input", "<![CDATA[dummy cdata]]>", "string_property_input.validator.error.cdata"),
        ("float input", "", "float_property_input.validator.error"),  # floatProperty
        ("float input", None, "float_property_input.validator.error"),
        ("float input", "a", "float_property_input.validator.error"),
        ("float input", "1.2.3", "float_property_input.validator.error"),
        ("float input", "1.2a", "float_property_input.validator.error"),
        ("int input", "", "integer_property_input.validator.error"),  # intProperty
        ("int input", None, "integer_property_input.validator.error"),
        ("int input", "a", "integer_property_input.validator.error"),
        ("int input", "1.2", "integer_property_input.validator.error"),
        ("int input", "1a", "integer_property_input.validator.error"),
        ("url input", "]]>", "url_property_input.validator.error.cdata"),  # urlProperty
        ("url input", "<![CDATA[", "url_property_input.validator.error.cdata"),
        ("url input", "https://url.url/]]>/", "url_property_input.validator.error.cdata"),
        
        # Required validation
        ("required string input", "", "property_input.validator.error.required"),
        ("required string input", None, "property_input.validator.error.required"),
        ("required url input", "", "property_input.validator.error.required"),
        ("required url input", None, "property_input.validator.error.required"),
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
    dialog.input_widgets[property_name].input.setText(property_value)

    # Accept dialog
    dialog.button_box.button(QDialogButtonBox.StandardButton.Save).click()

    # Store error message
    error_message = dialog.input_widgets[property_name].error_label.text()


    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check error message exists
    assert error_message is not None, "Error message not found"

    # Check error message is correct
    assert (
        Translator().text(expected_error) == error_message
    ), f"Error message is '{error_message}' but should be '{Translator().text(expected_error)}'"
