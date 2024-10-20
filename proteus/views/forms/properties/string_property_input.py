# ==========================================================================
# File: string_property_input.py
# Description: String property input widget for properties forms.
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

from proteus.model import PROTEUS_NAME
from proteus.model.properties.string_property import StringProperty
from proteus.views.forms.properties.property_input import PropertyInput


# --------------------------------------------------------------------------
# Class: StringPropertyInput
# Description: String property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class StringPropertyInput(PropertyInput):
    """
    String property input widget for properties forms.
    """

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> str:
        """
        Returns the value of the input widget. The value is converted to a
        string.
        """
        self.input: QLineEdit
        return self.input.text()

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str | None:
        """
        Validates the input widget. Returns an error message if the input
        has errors, None otherwise.
        """
        # Get the input text
        text = self.input.text()

        # Get Property or Trace name
        name = self.property.name

        # Check if the input is valid (not None)
        # Check if the input is required
        # :Proteus-name is always required
        # TODO: Consider if :Proteus-name must be checked or we can
        # assume that the archetypes will always include required=True
        # in this mandatory property
        if (
            text is None
            or (self.property.required and text == "")
            or (name == PROTEUS_NAME and text == "")
        ):
            return "property_input.validator.error.required"

        # Check if text contains CDATA section delimiters
        if text.find("<![CDATA[") != -1 or text.find("]]>") != -1:
            return "string_property_input.validator.error.cdata"

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
    def create_input(property: StringProperty, *args, **kwargs) -> QLineEdit:
        """
        Creates the input widget based on QLineEdit.
        """
        input: QLineEdit = QLineEdit()
        input.setText(property.value)
        return input
