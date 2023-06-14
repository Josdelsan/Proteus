# ==========================================================================
# File: change_object_position.py
# Description: Controller to change the position of an object.
# Date: 13/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Union, List

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


# --------------------------------------------------------------------------
# Class: CloneArchetypeDocumentCommand
# Description: Controller class to clone an archetype object.
# Date: 13/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ChangeObjectPositionCommand(QUndoCommand):
    """
    Controller class to change the position of an object.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 13/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self, object_id: ProteusID, new_position: int, new_parent_id: ProteusID
    ):
        super(ChangeObjectPositionCommand, self).__init__()

        # Object to apply position change
        self.object: Object = ProjectService._get_element_by_id(object_id)

        # Old parent information
        self.old_parent: Union[Project, Object] = self.object.parent
        self.old_position: int = None
        self.old_parent_state: ProteusState = self.old_parent.state

        # New parent information
        self.new_parent: Union[Project, Object] = ProjectService._get_element_by_id(
            new_parent_id
        )
        self.new_position: int = new_position
        self.new_parent_state: ProteusState = self.new_parent.state

        # Set old position relative to non DEAD objects
        alive_siblings: List[Object] = [
            d
            for d in self.object.parent.get_descendants()
            if d.state != ProteusState.DEAD
        ]
        self.old_position = alive_siblings.index(self.object)
        # Normalize position
        if self.old_position > self.new_position:
            self.old_position += 1

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the command, changing the position of the object.
    # Date       : 13/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo the command, changing the position of the object.
        """

        # Set redo text
        self.setText(f"Change position of {self.object.id} to {self.new_position}")

        # Call ProjectService method
        ProjectService.change_object_position(
            self.object.id, self.new_position, self.new_parent
        )

        # Notify a deletion and add object event
        EventManager.notify(Event.DELETE_OBJECT, element_id=self.object.id)
        EventManager.notify(Event.ADD_OBJECT, object=self.object)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, changing the position of the object to
    #              the previous one.
    # Date       : 13/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo the command, changing the position of the object to the previous one.
        """

        # Set undo text
        self.setText(f"Change position of {self.object.id} to {self.old_position}")

        # Call ProjectService method
        ProjectService.change_object_position(
            self.object.id, self.old_position, self.old_parent
        )

        # Restore the state of the old and new parent
        self.old_parent.state = self.old_parent_state
        self.new_parent.state = self.new_parent_state

        # Notify a deletion and add object event
        EventManager.notify(Event.DELETE_OBJECT, element_id=self.object.id)
        EventManager.notify(Event.ADD_OBJECT, object=self.object)
