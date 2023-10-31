# ==========================================================================
# File: boolean_property_input.py
# Description: Boolean property input widget for properties forms.
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
    QCheckBox,
)
from PyQt6.QtCore import (
    Qt,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.boolean_property import BooleanProperty
from proteus.views.utils.forms.properties.property_input import PropertyInput


# --------------------------------------------------------------------------
# Class: BooleanPropertyInput
# Description: Boolean property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class BooleanPropertyInput(PropertyInput):
    """
    Boolean property input widget for properties forms.
    """

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> bool:
        """
        Returns the value of the input widget. The value is converted to a
        boolean.
        """
        return self.input.isChecked()

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str:
        """
        Boolean property input does not need validation because it is validated
        by the QCheckBox widget.
        """
        pass

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_input(self, property: BooleanProperty) -> None:
        """
        Creates the input widget based on QCheckBox.
        """
        self.input: QCheckBox = QCheckBox()
        state = (
            Qt.CheckState.Checked if bool(property.value) else Qt.CheckState.Unchecked
        )
        self.input.setCheckState(state)
