# ==========================================================================
# File: date_property_input.py
# Description: Date property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from datetime import date

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QDateEdit,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.date_property import DateProperty
from proteus.views.utils.forms.properties.property_input import PropertyInput

# --------------------------------------------------------------------------
# Class: DatePropertyInput
# Description: Date property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DatePropertyInput(PropertyInput):
    """
    Date property input widget for properties forms.
    """
        
    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> date:
        """
        Returns the value of the input widget. The value is converted to a
        date.
        """
        return self.input.date().toPyDate()

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str:
        """
        Date property input does not need validation because it is validated
        by the QDateEdit widget.
        """
        pass

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_input(self, property: DateProperty) -> None:
        """
        Creates the input widget based on QDateEdit.
        """
        self.input: QDateEdit = QDateEdit()
        self.input.setDate(property.value)