# ==========================================================================
# File: sort_children.py
# Description: Controller to sort the children of an object.
# Date: 17/06/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoCommand

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.services.project_service import ProjectService
from proteus.application.events import (
    SortChildrenEvent,
)

# --------------------------------------------------------------------------
# Class: SortChildrenCommand
# Description: Controller class to sort the children of an object.
# Date: 17/06/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class SortChildrenCommand(QUndoCommand):
    """
    Controller class to sort the children of an object/document.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 17/06/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        object_id: ProteusID,
        reverse: bool,
        project_service: ProjectService,
    ):
        """
        Class constructor, invoke the parents class constructors.
        """
        super(SortChildrenCommand, self).__init__()

        # Dependency injection
        assert isinstance(
            project_service, ProjectService
        ), "Must provide a project service instance to the command"
        self.project_service = project_service

        # Object to sort children
        self.object: Object = self.project_service._get_element_by_id(object_id)

        # Reverse flag
        self.reverse = reverse

        # Old children order
        self.old_children_list = self.object.get_descendants().copy()

        # Object previous state
        self.old_object_state = self.object.state


    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the command, sorting the children of the object.
    # Date       : 17/06/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo the command, sorting the children of the object.
        """

        # Sort children
        self.project_service.sort_children_by_name(self.object.id, self.reverse)

        SortChildrenEvent().notify(self.object.id, update_view=True)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, restoring the previous children order.
    # Date       : 17/06/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo the command, restoring the previous children order.
        """

        # Restore previous children order
        self.object._children = self.old_children_list.copy()

        # Restore object state
        self.object.state = self.old_object_state

        SortChildrenEvent().notify(self.object.id, update_view=True)

        
        
        