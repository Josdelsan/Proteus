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

from typing import List, Dict, Union

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
from proteus.model.properties import Property
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.application.events import (
    ModifyObjectEvent,
)

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
    def __init__(
        self,
        element_id: ProteusID,
        new_properties: List[Property],
        project_service: ProjectService,
    ):
        super(UpdatePropertiesCommand, self).__init__()

        # Dependency injection
        assert isinstance(
            project_service, ProjectService
        ), "Must provide a project service instance to the command"
        self.project_service = project_service

        # Check new properties
        assert isinstance(
            new_properties, List
        ), "The new properties must be provided as a list"

        # Create a list of properties
        self.new_properties: List[Property] = new_properties

        # Get the element to update
        self.element_id: ProteusID = element_id
        self.element: Union[Object, Project] = self.project_service._get_element_by_id(
            element_id
        )

        # Get old properties values before updating
        old_properties_dict: Dict[str, Property] = self.element.properties
        self.old_properties: List[Property] = [
            old_properties_dict[prop.name] for prop in self.new_properties
        ]

        # Get the old state of the element
        self.old_state: ProteusState = self.element.state

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
        self.project_service.update_properties(self.element_id, self.new_properties)

        # Notify the frontend components
        ModifyObjectEvent().notify(self.element_id)

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

        # Restore the properties of the element
        self.project_service.update_properties(self.element_id, self.old_properties)

        # Change the state of the element to the previous state
        self.element.state = self.old_state

        # Notify the frontend components
        ModifyObjectEvent().notify(self.element_id)