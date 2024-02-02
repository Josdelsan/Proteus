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


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.boolean_property import BooleanProperty
from proteus.views.forms.properties.property_input import PropertyInput
from proteus.views.forms.boolean_edit import BooleanEdit


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
        self.input: BooleanEdit
        return self.input.checked()

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
        is  empty, None otherwise. Qt checkboxes value cannot be None,
        anyways is checked.
        """
        
        if self.get_value() is None:
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
    def create_input(property: BooleanProperty, *args, **kwargs) -> BooleanEdit:
        """
        Creates the input widget based on QCheckBox.
        """
        input: BooleanEdit = BooleanEdit(tooltip=property.tooltip)
        input.setChecked(property.value)
        return input
