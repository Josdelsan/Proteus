# ==========================================================================
# File: object.py
# Description: a PROTEUS object
# Date: 16/09/2022
# Version: 0.2
# Author: Amador Durán Toro
# ==========================================================================
# Update: 16/09/2022 (Amador)
# Description:
# - Object now inherits from AbstractObject
# ==========================================================================
# Update: 15/04/2023 (José María)
# Description:
# - Object now lazy loads its children.
# ==========================================================================

# for using classes as return type hints in methods
# (this will change in Python 3.11)
from __future__ import annotations # it has to be the first import

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import pathlib
import os
import logging
from typing import List, NewType, Union
import copy

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET
import shortuuid

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID, CHILDREN_TAG, OBJECT_TAG, OBJECTS_REPOSITORY, CHILD_TAG, PROTEUS_ANY
from proteus.model.abstract_object import AbstractObject, ProteusState
# from proteus.model.project import Project
# Project class dummy declaration to break circular import
class Project(AbstractObject):
    pass

# Type for Class tags in Proteus
ProteusClassTag = NewType('ProteusClassTag', str)

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: Object
# Description: Class for PROTEUS objects
# Date: 16/09/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class Object(AbstractObject):
    """
    A PROTEUS object is an XML file inside of a PROTEUS project 'objects'
    directory.

    A PROTEUS object can only be created by cloning another existing object,
    usually an archetype object.

    An already created object can be loaded by providing the path to its XML
    file.
    """
    # ----------------------------------------------------------------------
    # Method: load (static)
    # Description: It loads a PROTEUS object from disk into memory
    # Date: 16/09/2022
    # Version: 0.2
    # Author: Amador Durán Toro
    # ----------------------------------------------------------------------
    # NOTE: Current working directory is set by Project.load().
    #       Do not change current directory in this method.
    # ----------------------------------------------------------------------

    @staticmethod
    def load(id:ProteusID, project:Project) -> Object:
        """
        Static factory method for loading a PROTEUS object given a project
        and a short UUID.
        """
        # TODO new param (parent:Project/Object) to set parent object
        # needed for some actions (move, delete, etc.)

        # Check project is not None
        assert project is not None, \
            f"Invalid project object when loading object from {id}.xml"

        # Extract project directory from project path
        project_directory : str = os.path.dirname(project.path)
        log.info(f"Loading a PROTEUS object from {project_directory}/{OBJECTS_REPOSITORY}/{id}.xml")

        # Create path to objects repository
        objects_repository : str = f"{project_directory}/{OBJECTS_REPOSITORY}"

        # Check objects repository is a directory
        assert os.path.isdir(objects_repository), \
            f"PROTEUS projects must have an objects repository. {objects_repository} is not a directory."

        # Complete path to object file
        object_file_path = f"{objects_repository}/{id}.xml"
        

        # # Check if object file exists
        assert os.path.isfile(object_file_path), \
            f"PROTEUS object file {object_file_path} not found in {objects_repository}."

        # Create and return the project object
        return Object(object_file_path, project=project)

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a PROTEUS object and builds it using an
    #              XML file.
    # Date       : 16/09/2022
    # Version    : 0.2
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def __init__(self, object_file_path: str, project:Project = None) -> None:
        """
        It initializes and builds a PROTEUS object from an XML file.
        """
        # Initialize property dictionary in superclass
        # TODO: pass some arguments?
        super().__init__(object_file_path)
        
        if(not os.path.isfile(object_file_path)):
            self.state = ProteusState.FRESH

        # Save project as an object's attribute
        self.project : Project = project

        # Parse and load XML into memory
        root : ET.Element = ET.parse( object_file_path ).getroot()

        # Check root tag is <object>
        assert root.tag == OBJECT_TAG, \
            f"PROTEUS object file {object_file_path} must have <{OBJECT_TAG}> as root element, not {root.tag}."

        # Get object ID from XML
        self.id : ProteusID = ProteusID(root.attrib['id'])

        # Object or Project
        self.parent : Union[Object,Project] = None

        # Get object classes and accepted children classes
        self.classes          : List[ProteusClassTag] = root.attrib['classes']
        self.acceptedChildren : List[ProteusClassTag] = root.attrib['acceptedChildren']

        # Load object's properties using superclass method
        super().load_properties(root)

        # Children dictionary (will be loaded on demand)
        self._children : List[Object] = None


    # ----------------------------------------------------------------------
    # Property   : children
    # Description: Property children getter. Loads children from XML file
    #              on demand.
    # Date       : 12/04/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @property
    def children(self) -> List[Object]:
        """
        Property children getter. Loads children from XML file on demand.
        :return: Dictionary of children objects
        """
        # Check if children dictionary is not initialized
        if self._children is None:
            # Initialize children dictionary
            self._children : List[Object] = []

            # Load children from XML file
            self.load_children()

        # Return children dictionary
        return self._children

    # ----------------------------------------------------------------------
    # Method     : load_children
    # Description: It loads the children of a PROTEUS object using an
    #              XML root element <object>.
    # Date       : 13/04/2023
    # Version    : 0.2
    # Author     : Amador Durán Toro
    #              José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def load_children(self) -> None:
        """
        It loads a PROTEUS object's children from an XML root element.
        """

        # Parse and load XML into memory
        root : ET.Element = ET.parse( self.path ).getroot()

        # Check root is not None
        assert root is not None, \
            f"Root element is not valid in {self.path}."

        # Load children
        children : ET.Element = root.find(CHILDREN_TAG)

        # Check whether it has children
        assert children is not None, \
            f"PROTEUS object file {self.id} does not have a <{CHILDREN_TAG}> element."

        # Parse object's children
        child : ET.Element
        for child in children:
            child_id : ProteusID = child.attrib['id']

            # Check whether the child has an ID
            assert child_id is not None, \
                f"PROTEUS object file {self.id} includes a child without ID."

            # Add the child to the children dictionary and set the parent
            if self.project is not None:
                # If the project is not None, load the child using the project
                object = Object.load(child_id, self.project)
            else:
                # If the project is None, this object is an archetype,
                # so load the child using the object's path
                objects_dir_path : str = os.path.dirname(self.path)
                object_path : str = f"{objects_dir_path}/{child_id}.xml"
                object = Object(object_path)
            
            object.parent = self

            self.children.append(object)

    # ----------------------------------------------------------------------
    # Method     : get_descendants
    # Description: It returns a list with all the children of an object.
    # Date       : 23/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_descendants(self) -> List:
        """
        It returns a list with all the children of an object.
        :return: list with all the children of an object.
        """
        # Return the list with all the descendants of an object
        return self.children


    # ----------------------------------------------------------------------
    # Method     : add_descendant
    # Description: It adds a child to a PROTEUS object.
    # Date       : 26/04/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def add_descendant(self, child: Object, position: int = None) -> None:
        """
        It adds a child to a PROTEUS object if class is accepted.

        :param child: Child Object to be added.
        :param position: Position in the children list where the child will be added.
        """
        # If position is not specified, add the object at the end
        if position is None:
            position = len(self.children)

        # Check if the child is a valid object
        assert isinstance(child, Object), \
            f"Child {child} is not a valid PROTEUS object."

        # Check if the child is accepted
        assert child.classes[-1] in self.acceptedChildren  \
            or PROTEUS_ANY in self.acceptedChildren,       \
            f"Child is not accepted by {self.id}.          \
            Accepted children are {self.acceptedChildren}. \
            Child is class {child.classes}."

        # Check if the child is already a child of this object
        assert child.id not in [o.id for o in self.children], \
            f"Object {child.id} is already a child of {self.id}."

        # Add the child to the children dictionary and set the parent
        self.children.insert(position, child)
        child.parent = self


    # ----------------------------------------------------------------------
    # Method     : generate_xml
    # Description: It generates an XML element for the object.
    # Date       : 16/09/2022
    # Version    : 0.2
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def generate_xml(self) -> ET.Element:
        """
        It generates an XML element for the object.
        """
        # Create <object> element and set ID
        object_element = ET.Element(OBJECT_TAG)
        object_element.set('id', self.id)
        object_element.set("classes", self.classes)
        object_element.set("acceptedChildren", self.acceptedChildren)

        # Create <properties> element
        super().generate_xml_properties(object_element)

        # Create <children> element
        children_element = ET.SubElement(object_element, CHILDREN_TAG)

        # Create <child> subelements
        for child in self.children:
            child_element = ET.SubElement(children_element, CHILD_TAG)
            child_element.set('id', child.id)

        return object_element
    
    # ----------------------------------------------------------------------
    # Method     : clone_object
    # Description: It clones an element.
    # Date       : 24/04/2023
    # Version    : 0.3
    # Author     : José María Delgado Sánchez
    #              Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    def clone_object(self, parent: Union[Object,Project], project: Project, position: int = None) -> None:
        """
        Function that clones an object in a new parent. This function doesn't
        save the object in the system but add it to the parent children so
        it will be saved when we save the project.

        :param parent: Parent of the new object.
        :param project: Project where the object will be saved.
        :param position: Position in the children list where the child will be added.
        :type parent: Union[Object,Project].
        """

        # Helper function to assign a new id to the object
        def generate_new_id(project: Project):
            """
            Helper function that generates a new id for the object.
            """
            # Generate a new id for the object
            new_id = ProteusID(shortuuid.random(length=12))

            # Check if the new id is already in use
            if new_id in project.get_ids():
                generate_new_id(project)
            
            return new_id


        # Check if project is not None
        # NOTE: Project instance type cannot be checked with isinstance
        # due to Project dummy class at the beginning of the file.
        assert project.__class__.__name__ ==  "Project", \
            f"Parent project must be instance of Project."
        
        # Check if parent is not None
        assert parent.__class__.__name__ == "Project"       \
            or isinstance(parent, Object),                  \
            f"Parent must be instance of Object or Project"


        # Deepcopy so we don't change the original object.
        # Differences between copy and deepcopy -> https://www.programiz.com/python-programming/shallow-deep-copy
        new_object = copy.deepcopy(self)

        # Force children load
        new_object.children

        # Set new project and FRESH state
        new_object.project = project
        new_object.state = ProteusState.FRESH

        # Assign a new id that is not in use
        new_object.id = generate_new_id(project)

        # Create file path
        project_objects_path = pathlib.Path(project.path).parent / OBJECTS_REPOSITORY
        new_object.path = project_objects_path / f"{new_object.id}.xml"

        # Add the new object to the parent children and set the parent
        parent.add_descendant(new_object, position)

        # If the object has children we clone them
        if len(new_object.children) > 0:

            # Get the children list
            children = list(new_object.children)

            # Clone the children
            for child in children:
                # Clone the child
                child.clone_object(new_object, project, len(new_object.children))

                # Remove the old child from the children list
                new_object.children.remove(child)


        # Check the new object is valid
        assert isinstance(new_object, Object), \
            f"Failed to clone {self.id} with parent {parent.id} in project {project.id}."
        
        # Return the new object
        return new_object
            

    # ----------------------------------------------------------------------
    # Method     : save
    # Description: It persist an Object in the system. If the object was
    #              already persisted, it will be updated. If the object was
    #              marked as dead, it will be deleted.
    # Date       : 01/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def save(self) -> None:
        """
        It saves an Object in the system.
        """
        # Save every child
        children = list(self.children)
        for child in children:
            child.save()

        # Persist the object if it is DIRTY or FRESH
        if(self.state == ProteusState.DIRTY or self.state == ProteusState.FRESH):
            root = self.generate_xml()

            # Get the elementTree, save it in the project path and set state to clean
            tree = ET.ElementTree(root)
            tree.write(self.path, pretty_print=True, xml_declaration=True, encoding="utf-8")
            self.state = ProteusState.CLEAN
        
        # Delete the object if it is DEAD
        elif(self.state == ProteusState.DEAD):
            # Delete itself from the parent children
            self.parent.get_descendants().remove(self)

            # Check if the file exists
            # NOTE: file might not exist if the object was created but not saved
            if os.path.exists(self.path):
                # Delete the file
                os.remove(self.path)


    # ----------------------------------------------------------------------
    # Method     : delete
    # Description: It marks an Object as dead. It will be deleted when the
    #              project is saved.
    # Date       : 01/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def delete(self) -> None:
        """
        It marks an Object as dead. It will be deleted when the project is saved.
        """
        self.state = ProteusState.DEAD

        # Delete every child
        for child in self.children:
            child.delete()