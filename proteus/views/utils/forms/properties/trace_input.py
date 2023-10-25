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

from proteus.model.trace import Trace
from proteus.controller.command_stack import Controller
from proteus.model.properties.property import Property
from proteus.views.utils.forms.properties.property_input import PropertyInput
from proteus.views.utils.forms.trace_edit import TraceEdit


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
    def create_input(self, property: Trace) -> None:
        """
        Creates the input widget based on TraceEdit.
        """
        self.input: TraceEdit = TraceEdit(controller=self.controller, accepted_sources=property.acceptedSources)
        self.input.setTraces(property.sources)
