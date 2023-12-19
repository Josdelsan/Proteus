# ==========================================================================
# File: time_property_input.py
# Description: Time property input widget for properties forms.
# Date: 15/11/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from datetime import time

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QTimeEdit,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.time_property import TimeProperty
from proteus.views.forms.properties.property_input import PropertyInput

# --------------------------------------------------------------------------
# Class: DatePropertyInput
# Description: Date property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class TimePropertyInput(PropertyInput):
    """
    Time property input widget for properties forms.
    """
        
    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> time:
        """
        Returns the value of the input widget. The value is converted to time.
        """
        self.input: QTimeEdit
        return self.input.time().toPyTime()

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str:
        """
        Time property input does not need validation because it is validated
        by the QTimeEdit widget.
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
    def create_input(property: TimeProperty, *args, **kwargs) -> QTimeEdit:
        """
        Creates the input widget based on QTimeEdit.
        """
        input: QTimeEdit = QTimeEdit()
        input.setTime(property.value)
        return input