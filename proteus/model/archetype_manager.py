# ==========================================================================
# File: archetype_manager.py
# Description: PROTEUS archetype manager
# Date: 13/04/2023
# Version: 0.3
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
#         José María Delgado Sánchez
# ==========================================================================
# Update: 01/10/2022 (Amador)
# Description:
# - Code review.
# ==========================================================================
# Update: 13/04/2023 (José María)
# Description:
# - ArcheTypeManager refactor to adapt to the new repository structure.
#   Now uses Project and Object clases and its lazy load instead of
#   proxy classes.
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from enum import Enum, auto
from os import listdir
import os
from os.path import join, dirname, abspath, isfile, isdir, exists
from os import pardir
import shutil

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET
from strenum import StrEnum
import proteus.config as config

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model import PROPERTIES_TAG
from proteus.model.archetype_proxys import DocumentArchetypeProxy, ObjectArchetypeProxy, ProjectArchetypeProxy
from proteus.model.properties import Property, PropertyFactory


# logging configuration
log = logging.getLogger(__name__)

# TODO: estos directorios habrá que establecerlos por configuración o como
# parámetros pasados al comienzo de la aplicación.


ARCHETYPES_FOLDER = config.Config().archetypes_directory
PROJECT_PROPERTIES_TO_SAVE = ["name", "description", "author", "date"]
DOCUMENT_PROPERTIES_TO_SAVE = ["name", "description", "author", "date"]

DOCUMENT_FILE = "document.xml"
OBJECTS_FILE = "objects.xml"
PROJECT_FILE = "project.xml"


# --------------------------------------------------------------------------
# Class: ArchetypesType
# Description: String-based enumeration for archetypes' types
# Date: 01/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------
# https://stackoverflow.com/questions/58608361/string-based-enum-in-python
# --------------------------------------------------------------------------

class ArchetypesType(StrEnum):
    """
    Enumeration for archetypes' types.
    """
    PROJECTS  = 'projects'
    DOCUMENTS = 'documents'
    OBJECTS   = 'objects'

# --------------------------------------------------------------------------
# Class: ArchetypeManager
# Description: Class for managing PROTEUS archetypes
# Date: 13/04/2023
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         José María Delgado Sánchez
# ----------------------------------------------------------------------

