# ==========================================================================
# File: project_service.py
# Description: Project interface
# Date: 06/05/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import Union, List, Dict
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.config import Config
from proteus.model import (
    ProteusID,
    ID_ATTRIBUTE,
    CHILD_TAG,
    DOCUMENT_TAG,
    ProteusClassTag,
    PROTEUS_ANY,
)
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.abstract_object import ProteusState
from proteus.model.properties import Property
from proteus.model.trace import Trace

# logging configuration
log = logging.getLogger(__name__)


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

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor.
    # Date       : 07/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self):
        """
        Class constructor.
        """
        # Instance variables
        self.project: Project = None
        self.project_index: Dict[ProteusID, Union[Object, Project]] = {}

        log.info("ProjectService initialized.")

    # ----------------------------------------------------------------------
    # Method     : load_project
    # Description: Initializes the project service with the given project
    #              path.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def load_project(self, project_path: str):
        """
        Initializes the project service with the given project path. Force
        the load of every object in the project to store it in a dictionary
        for easy access.

        :param project_path: Path to the project directory.
        """
        # Load project
        self.project = Project.load(project_path)

        # Set current project path in application config
        Config().current_project_path = project_path

        # Initialize project index
        self.project_index = {}

        # Populate project index
        self._populate_index()

        log.info(f"Project '{self.project.get_property('name').value}' loaded.")

    # ----------------------------------------------------------------------
    # Method     : _get_element
    # Description: Helper method that returns the project or object with
    #              the given id.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _get_element_by_id(self, element_id: ProteusID) -> Union[Project, Object]:
        """
        Returns the project or object with the given id.

        Raises an exception if the element is not found.

        :param element_id: Id of the project or object.
        :return: Project or object with the given id.
        """
        # Populate index to check for new objects
        if element_id not in self.project_index:
            self._populate_index()

        # Check if the element is in the index
        assert (
            element_id in self.project_index
        ), f"Element with id {element_id} not found."

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
    def _populate_index(self) -> None:
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
            if object.id not in self.project_index:
                self.project_index[object.id] = object

            # Add children to the index
            for child in object.get_descendants():
                _populate_index_private(child)

        # Load project index, this forces load for
        # every object in the project
        for document in self.project.get_descendants():
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
    def get_properties(self, element_id: ProteusID) -> Dict[str, Property]:
        """
        Returns the project or object properties.

        :param element_id: Id of the project or object.
        :return: Dictionary of properties.
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
    def update_properties(
        self, element_id: ProteusID, properties: List[Property]
    ) -> None:
        """
        Updates the project or object properties.

        :param element_id: Id of the project or object.
        :param properties: List of properties to update.
        """
        # Check properties is a list
        assert isinstance(properties, list), "Properties must be a list."

        # Check properties are Property objects
        assert all(
            isinstance(property, Property) for property in properties
        ), "Properties must be Property objects."

        # Get element by id
        element = self._get_element_by_id(element_id)

        # Check element is an object or project
        assert isinstance(
            element, (Object, Project)
        ), f"Element with id {element_id} is not an object or project."

        for property in properties:
            element.set_property(property)

    # ----------------------------------------------------------------------
    # Method     : update_traces
    # Description: Updates the object traces.
    # Date       : 26/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_traces(self, element_id: ProteusID, traces: List[Trace]) -> None:
        """
        Updates the object traces.

        :param element_id: Id of the object.
        :param traces: List of traces to update.
        """
        # Check traces is a list
        assert isinstance(traces, list), "Traces must be a list."

        # Check traces are Trace objects
        assert all(
            isinstance(trace, Trace) for trace in traces
        ), "Traces must be Trace objects."

        # Get element by id
        element = self._get_element_by_id(element_id)

        # Check element is an object or project
        assert isinstance(
            element, (Object)
        ), f"Element with id {element_id} is not an object. Traces can only be added to objects"

        for trace in traces:
            element.traces[trace.name] = trace

        # Update state to Dirty if traces are updated and the element is not FRESH
        if traces and element.state == ProteusState.CLEAN:
            element.state = ProteusState.DIRTY

    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: Saves the project to disk.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_project(self) -> None:
        """
        Saves the project to disk.
        """
        self.project.save_project()

    # ----------------------------------------------------------------------
    # Method     : change_state_recursive
    # Description: Changes the state of the object with the given id and
    #              all its children recursively.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def change_state(self, object_id: ProteusID, new_state: ProteusState) -> None:
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
        object = self._get_element_by_id(object_id)

        _change_state(object, new_state)

    # ----------------------------------------------------------------------
    # Method     : get_object_structure
    # Description: Returns the object structure as a tree.
    # Date       : 08/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_structure(self, object_id: ProteusID) -> Dict[Object, List]:
        """
        Returns the element structure as a tree. Each element is represented
        by a dictionary with the following structure: {id: [{id: [{...}, {...}, ...]}, {...}, ...]}.
        Each object is represented by a list of dictionaries, where each dictionary
        represents a child object. The list is empty if the object has no children.

        :param element_id: Id of the element.
        :return: Dictionary with the element structure.
        """
        # Get object using helper method
        object: Object = self._get_element_by_id(object_id)

        # Initialize an empty dictionary to store the object structure
        obj_struc: Dict[Object, List] = {}

        # Create object structure
        obj_struc_list: List = self._get_object_structure(object)
        obj_struc[object] = obj_struc_list

        return obj_struc

    def _get_object_structure(self, object: Object) -> Dict[Object, List]:
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
            child_struc: Dict[Object, List] = self._get_object_structure(child)
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
    def get_project_structure(self) -> List[Object]:
        """
        Returns the project structure one depth level. Each element is
        represented by a dictionary with the following structure: {id: id, ...}

        :return: List with the project documents.
        """
        return self.project.get_descendants()

    # ----------------------------------------------------------------------
    # Method     : get_objects
    # Description: Returns objects in the project.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_objects(self, classes: List[ProteusClassTag] = []) -> List[Object]:
        """
        Get the objects of the current project. They can be filtered by classes.
        """

        # Variable initialization
        objects: List[Object] = []

        # if classes is empty, is None or contains :Proteus-any, return all objects
        if not classes or PROTEUS_ANY in classes:
            # Iterate over project index and drop project and dead objects
            for element in self.project_index.values():
                if isinstance(element, Object) and element.state != ProteusState.DEAD:
                    objects.append(element)

        # else, filter objects by classes droping project and dead objects
        else:
            object: Object
            # Iterate over all objects in the project
            for object in self.project_index.values():
                if object.state == ProteusState.DEAD or not isinstance(object, Object):
                    continue

                # Get object classes
                object_classes: List[ProteusClassTag] = object.classes

                # Check for common classes between object classes and desired classes
                common_classes = [c for c in classes if c in object_classes]
                if common_classes:
                    objects.append(object)

        return objects

    # ----------------------------------------------------------------------
    # Method     : clone_object
    # Description: Clones the object with the given id.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def clone_object(self, object_id: ProteusID) -> None:
        """
        Clones the object with the given id and inserts it as a sibling next
        to the original object.

        :param object_id: Id of the object to clone.
        """
        # Check the object_id is not None
        assert object_id is not None, "Object id cannot be None."

        # Get object using helper method
        object: Object = self._get_element_by_id(object_id)

        # Check that the object is an object
        assert isinstance(object, Object), f"Element with id {object} is not an object."

        # Calculate position of the cloned object
        siblings: List[Object] = object.parent.get_descendants()
        cloned_position: int = siblings.index(object) + 1

        # Clone object
        return object.clone_object(
            parent=object.parent, project=self.project, position=cloned_position
        )

    # ----------------------------------------------------------------------
    # Method     : change_object_position
    # Description: Changes the position of the object with the given id.
    # Date       : 13/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def change_object_position(
        self,
        object_id: ProteusID,
        new_position: int,
        new_parent: Union[Project, Object],
    ) -> None:
        """
        Changes the position of the object with the given id. If position is
        None, the object is moved to the end of the parent. Given position
        must be relative to non DEAD objects.

        :param object_id: Id of the object to change position.
        :param new_position: New position of the object.
        :param new_parent: New parent of the object.
        """
        # TODO: This method should be refactored to not recieve the new position
        #       relative to non DEAD objects, but relative to all objects. Since
        #       this is a problem when redoing delete operations.

        # Check the object_id is valid
        assert isinstance(object_id, str), f"Invalid object id {object_id}."

        # Check the new_parent is valid
        assert isinstance(
            new_parent, (Project, Object)
        ), f"Invalid new parent {new_parent}."

        # Get object using helper method
        object: Object = self._get_element_by_id(object_id)

        # Check that the object is an object
        assert isinstance(object, Object), f"Element with id {object} is not an object."

        # Set old parent to change its state later
        old_parent: Union[Project, Object] = object.parent

        # Store the current position of the object in its parent to later drop it
        current_position: int = old_parent.get_descendants().index(object)

        # Descendants lists, one with the dead objects and one without them
        # to calculate position relative to non DEAD objects
        new_parent_descendants: List[Object] = new_parent.get_descendants()
        alive_descendants: List[Object] = [
            d for d in new_parent_descendants if d.state != ProteusState.DEAD
        ]

        # If no position is given or the position is greater than the number of
        # alive descendants, move the object to the end of the parent
        if new_position is None or new_position >= len(alive_descendants):
            new_position = None
        # If position is given, calculate the real position using a reference sibling
        else:
            # Check the new position is valid (different from current position and the following one)
            assert (
                new_position != current_position
            ), f"Object {object_id} is already in position {new_position}."

            # Use a sibling as reference to calculate the real position relative to
            # non DEAD objects and once the object in current position is removed
            reference_sibling: Object = alive_descendants[new_position]

            # If the new parent is the same as the old parent, take into account
            # the object in current position is going to be removed
            if old_parent == new_parent:
                # Simulate the removal of the object in current position
                descendants_copy: List[Object] = new_parent_descendants.copy()
                descendants_copy.pop(current_position)
                new_position = descendants_copy.index(reference_sibling)
            else:
                new_position = new_parent_descendants.index(reference_sibling)

        # Change the old parent state to DIRTY if not FRESH
        if old_parent.state != ProteusState.FRESH:
            old_parent.state = ProteusState.DIRTY

        # Remove object from current parent descendants
        old_parent.get_descendants().pop(current_position)

        # Add object to new parent descendants
        new_parent.add_descendant(object, new_position)

    # ----------------------------------------------------------------------
    # Method     : generate_document_xml
    # Description: Generates the xml file for the given document.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def generate_document_xml(self, document_id: ProteusID) -> ET.Element:
        """
        Generates the xml file for the given document. Iterates until no
        child tags are found. Replaces child tags with the xml of the child
        object.

        :param document_id: Id of the document.
        """
        # Get document using helper method
        document = self._get_element_by_id(document_id)

        # Generate project xml file
        root: ET.element = self.project.generate_xml()
        # Iterate over document tag and replace the asked document
        for document_element in root.findall(f".//{DOCUMENT_TAG}"):
            if document_element.attrib[ID_ATTRIBUTE] == document_id:
                parent_element: ET.Element = document_element.getparent()
                document_xml: ET.Element = document.generate_xml()
                parent_element.replace(document_element, document_xml)
            # Delete the rest of documents
            else:
                document_element.getparent().remove(document_element)

        # Iterate until no chil tags are found
        while root.findall(f".//{CHILD_TAG}"):
            # Load children
            children: ET.Element = root.findall(f".//{CHILD_TAG}")

            # Parse object's children
            child_element: ET.Element
            for child_element in children:
                child_id: ProteusID = child_element.attrib[ID_ATTRIBUTE]

                # Get child object
                child: Object = self._get_element_by_id(child_id)

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

    # ----------------------------------------------------------------------
    # Method     : add_project_template
    # Description: Add a new project template to the project.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_project_template(self, template_name: str) -> None:
        """
        Add a new project template to the project.

        :param template_name: The name of the template to add.
        """
        # Check if the template exists in the app installation
        xslt_routes: Dict[str, Path] = Config().xslt_routes
        assert (
            template_name in xslt_routes
        ), f"XSLT file {template_name} not found in config file"

        self.project.xsl_templates.append(template_name)
        self.project.state = ProteusState.DIRTY

    # ----------------------------------------------------------------------
    # Method     : delete_project_template
    # Description: Delete a project template from the project.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_project_template(self, template_name: str) -> None:
        """
        Remove a project template from the project.

        :param template_name: The name of the template to remove.
        """
        self.project.xsl_templates.remove(template_name)
        self.project.state = ProteusState.DIRTY
