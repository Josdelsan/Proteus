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
        # Load project
        self.project = Project.load(project_path)

        # Initialize project index
        self.project_index = {}

        # Populate project index
        self._populate_index()

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
        # Populate index to check for new objects
        if element_id not in self.project_index:
            self._populate_index()

        # Check if the element is in the index
        assert element_id in self.project_index, \
            f"Element with id {element_id} not found."

        # Return the element
        return self.project_index[element_id]
    
    # ----------------------------------------------------------------------
    # Method     : _populate_index
    # Description: Helper method that populates the project index with
    #              the all the objects in the project. If an object was
    #              already in the index, it will be ignored.
    # Date       : 07/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _populate_index (self) -> None:
        """
        Populates the project index with the all the objects in the project.
        If an object was already in the index, it will be ignored.
        """
        def _populate_index_private (object: Object) -> None:
            """
            Private helper method that populates the project index with
            the all the objects in the project recursively.

            :param object: Object to add to the index.
            """
            # If the object is not in the index, add it
            if object.id not in self.project_index:
                self.project_index[object.id] = object

            # Add children to the index
            for child in object.children.values():
                _populate_index_private(child)

        # Load project index, this forces load for
        # every object in the project
        for document in self.project.documents.values():
            _populate_index_private(document)

        # Include project in the index if it is not there
        if self.project.id not in self.project_index:
            self.project_index[self.project.id] = self.project

    # ----------------------------------------------------------------------
    # Method     : get_properties
    # Description: Returns the project or object properties properties.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_properties (self, element_id : ProteusID) -> Dict[str, Property]:
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
    # Method     : get_object_structure
    # Description: Returns the object structure as a tree.
    # Date       : 08/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_structure (self, object_id: ProteusID) -> Dict[ProteusID, Dict]:
        """
        Returns the element structure as a tree. Each element is represented
        by a dictionary with the following structure: {id: {id: id, ...}, ...}

        :param element_id: Id of the element.
        """
        # TODO: Return the object structure using a more verbose format like
        #       a name property or similar.

        # Get object using helper method
        object : Object = self._get_element_by_id(object_id)

        # Check that the element is an object
        assert isinstance(object, Object), \
            f"Element with id {object_id} is not an object."
        
        # Initialize an empty dictionary to store the current object structure
        obj_struc : Dict[ProteusID, Dict] = {}

        # Add children to the structure
        for child in object.children.values():
            child_struc : Dict[ProteusID, Dict] = self.get_object_structure(child.id)
            obj_struc[child.id] = child_struc

        return obj_struc
    
    # ----------------------------------------------------------------------
    # Method     : get_project_structure
    # Description: Returns the project structure one depth level.
    # Date       : 08/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_project_structure (self) -> List[ProteusID]:
        """
        Returns the project structure one depth level. Each element is
        represented by a dictionary with the following structure: {id: id, ...}
        """
        # TODO: Return the project structure using a more verbose format like
        #       a name property or similar.

        # Initialize an empty dictionary to store the current project structure
        proj_struc : Dict = {}

        # Add documents to the structure
        for document in self.project.documents.values():
            proj_struc[document.id] = document.id

        return proj_struc