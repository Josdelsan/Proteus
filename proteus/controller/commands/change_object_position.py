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
from proteus.utils.events import (
    AddObjectEvent,
    DeleteObjectEvent,
)

# --------------------------------------------------------------------------
# Class: ChangeObjectPositionCommand
# Description: Controller class to change the position of an object.
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
        self,
        object_id: ProteusID,
        new_position: int,
        new_parent_id: ProteusID,
        project_service: ProjectService,
    ):
        super(ChangeObjectPositionCommand, self).__init__()
        # Dependency injection
        assert isinstance(
            project_service, ProjectService
        ), "Must provide a project service instance to the command"
        self.project_service = project_service

        # Object to apply position change
        self.object: Object = self.project_service._get_element_by_id(object_id)

        # Old parent information
        self.old_parent: Object = self.object.parent
        self.old_parent_descendants: List[
            Object
        ] = self.old_parent.get_descendants().copy()
        self.old_parent_state: ProteusState = self.old_parent.state

        # New parent information
        self.new_parent: Object = self.project_service._get_element_by_id(new_parent_id)
        self.new_position: int = new_position
        self.new_parent_state: ProteusState = self.new_parent.state

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
        self.setText(
            f"Change position of {self.object.id} to {self.new_position} in parent {self.new_parent.id}"
        )

        # Call ProjectService method
        self.project_service.change_object_position(
            self.object.id, self.new_position, self.new_parent.id
        )

        # Notify a deletion and add object event
        DeleteObjectEvent().notify(self.object.id, False)
        AddObjectEvent().notify(self.object.id)


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
        self.setText(
            f"Change position of {self.object.id} to original position and parent"
        )

        # Pop the object from the new parent, calculate the position in case
        # it was None to add it to the end of the list
        position: int = self.new_parent.get_descendants().index(self.object)
        self.new_parent.get_descendants().pop(position)

        # Restore descendants of the old parent
        # NOTE: Accessing private attribute _children is not recommended, but
        #       it is the only way to restore the state of the old parent since
        #       the service method does not take into account DEAD objects correctly
        self.old_parent._children = self.old_parent_descendants.copy()

        # Set the object parent to the old parent
        self.object.parent = self.old_parent

        # Restore the state of the old and new parent
        self.old_parent.state = self.old_parent_state
        self.new_parent.state = self.new_parent_state

        # Notify a deletion and add object event
        DeleteObjectEvent().notify(self.object.id, False)
        AddObjectEvent().notify(self.object.id)