class ArchetypeManager:
    """
    An utility class for managing PROTEUS archetypes. It must provide a way
    to get the project, document, and object archetypes on demand.
    TODO: in the future, it will also be responsible for adding new archetypes.
    """

    # ----------------------------------------------------------------------
    # Method: load_object_archetypes (static)
    # Description: It load object archetypes
    # Date: 13/04/2023
    # Version: 0.2
    # Author: Pablo Rivera Jiménez
    #         José María Delgado Sánchez
    # ----------------------------------------------------------------------

    @classmethod
    def load_object_archetypes( cls ) -> dict[str, list[Object]]:
        """
        Method that loads the object archetypes.
        :return: A dict with key archetype class and value list of objects.
        """
        log.info('ArchetypeManager - load object archetypes')
        # Build archetypes directory name from archetype type
        archetypes_dir : str = join(ARCHETYPES_FOLDER, ArchetypesType.OBJECTS)

        # Scan all the subdirectories in the archetypes directory (one depth level only)
        # TODO: this means that ALL archetypes must be in one subdirectory, i.e., that
        #       no archetypes are supposed to be in the root directory, AND that only one
        #       level of subdirectories is allowed.
        subdirs : list[str] = [f for f in listdir(archetypes_dir) if isdir(join(archetypes_dir, f))]
        
        # We create a dictionary to store the result
        object_arquetype_dict : dict[str, list[Object]] = dict[str, list[Object]]()

        # For each subdirectory, containing the archetypes of a given class
        for subdir in subdirs:
            # We create a list to store the archetypes of the class
            object_arquetype_list : list[Object] = list[Object]()

            # Build the full path to the subdirectory
            object_archetype_class_path : str = join(archetypes_dir, subdir)

            # Get object pointer file. Inside we find inside it the ids that
            # referes to the objects and omit the rest of children objects
            objects_pointer_file : str = join(object_archetype_class_path, OBJECTS_FILE)

            # Parse the XML file
            objects_pointer_xml : ET.Element = ET.parse(objects_pointer_file)
            objects_id_list : list[str] = [child.attrib["id"] for child in objects_pointer_xml.getroot()]

            # For each object id, we create the object and add it to the list
            for object_id in objects_id_list:
                # We get the path of the object
                objects_path = join(object_archetype_class_path, "objects")
                object_path : str = join(objects_path,f'{object_id}.xml')

                # We create the object
                object : Object = Object(object_path)

                # We add it to the list
                object_arquetype_list.append(object)

            # We add the list to the dictionary
            object_arquetype_dict[subdir] = object_arquetype_list

        return object_arquetype_dict

    # ----------------------------------------------------------------------
    # Method: load_document_archetypes (static)
    # Description: It load document archetypes
    # Date: 13/04/2023
    # Version: 0.2
    # Author: Pablo Rivera Jiménez
    #         José María Delgado Sánchez
    # ----------------------------------------------------------------------

    @classmethod
    def load_document_archetypes( cls ) -> list:
        """
        Method that loads the document archetypes.
        :return: A list of documents (Objects) objects.
        """
        log.info('ArchetypeManager - load document archetypes')
        # Build archetypes directory name from archetype type
        archetypes_dir : str = join(ARCHETYPES_FOLDER, ArchetypesType.DOCUMENTS)

        # Scan all the subdirectories in the archetypes directory (one depth level only)
        # TODO: this means that ALL archetypes must be in one subdirectory, i.e., that
        #       no archetypes are supposed to be in the root directory, AND that only one
        #       level of subdirectories is allowed.
        subdirs : list[str] = [f for f in listdir(archetypes_dir) if isdir(join(archetypes_dir, f))]
        
        document_archetype_list : list[Object] = list ()

        # For each document archetype subdir
        for subdir in subdirs:
            # Build the full path to the subdirectory
            archetype_dir_path : str = join(archetypes_dir, subdir)

            # TODO: Check the archetype structure is correct and all files are present

            # Get document pointer file. Inside we find inside it the id that
            # referes to the main document (the one with class ':Proteus-document')
            document_pointer_file : str = join(archetype_dir_path, DOCUMENT_FILE)

            # Parse the XML file
            document_pointer_xml : ET.Element = ET.parse(document_pointer_file)

            # Get the id of the root document from document.xml
            document_id : str = document_pointer_xml.getroot().attrib["id"]

            # Build the path to the root document
            objects_path = join(archetype_dir_path, "objects")
            document_archetype_file_path = join(objects_path, document_id + ".xml")

            # We create an object from the archetype
            document_archetype : Object = Object(document_archetype_file_path)

            # We add it to the list
            document_archetype_list.append(document_archetype)

        return document_archetype_list


    # ----------------------------------------------------------------------
    # Method: load_project_archetypes (static)
    # Description: It loads project archetypes from archetypes repository
    # Date: 13/04/2023
    # Version: 0.2
    # Author: Pablo Rivera Jiménez
    #         José María Delgado Sánchez
    # ----------------------------------------------------------------------

    @classmethod
    def load_project_archetypes( cls ) -> list[Project]:
        """
        Method that loads the project archetypes in a list.
        :return: A list of Project objects.
        """
        log.info('ArchetypeManager - load project archetypes')
        # Build archetypes directory name from archetype type (project)
        archetypes_dir : str = join(ARCHETYPES_FOLDER, ArchetypesType.PROJECTS)

        # Scan all the subdirectories in the archetypes directory (one depth level only)
        # TODO: this means that ALL archetypes must be in one subdirectory, i.e., that
        #       no archetypes are supposed to be in the root directory, AND that only one
        #       level of subdirectories is allowed.
        subdirs : list[str] = [f for f in listdir(archetypes_dir) if isdir(join(archetypes_dir, f))]

        # Result as a list of Projects
        project_archetype_list : list [Project] = []

        # For each subdirectory
        for subdir in subdirs:
            # Build the full path to the project archetype file
            project_archetype_file_path : str = join(archetypes_dir, subdir, PROJECT_FILE)

            # We create a project from the archetype
            project_archetype : Project = Project(project_archetype_file_path)
            
            # We add it to the result list
            project_archetype_list.append(project_archetype)
        
        return project_archetype_list
    
    # ----------------------------------------------------------------------
    # Method     : clone_project
    # Description: It clones a project archetype into the sys path wanted.
    # Date       : 27/09/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    @staticmethod
    def clone_project(filename_path: str, filename_path_to_save: str):
        """
        Method that creates a new project from an archetype.
        :param filename: Path where we want to save the project.
        :param archetype: Archetype type.
        """
        
        # Directory where we save the project
        path = os.path.realpath(filename_path_to_save)
        
        # Directory where is the archetype
        archetype_dir = os.path.dirname(filename_path)

        # Copy the archetype to the project directory
        original = filename_path
        target = path
        shutil.copy(original, target)
        
        # In case there is no directory, create it
        if "assets" not in os.listdir(path):
            shutil.copytree(join(archetype_dir, "assets"), join(path, "assets"))

        # Copy the objects file from the archetypes directory into the project directory
        source_dir = join(archetype_dir, "objects")
        destination_dir = join(path, "objects")
        
        shutil.copytree(source_dir, destination_dir)