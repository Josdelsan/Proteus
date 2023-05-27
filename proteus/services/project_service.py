# ==========================================================================
# File: project_service.py
# Description: Project interface
# Date: 06/05/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# ==========================================================================
# Update: 27/05/2023 (José María Delgado Sánchez)
# Description:
# - Atributes are now class atributes instead of instance atributes.
#   Methods are now class methods instead of instance methods.
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

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
class ProjectService():
    """
    Acts as an interface for project, documents and objects operations.
    Loads a project into memory and provides methods to perform operations.
    """

    project       : Project                 = None
    project_index : Dict[ProteusID, Object] = {}

    @classmethod
    def load_project (cls, project_path: str):
        """
        Initializes the project service with the given project path. Force
        the load of every object in the project to store it in a dictionary
        for easy access.

        :param project_path: Path to the project directory.
        """
        # Load project
        cls.project = Project.load(project_path)

        # Initialize project index
        cls.project_index = {}

        # Populate project index
        cls._populate_index()


    # ----------------------------------------------------------------------
    # Method     : _get_element
    # Description: Helper method that returns the project or object with
    #              the given id.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def _get_element_by_id (cls, element_id: ProteusID) -> Union[Project, Object]:
        """
        Returns the project or object with the given id.

        :param element_id: Id of the project or object.
        :return: Project or object with the given id.
        """
        # Populate index to check for new objects
        if element_id not in cls.project_index:
            cls._populate_index()

        # Check if the element is in the index
        assert element_id in cls.project_index, \
            f"Element with id {element_id} not found."

        # Return the element
        return cls.project_index[element_id]
    
    # ----------------------------------------------------------------------
    # Method     : _populate_index
    # Description: Helper method that populates the project index with
    #              the all the objects in the project. If an object was
    #              already in the index, it will be ignored.
    # Date       : 07/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def _populate_index (cls) -> None:
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
            if object.id not in cls.project_index:
                cls.project_index[object.id] = object

            # Add children to the index
            for child in object.get_descendants():
                _populate_index_private(child)

        # Load project index, this forces load for
        # every object in the project
        for document in cls.project.get_descendants():
            _populate_index_private(document)

        # Include project in the index if it is not there
        if cls.project.id not in cls.project_index:
            cls.project_index[cls.project.id] = cls.project

    # ----------------------------------------------------------------------
    # Method     : get_properties
    # Description: Returns the project or object properties properties.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_properties (cls, element_id : ProteusID) -> Dict[str, Property]:
        """
        Returns the project or object properties.

        :param element_id: Id of the project or object.
        :return: Dictionary of properties.
        """
        element = cls._get_element_by_id(element_id)

        return element.properties
        
    # ----------------------------------------------------------------------
    # Method     : update_properties
    # Description: Updates the project or object properties.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def update_properties (cls, element_id : ProteusID, properties: List[Property]) -> None:
        """
        Updates the project or object properties.

        :param element_id: Id of the project or object.
        :param properties: List of properties to update.
        """
        element = cls._get_element_by_id(element_id)

        for property in properties:
            element.set_property(property)

    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: Saves the project to disk.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def save_project (cls) -> None:
        """
        Saves the project to disk.
        """
        cls.project.save()

    # ----------------------------------------------------------------------
    # Method     : delete_object
    # Description: Deletes the object with the given id from the project.
    #              Changes are not saved to disk until save_project is
    #              called.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def delete_object (cls, object_id: ProteusID) -> None:
        """
        Deletes the object with the given id from the project. Changes are
        not saved to disk until save_project is called.

        :param object_id: Id of the object to delete.
        """
        # Get object using helper method
        object = cls._get_element_by_id(object_id)

        object.delete()

    # ----------------------------------------------------------------------
    # Method     : get_object_structure
    # Description: Returns the object structure as a tree.
    # Date       : 08/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_object_structure (cls, object_id: ProteusID) -> Dict[Object, List]:
        """
        Returns the element structure as a tree. Each element is represented
        by a dictionary with the following structure: {id: [{id: [{...}, {...}, ...]}, {...}, ...]}.
        Each object is represented by a list of dictionaries, where each dictionary
        represents a child object. The list is empty if the object has no children.

        :param element_id: Id of the element.
        :return: Dictionary with the element structure.
        """
        # Get object using helper method
        object : Object = cls._get_element_by_id(object_id)
        
        # Initialize an empty dictionary to store the object structure
        obj_struc : Dict[Object, List] = {}

        # Create object structure
        obj_struc_list : List = cls._get_object_structure(object)
        obj_struc[object] = obj_struc_list

        return obj_struc
        
    @classmethod
    def _get_object_structure (cls, object: Object) -> Dict[Object, List]:
        """
        Private method for get_object_structure.
        """
        # Check that the element is an object
        assert isinstance(object, Object), \
            f"Element with id {object} is not an object."
        
        # Initialize an empty list to store the objects
        children_struc : List = list()

        # Add children to the structure
        for child in object.get_descendants():

            # Initialize an empty dictionary to store the current object structure
            obj_struc : Dict[Object, List] = {}

            # Create child structure
            child_struc : Dict[Object, List] = cls._get_object_structure(child)
            obj_struc[child] = child_struc

            # Add child to the list
            children_struc.append(obj_struc)

        return children_struc
    
    # ----------------------------------------------------------------------
    # Method     : get_project_structure
    # Description: Returns the project structure one depth level.
    # Date       : 08/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_project_structure (cls) -> List[Object]:
        """
        Returns the project structure one depth level. Each element is
        represented by a dictionary with the following structure: {id: id, ...}

        :return: Dictionary with the project documents.
        """
        return cls.project.get_descendants()