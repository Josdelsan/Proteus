# ==========================================================================
# File: project.py
# Description: a PROTEUS project
# Date: 07/08/2022
# Version: 0.2
# Author: Amador Durán Toro
# ==========================================================================
# Update: 15/09/2022 (Amador)
# Description:
# - Project now inherits from AbstractObject
# ==========================================================================

# imports

# for using classes as return type hints in methods
# (this will change in Python 3.11)
from __future__ import annotations # it has to be the first import

# standard library imports
import os
from os.path import join
import shutil
import logging
import lxml.etree as ET

# local imports (starting from root)
from proteus.model import DOCUMENT_TAG, DOCUMENTS_TAG, OBJECTS_REPOSITORY, PROJECT_TAG, ProteusID, PROJECT_FILE_NAME
from proteus.model.abstract_object import AbstractObject, ProteusState
import proteus.model.archetype_manager as archetypes
#if 'proteus.model.object' in sys.modules:
#    from proteus.model.object import Object
from proteus.model.object import Object

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: Project
# Description: Class for PROTEUS projects
# Date: 07/08/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class Project(AbstractObject):
    """
    A PROTEUS project is a 'proteus.xml' file inside a directory with 'objects'
    and 'assets' directories. The 'proteus.xml' must describe the projects
    properties and the short UUIDs of their documents (which are PROTEUS objects
    of with class tag ':Proteus-Document'.

    A PROTEUS project can only be created by cloning another existing project,
    usually an archetype project.

    An already created project can be loaded by providing the path to its
    directory.
    """
    # ----------------------------------------------------------------------
    # Method: load (static)
    # Description: It loads a PROTEUS project from disk into memory
    # Date: 22/08/2022
    # Version: 0.1
    # Author: Amador Durán Toro
    # ----------------------------------------------------------------------

    @staticmethod
    def load(path: str) -> Project:
        """
        Static factory method for loading a PROTEUS project from a given path.
        """
        log.info(f"Loading a PROTEUS project from {path}.")

        # Check path is a directory
        assert os.path.isdir(path), \
            f"PROTEUS projects must be located in a directory. {path} is not a directory."

        # Change the current working directory
        os.chdir(path)

        # Complete path to project file
        project_file_path = f"./{PROJECT_FILE_NAME}"

        # Check project file exists
        assert os.path.isfile(project_file_path), \
            f"PROTEUS project file {project_file_path} not found in {path}."

        # Create and return the project object
        return Project(project_file_path)

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a PROTEUS project and builds it using an
    #              XML file.
    # Date       : 22/08/2022
    # Version    : 0.2
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def __init__(self, project_file_path: str) -> None:
        """
        It initializes and builds a PROTEUS project from an XML file.
        """

        # Initialize property dictionary in superclass
        # TODO: pass some arguments?
        super().__init__(project_file_path)

        # Save the project path as a project's attribute
        # TODO: probably this can be factored up to superclass
        self.path = project_file_path

        # Parse and load XML into memory
        root : ET.Element = ET.parse( project_file_path ).getroot()

        # Check root tag is <project>
        assert root.tag == PROJECT_TAG, \
            f"PROTUES project file {project_file_path} must have <{PROJECT_TAG}> as root element, not {root.tag}."

        # Get project ID from XML
        self.id = ProteusID(root.attrib['id'])

        # Load project's properties using superclass method
        super().load_properties(root)

        # Documents dictionary
        self.documents : dict[ProteusID,Object] = dict[ProteusID,Object]()

        # Load project's documents
        self.load_documents(root)

    # ----------------------------------------------------------------------
    # Method     : load_documents
    # Description: It loads the documents of a PROTEUS project using an
    #              XML root element <project>.
    # Date       : 22/08/2022
    # Version    : 0.1
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def load_documents(self, root : ET.Element) -> None:
        """
        It loads a PROTEUS project's documents from an XML root element.
        """

        # Check root is not None
        assert root is not None, \
            f"Root element is not valid in {self.path}."

        # Load documents
        documents_element : ET.Element = root.find(DOCUMENTS_TAG)

        # Check whether it has documents
        assert documents_element is not None, \
            f"PROTEUS project file {self.path} does not have a <{DOCUMENTS_TAG}> element."

        # Parse project's documents
        # TODO: check document_element tag is <document>
        document_element : ET.Element
        for document_element in documents_element:
            document_id : ProteusID = document_element.attrib.get('id', None)

            # Check whether the document has an ID
            assert document_id is not None, \
                f"PROTEUS project file {self.path} includes a document without ID."

            # Add the document to the documents dictionary
            self.documents[document_id] = Object.load(self, document_id)

    # ----------------------------------------------------------------------
    # Method     : generate_xml
    # Description: It generates an XML element for the project.
    # Date       : 26/08/2022
    # Version    : 0.1
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def generate_xml(self) -> ET.Element:
        """
        It generates an XML element for the project.
        """
        # Create <project> element and set ID
        project_element = ET.Element(PROJECT_TAG)
        project_element.set('id', self.id)

        # Create <properties> element
        super().generate_xml_properties(project_element)

        # Create <documents> element
        documents_element = ET.SubElement(project_element, DOCUMENTS_TAG)

        # Create <document> subelements
        for document in self.documents.values():
            document_element = ET.SubElement(documents_element, DOCUMENT_TAG)
            document_element.set('id', document.id)

        return project_element

    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: It saves a project in the system.
    # Date       : 27/09/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    def save_project(self):
        print("Saving project...")

        # Extract project directory from project path
        project_directory : str = os.path.dirname(self.path)
        
        # Create path to objects repository
        objects_repository : str = f"{project_directory}/{OBJECTS_REPOSITORY}"
        
        # If the Project is dead (Deleted/removed)
        if(self.state == ProteusState.DEAD):
            # If the project was already saved in OS and not in memory:
            if(os.path.isfile(self.path)):
                pass
            for document in self.documents.values():
                document.state = ProteusState.DEAD
        
        # If the Project is Dirty
        elif(self.state == ProteusState.DIRTY):
            root = self.generate_xml()
            # In case we can set any indent
            # ET.indent(root, "    ")

            # Get the elementTree, save it in the project path and set state to clean
            tree = ET.ElementTree(root)
            tree.write(self.path, pretty_print=True, xml_declaration=True, encoding="utf-8")
            self.state == ProteusState.CLEAN
        
        # For each document in the project
        for document in self.documents.values():
            document_path = f"{objects_repository}/{document.id}.xml"

            # If the document is DEAD (Deleted)
            if(document.state == ProteusState.DEAD):
                
                # If the document has children, we get the children and set them to DEAD
                if(document.children):
                    def delete_children(children : dict[ProteusID,Object]):
                        child: Object
                        for child in children.values():
                            child_path = f"{objects_repository}/{child.id}.xml"

                            child.state = ProteusState.DEAD

                            # If the document exists (not in memory), we deleted from os
                            if(os.path.isfile(child_path)):
                                #TODO remove from OS
                                pass
                            delete_children(child.children)
                    delete_children(document.children)
                
                # If the document exists (not in memory), we deleted from os
                if(os.path.isfile(document_path)):
                    #TODO remove from OS
                    pass
            
            # If the state of the document is DIRTY or FRESH, we save it
            elif(document.state == ProteusState.DIRTY or document.state == ProteusState.FRESH):
                root = document.generate_xml()
                # In case we can set any indent
                # ET.indent(root, "    ")
                tree = ET.ElementTree(root)
                tree.write(document_path, pretty_print=True, xml_declaration=True, encoding="utf-8")
                document.state == ProteusState.CLEAN

            if(document.children):
                # If the document has children we save them and if the child has children
                # we save them as well
                def save_children(parent: Object):
                    child: Object
                    for child in document.children.values():

                        child_path = f"{objects_repository}/{child.id}.xml"
                        child_root = child.generate_xml()
                        
                        if((child.state == ProteusState.DIRTY or child.state == ProteusState.FRESH)
                            and parent.state != ProteusState.DEAD):
                            # In case we can set any indent
                            # ET.indent(root, "    ")
                            
                            tree = ET.ElementTree(child_root)
                            tree.write(child_path, pretty_print=True, xml_declaration=True, encoding="utf-8")
                            child.state == ProteusState.CLEAN
                        if(child.state == ProteusState.DEAD or parent.state == ProteusState.DEAD):
                            #Remove from OS
                            child.state = ProteusState.DEAD
                            pass
                save_children(document)

    # ----------------------------------------------------------------------
    # Method     : clone_project
    # Description: It clones a project archetype into the sys path wanted.
    # Date       : 27/09/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    # TODO -> MOVE TO ARCHETYPES?
    @staticmethod
    def clone_project(filename_path_to_save: str, filename_path: str):
        """
        Method that creates a new project from an archetype.

        :param filename: Path where we want to save the project.
        :param archetype: Archetype type.
        """
        # Directory where we save the project
        path = os.path.dirname(os.path.realpath(filename_path_to_save))

        # Directory where is the archetype
        archetype_dir = os.path.dirname(filename_path)

        # Copy the archetype to the project directory
        original = filename_path
        target = filename_path_to_save
        shutil.copyfile(original, target)

        # In case there is no directory, create it
        if "assets" not in os.listdir(os.path.dirname(filename_path_to_save)):
            os.mkdir(join(path, "assets"))
            shutil.copytree(archetype_dir / "assets", path / "assets")

        #TODO remove this if in future. This if is just because otherwise while testing it will fail.
        if "objects" not in os.listdir(archetype_dir):
            # Copy the objects file from the archetypes directory into the project directory
            source_dir = join(archetype_dir, "objects")
            destination_dir = join(path, "objects")
            shutil.copytree(source_dir, destination_dir)


