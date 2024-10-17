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

from typing import Union, Set

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
from proteus.application.state.manager import StateManager
from proteus.application.events import (
    AddObjectEvent,
    DeleteObjectEvent,
)

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
    def __init__(self, object_id: ProteusID, new_parent_id: ProteusID, project_service: ProjectService):
        super(CloneObjectCommand, self).__init__()

        # Dependency injection
        assert isinstance(
            project_service, ProjectService
        ), "Must provide a project service instance to the command"
        self.project_service = project_service

        # Command attributes
        self.object_id: ProteusID = object_id
        self.new_parent_id: ProteusID = new_parent_id
        self.before_clone_parent_state: ProteusState = None
        self.after_clone_parent_state: ProteusState = None
        self.cloned_object: Object = None

        # This will help to redo the command if the operation was already performed
        # in order to avoid setting FRESH state to cloned object children that are 
        # were not part of the original clone operation.
        self.cloned_objects_list: Set[ProteusID] = set()

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

            # Get the new parent
            parent: Union[Project, Object] = self.project_service._get_element_by_id(
                self.new_parent_id
            )

            # Save the new parent state before clone
            self.before_clone_parent_state: ProteusState = parent.state

            # Clone the object
            self.cloned_object: Object = self.project_service.clone_object(self.object_id, self.new_parent_id)

            # Get the list of cloned objects in this operation
            self.cloned_objects_list = self.cloned_object.get_ids()

            # Save the new parent state after clone
            self.after_clone_parent_state = parent.state
        else:
            # Set redo text
            self.setText(f"Mark as ALIVE cloned object {self.cloned_object.id}")

            # Change the state of the cloned object and his children to FRESH
            for id in self.cloned_objects_list:
                self.project_service._get_element_by_id(id).state = ProteusState.FRESH

            # Set the new parent state to the state after clone stored in the first redo
            parent: Union[Project, Object] = self.project_service._get_element_by_id(self.new_parent_id)
            parent.state = self.after_clone_parent_state

        # Emit the event to update the view
        AddObjectEvent().notify(self.cloned_object.id)

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
        for id in self.cloned_objects_list:
            self.project_service._get_element_by_id(id).state = ProteusState.DEAD

        # Set the new parent state to the old state
        parent: Union[Project, Object] = self.project_service._get_element_by_id(self.new_parent_id)
        parent.state = self.before_clone_parent_state

        # Deselect the object in case it was selected to avoid errors
        StateManager().deselect_object(self.cloned_object.id)

        # Emit the event to update the view
        DeleteObjectEvent().notify(self.cloned_object.id)