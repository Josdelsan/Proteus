# ==========================================================================
# File: url_property_input.py
# Description: Url property input widget for properties forms.
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

from proteus.model.properties.url_property import UrlProperty
from proteus.views.forms.properties.property_input import PropertyInput


# --------------------------------------------------------------------------
# Class: UrlPropertyInput
# Description: Url property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class UrlPropertyInput(PropertyInput):
    """
    Url property input widget for properties forms.
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
        url.
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
        url: str = self.get_value()

        # Check if text contains CDATA section delimiters
        if url.find("<![CDATA[") != -1 or url.find("]]>") != -1:
            return "url_property_input.validator.error.cdata"
        
        # Check required
        if self.property.required and (url == None or url == ""):
            return "property_input.validator.error.required"
        
        return None

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(property: UrlProperty, *args, **kwargs) -> QLineEdit:
        """
        Creates the input widget based on QLineEdit.
        """
        input: QLineEdit = QLineEdit()
        input.setText(property.value)
        return input
