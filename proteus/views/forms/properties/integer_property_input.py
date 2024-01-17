# ==========================================================================
# File: integer_property_input.py
# Description: Integer property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QLineEdit,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.integer_property import IntegerProperty
from proteus.views.forms.properties.property_input import PropertyInput


# --------------------------------------------------------------------------
# Class: IntegerPropertyInput
# Description: Integer property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class IntegerPropertyInput(PropertyInput):
    """
    Integer property input widget for properties forms.
    """

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> int:
        """
        Returns the value of the input widget. The value is converted to a
        integer.
        """
        self.input: QLineEdit
        return int(self.input.text())

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str:
        """
        Validates the input widget. Returns an error message if the input
        has errors, None otherwise.
        """
        # Perform validation to prevent non-numeric values
        text = self.input.text()
        try:
            int(text)
        except ValueError:
            return "integer_property_input.validator.error"

        # Return None if the input is valid
        return None

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(property: IntegerProperty, *args, **kwargs) -> QLineEdit:
        """
        Creates the input widget based on QLineEdit.
        """
        input: QLineEdit = QLineEdit()
        input.setText(str(property.value))
        return input
