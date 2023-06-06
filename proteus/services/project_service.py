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

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID, CHILDREN_TAG, CHILD_TAG
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.abstract_object import ProteusState
from proteus.model.properties import Property


# --------------------------------------------------------------------------
# Class: ProjectService
# Description: Class for project operations interface
# Date: 06/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ProjectService:
    """
    Acts as an interface for project, documents and objects operations.
    Loads a project into memory and provides methods to perform operations.
    """

    project: Project = None
    project_index: Dict[ProteusID, Object] = {}

    @classmethod
    def load_project(cls, project_path: str):
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
    def _get_element_by_id(cls, element_id: ProteusID) -> Union[Project, Object]:
        """
        Returns the project or object with the given id.

        :param element_id: Id of the project or object.
        :return: Project or object with the given id.
        """
        # Populate index to check for new objects
        if element_id not in cls.project_index:
            cls._populate_index()

        # Check if the element is in the index
        assert (
            element_id in cls.project_index
        ), f"Element with id {element_id} not found."

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
    def _populate_index(cls) -> None:
        """
        Populates the project index with the all the objects in the project.
        If an object was already in the index, it will be ignored.
        """

        def _populate_index_private(object: Object) -> None:
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
    def get_properties(cls, element_id: ProteusID) -> Dict[str, Property]:
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
    def update_properties(
        cls, element_id: ProteusID, properties: List[Property]
    ) -> None:
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
    def save_project(cls) -> None:
        """
        Saves the project to disk.
        """
        cls.project.save_project()

    # ----------------------------------------------------------------------
    # Method     : change_state_recursive
    # Description: Changes the state of the object with the given id and
    #              all its children recursively.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def change_state(cls, object_id: ProteusID, new_state: ProteusState) -> None:
        """
        Changes the state of the object with the given id and all its children
        recursively.

        :param object_id: Id of the object to change state.
        :param new_state: New state of the object.
        """

        # Private helper function
        def _change_state(object: Object, new_state: ProteusState) -> None:
            # Change state of object
            object.state = new_state

            # Change state of children
            for child in object.get_descendants():
                _change_state(child, new_state)

        # Get object using helper method
        object = cls._get_element_by_id(object_id)

        _change_state(object, new_state)

    # ----------------------------------------------------------------------
    # Method     : get_object_structure
    # Description: Returns the object structure as a tree.
    # Date       : 08/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_object_structure(cls, object_id: ProteusID) -> Dict[Object, List]:
        """
        Returns the element structure as a tree. Each element is represented
        by a dictionary with the following structure: {id: [{id: [{...}, {...}, ...]}, {...}, ...]}.
        Each object is represented by a list of dictionaries, where each dictionary
        represents a child object. The list is empty if the object has no children.

        :param element_id: Id of the element.
        :return: Dictionary with the element structure.
        """
        # Get object using helper method
        object: Object = cls._get_element_by_id(object_id)

        # Initialize an empty dictionary to store the object structure
        obj_struc: Dict[Object, List] = {}

        # Create object structure
        obj_struc_list: List = cls._get_object_structure(object)
        obj_struc[object] = obj_struc_list

        return obj_struc

    @classmethod
    def _get_object_structure(cls, object: Object) -> Dict[Object, List]:
        """
        Private method for get_object_structure.
        """
        # Check that the element is an object
        assert isinstance(object, Object), f"Element with id {object} is not an object."

        # Initialize an empty list to store the objects
        children_struc: List = list()

        # Add children to the structure
        for child in object.get_descendants():
            # Initialize an empty dictionary to store the current object structure
            obj_struc: Dict[Object, List] = {}

            # Create child structure
            child_struc: Dict[Object, List] = cls._get_object_structure(child)
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
    def get_project_structure(cls) -> List[Object]:
        """
        Returns the project structure one depth level. Each element is
        represented by a dictionary with the following structure: {id: id, ...}

        :return: Dictionary with the project documents.
        """
        return cls.project.get_descendants()

    # ----------------------------------------------------------------------
    # Method     : clone_object
    # Description: Clones the object with the given id.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def clone_object(cls, object_id: ProteusID) -> None:
        """
        Clones the object with the given id and inserts it as a sibling next
        to the original object.

        :param object_id: Id of the object to clone.
        """
        # Get object using helper method
        object: Object = cls._get_element_by_id(object_id)

        # Check that the object is an object
        assert isinstance(object, Object), f"Element with id {object} is not an object."

        # Calculate position of the cloned object
        siblings: List[Object] = object.parent.get_descendants()
        cloned_position: int = siblings.index(object) + 1

        # Clone object
        return object.clone_object(
            parent=object.parent, project=cls.project, position=cloned_position
        )

    # ----------------------------------------------------------------------
    # Method     : generate_document_xml
    # Description: Generates the xml file for the given document.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def generate_document_xml(cls, document_id: ProteusID) -> ET.Element:
        """
        Generates the xml file for the given document. Iterates until no
        child tags are found. Replaces child tags with the xml of the child
        object.

        :param document_id: Id of the document.
        """
        # Get document using helper method
        document = cls._get_element_by_id(document_id)

        # Generate xml file
        root: ET.element = document.generate_xml()

        # Iterate until no chil tags are found
        while root.findall(f".//{CHILD_TAG}"):
            # Load children
            children: ET.Element = root.findall(f".//{CHILD_TAG}")

            # Parse object's children
            child_element: ET.Element
            for child_element in children:
                child_id: ProteusID = child_element.attrib["id"]

                # Get child object
                child: Object = cls._get_element_by_id(child_id)

                # Remove dead objects
                if child.state == ProteusState.DEAD:
                    parent_element: ET.Element = child_element.getparent()
                    parent_element.remove(child_element)
                else:
                    # Generate xml file
                    child_xml: ET.Element = child.generate_xml()

                    # Replace child element with xml
                    parent_element: ET.Element = child_element.getparent()
                    parent_element.replace(child_element, child_xml)

        return root
