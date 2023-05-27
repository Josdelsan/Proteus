# ==========================================================================
# File: update_properties.py
# Description: Command to update the properties of an element.
# Date: 27/05/2023
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

from PyQt6.QtGui import QUndoCommand

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.services.project_service import ProjectService


# --------------------------------------------------------------------------
# Class: UpdatePropertiesCommand
# Description: Command class to update the properties of an element.
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class UpdatePropertiesCommand(QUndoCommand):
    """
    Command class to update the properties of an element.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, element_id, properties, new_properties):
        super(UpdatePropertiesCommand, self).__init__()
        self.element_id : ProteusID = element_id
        self.old_properties : List = properties
        self.new_properties : List = new_properties

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the command, updating the properties of the element.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self):
        """
        Do the command, updating the properties of the element using the
        new properties.
        """
        ProjectService.update_properties(self.element_id, self.new_properties)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, updating the properties of the element
    #              to the previous state.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo the command, updating the properties of the element to the
        previous values.
        """
        ProjectService.update_properties(self.element_id, self.old_properties)