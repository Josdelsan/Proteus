# ==========================================================================
# File: trace_input.py
# Description: Trace input widget for properties forms.
# Date: 25/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.properties import TraceProperty
from proteus.controller.command_stack import Controller
from proteus.views.forms.properties.property_input import PropertyInput
from proteus.views.forms.trace_edit import TraceEdit


# --------------------------------------------------------------------------
# Class: TraceInput
# Description: Trace input widget for properties forms.
# Date: 25/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class TraceInput(PropertyInput):
    """
    Trace input widget for properties forms.
    """

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> List:
        """
        Returns the value of the input widget. The value is converted to a
        list.
        """
        self.input: TraceEdit
        return self.input.traces()

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 25/10/2023
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
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(property: TraceProperty, controller: Controller, element_id: ProteusID, *args, **kwargs) -> TraceEdit:
        """
        Creates the input widget based on PROTEUS TraceEdit.
        """
        input: TraceEdit = TraceEdit(
            element_id=element_id, controller=controller, accepted_targets=property.acceptedTargets, limit=property.max_targets_number
        )
        input.setTraces(property.value)
        return input
