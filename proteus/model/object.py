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

# imports

# for using classes as return type hints in methods
# (this will change in Python 3.11)
from __future__ import annotations # it has to be the first import

import pathlib
from distutils.dir_util import copy_tree
# standard library imports
import shortuuid
import os
import logging
from typing import List, NewType, Union
import lxml.etree as ET
import copy

# local imports (starting from root)
from proteus.model import *
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
    def load(project:Project, id:ProteusID) -> Object:
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
        return Object(project, object_file_path)

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a PROTEUS object and builds it using an
    #              XML file.
    # Date       : 16/09/2022
    # Version    : 0.2
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def __init__(self, project:Project, object_file_path: str) -> None:
        """
        It initializes and builds a PROTEUS object from an XML file.
        """
        # Initialize property dictionary in superclass
        # TODO: pass some arguments?
        super().__init__(object_file_path)

        # Check project object
        assert project is not None, \
            f"Invalide project object for {object_file_path}"
        
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

        # Get object classes and accepted children classes
        self.classes          : List[ProteusClassTag] = root.attrib['classes']
        self.acceptedChildren : List[ProteusClassTag] = root.attrib['acceptedChildren']

        # Load object's properties using superclass method
        super().load_properties(root)

        # Children dictionary
        self.children : dict[ProteusID,Object] = dict[ProteusID,Object]()

        # Load object's children
        self.load_children(root)

    # ----------------------------------------------------------------------
    # Method     : load_children
    # Description: It loads the children of a PROTEUS object using an
    #              XML root element <object>.
    # Date       : 16/09/2022
    # Version    : 0.2
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def load_children(self, root : ET.Element) -> None:
        """
        It loads a PROTEUS object's children from an XML root element.
        """

        # Check root is not None
        assert root is not None, \
            f"Root element is not valid for {self.id}."

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

            # Add the child to the children dictionary
            self.children[child_id] = Object.load(self.project, child_id)

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
        for child in self.children.values():
            child_element = ET.SubElement(children_element, CHILD_TAG)
            child_element.set('id', child.id)

        return object_element
    
    # ----------------------------------------------------------------------
    # Method     : clone_object
    # Description: It clones an element.
    # Date       : 27/09/2022
    # Version    : 0.2
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    def clone_object(self, parent: Union[Object,Project]):
        
        # Deepcopy so we don't change the original object.
        # Differences between copy and deepcopy -> https://www.programiz.com/python-programming/shallow-deep-copy
        new_object = copy.deepcopy(self)

        def generate_uuid():
            uuid = shortuuid.random(length=12)
            if uuid in self.project.documents.keys():
                uuid = generate_uuid()
            return uuid

        # REASSIGN ID
        new_object.id = generate_uuid()

        # Clone children
        def rename_ids(object: Object):
            for child in object.children.values():
                child.id = generate_uuid()
                child.state = ProteusState.FRESH

                # Check if object has children
                if(child.children):
                    rename_ids(child)

        # Check if object has children
        if(new_object.children):
            rename_ids(new_object)

        object_assets_path = pathlib.Path(self.path).parent.parent / "assets"


        if (parent.__class__.__name__ == "Project"):
            parent.documents[new_object.id] = new_object
            if(object_assets_path.exists()):
                parent_relative_path = pathlib.Path(parent.path)
                parent_absolute_path = parent_relative_path.resolve()
                parent_assets_path = parent_absolute_path.parent / "assets"    
                copy_tree(str(object_assets_path), str(parent_assets_path))

        elif (type(parent) is Object):
            parent.children[new_object.id] = new_object
            if(object_assets_path.exists()):
                parent_relative_path = pathlib.Path(parent.project.path)
                parent_absolute_path = parent_relative_path.resolve()
                parent_assets_path = parent_absolute_path.parent / "assets"    
                copy_tree(str(object_assets_path), str(parent_assets_path))
        


        parent.state = ProteusState.DIRTY
        new_object.state = ProteusState.FRESH

