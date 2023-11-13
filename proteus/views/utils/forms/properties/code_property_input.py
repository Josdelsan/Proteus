# ==========================================================================
# File: code_property_input.py
# Description: Code property input widget for properties forms.
# Date: 10/11/2023
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

from proteus.model.properties.code_property import CodeProperty, ProteusCode
from proteus.views.utils.forms.properties.property_input import PropertyInput
from proteus.views.utils.forms.code_edit import CodeEdit


# --------------------------------------------------------------------------
# Class: CodePropertyInput
# Description: Code property input widget for properties forms.
# Date: 10/11/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class CodePropertyInput(PropertyInput):
    """
    Code property input widget for properties forms.
    """

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> ProteusCode:
        """
        Returns the value of the input widget. The value is converted to a
        ProteusCode object.
        """
        self.input: CodeEdit
        prefix, number, suffix = self.input.code()
        return ProteusCode(prefix=prefix, number=number, suffix=suffix)

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 10/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str:
        """
        Validates the input widget information. Returns None if the input is
        valid, otherwise returns the error message.
        """
        prefix, number, _ = self.input.code()
        
        if prefix == "":
            return "code_property_input.validator.error.prefix"

        try:
            int(number)
        except ValueError:
            return "code_property_input.validator.error.number_type"
        
        if int(number) <= 0:
            return "code_property_input.validator.error.number_value"

        # Return None if the input is valid
        return None

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 10/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(property: CodeProperty, *args, **kwargs) -> CodeEdit:
        """
        Creates the input widget based on CodeEdit custom widget.
        """
        input: CodeEdit = CodeEdit()
        code: ProteusCode = property.value
        input.setCode(prefix=code.prefix, number=code.number, suffix=code.suffix)
        return input
