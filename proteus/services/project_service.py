# ==========================================================================
# File: project_service.py
# Description: Project interface
# Date: 06/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Union, List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.properties import Property

# --------------------------------------------------------------------------
# Class: ProjectService
# Description: Class for project operations interface
# Date: 06/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@dataclass
class ProjectService():
    """
    Acts as an interface for project, documents and objects operations.
    Loads a project into memory and provides methods to perform operations.
    """

    project       : Project                 = None
    project_index : Dict[ProteusID, Object] = field(default_factory=dict)

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Initializes the project service with the given project
    #              path.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__ (self, project_path: str) -> None:
        """
        Initializes the project service with the given project path. Force
        the load of every object in the project to store it in a dictionary
        for easy access.

        :param project_path: Path to the project directory.
        """
        # Helper function to populate the project index
        def populate_index (object: Object) -> None:
            self.project_index[object.id] = object

            for child in object.children:
                populate_index(child)

        # Load project
        self.project = Project.load(project_path)

        # Load project index, this forces load for
        # every object in the project
        for document in self.project.documents:
            populate_index(document)

        # Include project in the index
        self.project_index[self.project.id] = self.project

    # ----------------------------------------------------------------------
    # Method     : get_properties
    # Description: Returns the project or object properties properties.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_project_properties (self, element_id : ProteusID) -> Dict[str, Property]:
        """
        Returns the project or object properties.

        :param element_id: Id of the project or object.
        """
        element = self._get_element_by_id(element_id)

        return element.properties
        
    # ----------------------------------------------------------------------
    # Method     : update_properties
    # Description: Updates the project or object properties.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_properties (self, element_id : ProteusID, properties: List[Property]) -> None:
        """
        Updates the project or object properties.

        :param element_id: Id of the project or object.
        :param properties: List of properties to update.
        """
        element = self._get_element_by_id(element_id)

        for property in properties:
            element.set_property(property)

    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: Saves the project to disk.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_project (self) -> None:
        """
        Saves the project to disk.
        """
        self.project.save()

    # ----------------------------------------------------------------------
    # Method     : delete_object
    # Description: Deletes the object with the given id from the project.
    #              Changes are not saved to disk until save_project is
    #              called.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_object (self, object_id: ProteusID) -> None:
        """
        Deletes the object with the given id from the project. Changes are
        not saved to disk until save_project is called.

        :param object_id: Id of the object to delete.
        """
        # Get object using helper method
        object = self._get_element_by_id(object_id)

        object.delete()

    # ----------------------------------------------------------------------
    # Method     : _get_element
    # Description: Helper method that returns the project or object with
    #              the given id.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _get_element_by_id (self, element_id: ProteusID) -> Union[Project, Object]:
        """
        Returns the project or object with the given id.

        :param element_id: Id of the project or object.
        """
        assert element_id in self.project_index, \
            f"Element with id {element_id} not found."

        return self.project_index[element_id]