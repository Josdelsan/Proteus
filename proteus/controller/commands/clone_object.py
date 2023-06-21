# ==========================================================================
# File: clone_object.py
# Description: Controller to clone an object from the project.
# Date: 06/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Union

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoCommand

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.views.utils.event_manager import EventManager, Event
from proteus.views.utils.state_manager import StateManager


# --------------------------------------------------------------------------
# Class: CloneObjectCommand
# Description: Controller class to clone an archetype object.
# Date: 06/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class CloneObjectCommand(QUndoCommand):
    """
    Controller class to clone an object.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, object_id: ProteusID):
        super(CloneObjectCommand, self).__init__()

        self.object_id: ProteusID = object_id
        self.before_clone_parent_state: ProteusState = None
        self.after_clone_parent_state: ProteusState = None
        self.cloned_object: Object = None

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the command, cloning the archetype object.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo the command, cloning the archetype object.
        """

        # NOTE: Must check if the operation was already performed once because
        #       cloning an object asigns a new ProteusID to the object, so if
        #       an edit operation is performed and undone we will not be able
        #       to redo if also undo is performed for the clone operation due
        #       to the ProteusID change.
        if self.cloned_object is None:
            # Set redo text
            self.setText(f"Clone object {self.object_id}")

            # Get the parent
            parent: Union[Project, Object] = ProjectService._get_element_by_id(
                self.object_id
            ).parent

            # Save the parent state before clone
            self.before_clone_parent_state: ProteusState = parent.state

            # Clone the object
            self.cloned_object: Object = ProjectService.clone_object(self.object_id)

            # Save the parent state after clone
            self.after_clone_parent_state = parent.state
        else:
            # Set redo text
            self.setText(f"Mark as ALIVE cloned object {self.cloned_object.id}")

            # Change the state of the cloned object and his children to FRESH
            ProjectService.change_state(self.cloned_object.id, ProteusState.FRESH)

            # Set the parent state to the state after clone stored in the first redo
            parent: Union[Project, Object] = ProjectService._get_element_by_id(self.object_id).parent
            parent.state: ProteusState = self.after_clone_parent_state

        # Emit the event to update the view
        EventManager.notify(Event.ADD_OBJECT, object=self.cloned_object)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, deleting the cloned object.
    # Date       : 02/06/2023
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo the command, deleting the cloned object.
        """
        # Set undo text
        self.setText(f"Mark as DEAD cloned object {self.cloned_object.id}")

        # Change the state of the cloned object and his children to DEAD
        ProjectService.change_state(self.cloned_object.id, ProteusState.DEAD)

        # Set the parent state to the old state
        parent: Union[Project, Object] = ProjectService._get_element_by_id(self.object_id).parent
        parent.state: ProteusState = self.before_clone_parent_state

        # Deselect the object in case it was selected to avoid errors
        StateManager.deselect_object(self.cloned_object.id)

        # Emit the event to update the view
        EventManager.notify(Event.DELETE_OBJECT, element_id=self.cloned_object.id)
