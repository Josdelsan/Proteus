# ==========================================================================
# File: clone_archetype_object.py
# Description: Command to clone an archetype object.
# Date: 01/06/2023
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
from proteus.model.object import Object
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.services.archetype_service import ArchetypeService
from proteus.views.utils.event_manager import EventManager, Event

# --------------------------------------------------------------------------
# Class: CloneArchetypeObjectCommand
# Description: Command class to clone an archetype object.
# Date: 01/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class CloneArchetypeObjectCommand(QUndoCommand):
    """
    Command class to clone an archetype object.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, archetype_id, parent_id):
        super(CloneArchetypeObjectCommand, self).__init__()

        self.archetype_id : ProteusID = archetype_id
        self.parent_id : ProteusID = parent_id
        self.cloned_object : Object = None
    

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
        # Set redo text
        self.setText(f"Clone archetype object {self.archetype_id} to {self.parent_id}")

        # Get the parent and project object
        parent = ProjectService._get_element_by_id(self.parent_id)
        project = ProjectService.project

        # Clone the archetype object
        self.cloned_object = ArchetypeService.create_object(self.archetype_id, parent, project)

        # Emit the event to update the view
        EventManager.notify(Event.CLONE_OBJECT, cloned_object=self.cloned_object)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, deleting the cloned object.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo the command, deleting the cloned object.
        """
        # Set undo text
        self.setText(f"Delete cloned object {self.cloned_object.id}")

        # Delete the object and its children
        for child in self.cloned_object.get_descendants():
            delete_object(child)

        # Remove the object from the parent
        parent = ProjectService._get_element_by_id(self.parent_id)
        parent.get_descendants().remove(self.cloned_object)

        # Store the id and delete the object
        element_id = self.cloned_object.id
        del self.cloned_object

        # Emit the event to update the view
        EventManager.notify(Event.DELETE_OBJECT, element_id=element_id)


def delete_object(object : Object):
    for child in object.get_descendants():
        delete_object(child)
    del object