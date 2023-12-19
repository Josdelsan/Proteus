# ==========================================================================
# File: enum_property_input.py
# Description: Enum property input widget for properties forms.
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
    QComboBox,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils.translator import Translator
from proteus.model.properties.enum_property import EnumProperty
from proteus.views.forms.properties.property_input import PropertyInput


# --------------------------------------------------------------------------
# Class: EnumPropertyInput
# Description: Enum property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class EnumPropertyInput(PropertyInput):
    """
    Enum property input widget for properties forms.
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
        enum.
        """
        self.input: QComboBox
        return self.input.currentData()

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
        pass

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(property: EnumProperty, *args, **kwargs) -> QComboBox:
        """
        Creates the input widget based on QComboBox.
        """
        input: QComboBox = QComboBox()
        choices = property.get_choices_as_set()
        # Add choices translated
        for choice in choices:
            input.addItem(Translator().text(choice), choice)
        # Set current choice
        input.setCurrentText(Translator().text(property.value))
        return input
