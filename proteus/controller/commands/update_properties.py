# ==========================================================================
# File: update_properties.py
# Description: Controller to update the properties of an element.
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
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.views.utils.event_manager import EventManager, Event


# --------------------------------------------------------------------------
# Class: UpdatePropertiesCommand
# Description: Controller class to update the properties of an element.
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class UpdatePropertiesCommand(QUndoCommand):
    """
    Controller class to update the properties of an element.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, element_id, new_properties):
        super(UpdatePropertiesCommand, self).__init__()

        # Get the old properties before updating the properties
        old_properties_dict = ProjectService.get_properties(element_id)
        old_properties = [old_properties_dict[prop.name] for prop in new_properties]

        self.element_id : ProteusID = element_id
        self.old_properties : List = old_properties
        self.old_state : ProteusState = ProjectService._get_element_by_id(element_id).state
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
        # Set redo command text
        self.setText(f"Update properties of {self.element_id}")

        # Update the properties of the element and change its state
        ProjectService.update_properties(self.element_id, self.new_properties)

        # Notify the frontend components
        EventManager().notify(event=Event.MODIFY_OBJECT, element_id=self.element_id)


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
        # Set undo command text
        self.setText(f"Undo update properties of {self.element_id}")

        # Update the properties of the element
        ProjectService.update_properties(self.element_id, self.old_properties)

        # Change the state of the element to the previous state
        ProjectService._get_element_by_id(self.element_id).state = self.old_state

        # Notify the frontend components
        EventManager().notify(event=Event.MODIFY_OBJECT, element_id=self.element_id)