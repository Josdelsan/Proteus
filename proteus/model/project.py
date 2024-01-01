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
# Update: 15/04/2023 (José María)
# Description:
# - Project now lazy loads its documents.
#   Project now has a method to clone itself into a new directory.
# ==========================================================================

# for using classes as return type hints in methods
# (this will change in Python 3.11)
from __future__ import annotations  # it has to be the first import

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------
import os
import pathlib
import shutil
import logging
from typing import List, MutableSet

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------
from proteus.model import (
    ID_ATTRIBUTE,
    NAME_ATTRIBUTE,
    DOCUMENT_TAG,
    DOCUMENTS_TAG,
    OBJECTS_REPOSITORY,
    PROJECT_TAG,
    ProteusID,
    PROJECT_FILE_NAME,
    PROTEUS_DOCUMENT,
    XSL_TEMPLATES_TAG,
    XLS_TEMPLATE_TAG,
)
from proteus.model.abstract_object import AbstractObject, ProteusState
from proteus.utils.config import Config

# if 'proteus.model.object' in sys.modules:
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

        :param path: path to the project file.
        :return: a PROTEUS project.
        """
        log.info(f"Loading a PROTEUS project from {path}.")

        # Check path is a directory
        assert os.path.isdir(
            path
        ), f"PROTEUS projects must be located in a directory. {path} is not a directory."

        # Complete path to project file
        project_file_path = f"{path}/{PROJECT_FILE_NAME}"

        # Check project file exists
        assert os.path.isfile(
            project_file_path
        ), f"PROTEUS project file {project_file_path} not found in {path}."

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

        :param project_file_path: path to the project file.
        """

        # Initialize property dictionary in superclass
        # TODO: pass some arguments?
        super().__init__(project_file_path)

        # Save the project path as a project's attribute
        # TODO: probably this can be factored up to superclass
        self.path = project_file_path

        # Parse and load XML into memory
        root: ET.Element = ET.parse(project_file_path).getroot()

        # Check root tag is <project>
        assert (
            root.tag == PROJECT_TAG
        ), f"PROTEUS project file {project_file_path} must have <{PROJECT_TAG}> as root element, not {root.tag}."

        # Get project ID from XML
        self.id = ProteusID(root.attrib[ID_ATTRIBUTE])

        # Load project's properties using superclass method
        super().load_properties(root)

        # Project's ids, this variable is set in get_ids method
        self._ids: MutableSet[ProteusID] = None

        # Template list
        self.xsl_templates: List[str] = self.load_xsl_templates(root)

        # Documents list
        self._documents: List[Object] = None

    # ----------------------------------------------------------------------
    # Property   : documents
    # Description: Property documents getter. Loads children from XML file
    #              on demand.
    # Date       : 12/04/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @property
    def documents(self) -> List[Object]:
        """
        Property documents getter. Loads documents from XML file on demand.
        :return: documents list.
        """
        # Check if documents list is not initialized
        if self._documents is None:
            # Initialize documents dictionary
            self._documents: List[Object] = []

            # Load documents from XML file
            self.load_documents()

        # Return documents list
        return self._documents

    # ----------------------------------------------------------------------
    # Property   : ids
    # Description: Property ids getter. Loads all ids from the project on
    #              demand.
    # Date       : 06/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @property
    def ids(self) -> MutableSet[ProteusID]:
        """
        Property ids getter. Loads all ids from the project on demand.

        This property is updated when add_descendant method is called
        in project and add_descendant in object.

        Ids must be recalculated when the project is saved.

        :return: ids set.
        """
        # Check if ids set is not initialized
        if self._ids is None:
            # Initialize ids set
            self._ids: MutableSet[ProteusID] = set()

            # Load ids from XML file
            self._ids = self.get_ids()

        # Return ids set
        return self._ids

    # ----------------------------------------------------------------------
    # Method     : load_documents
    # Description: It loads the documents of a PROTEUS project using an
    #              XML root element <project>.
    # Date       : 22/08/2022
    # Version    : 0.1
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def load_documents(self) -> None:
        """
        It loads a PROTEUS project's documents from an XML root element.
        :param root: XML root element.
        """
        # Parse and load XML into memory
        root: ET.Element = ET.parse(self.path).getroot()

        # Check root is not None
        assert root is not None, f"Root element is not valid in {self.path}."

        # Load documents
        documents_element: ET.Element = root.find(DOCUMENTS_TAG)

        # Check whether it has documents
        assert (
            documents_element is not None
        ), f"PROTEUS project file {self.path} does not have a <{DOCUMENTS_TAG}> element."

        # Parse project's documents
        # TODO: check document_element tag is <document>
        document_element: ET.Element
        for document_element in documents_element:
            document_id: ProteusID = document_element.attrib.get(ID_ATTRIBUTE, None)

            # Check whether the document has an ID
            assert (
                document_id is not None
            ), f"PROTEUS project file {self.path} includes a document without ID."

            # Add the document to the documents dictionary and set the parent
            object = Object.load(document_id, self)
            object.parent = self
            self.documents.append(object)

    # ----------------------------------------------------------------------
    # Method     : load_xsl_templates
    # Description: It loads the XSL templates of a PROTEUS project using an
    #              XML root element <project>.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def load_xsl_templates(self, root: ET.Element) -> List[str]:
        """
        It loads a PROTEUS project's XSL templates from an XML root element.

        :param root: XML root element.
        """
        # Check root is not None
        assert root is not None, f"Root element is not valid in {self.path}."

        # Load XSL templates
        xsl_templates_element: ET.Element = root.find(XSL_TEMPLATES_TAG)

        # Check whether it has XSL templates
        assert (
            xsl_templates_element is not None
        ), f"PROTEUS project file {self.path} does not have a <{XSL_TEMPLATES_TAG}> element."

        # Parse project's XSL templates
        xsl_template_element: ET.Element
        xsl_templates: List[str] = []
        for xsl_template_element in xsl_templates_element:
            xsl_template_name: str = xsl_template_element.attrib.get(NAME_ATTRIBUTE, None)

            # NOTE: Templates that are not in the system installation are
            #       ignored and not saved later
            if xsl_template_name in Config().xslt_routes:
                xsl_templates.append(xsl_template_name)
            else:
                log.warning(
                    f"XSL template '{xsl_template_name}' is not in the system installation and will be ignored. It will not be saved later if the project is modified."
                )

        # Return XSL templates
        return xsl_templates

    # ----------------------------------------------------------------------
    # Method     : get_descendants
    # Description: It returns a list with all the documents of a project.
    # Date       : 23/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_descendants(self) -> List[Object]:
        """
        It returns a list with all the documents of a project.
        :return: list with all the documents of a project.
        """
        # Return the list with all the descendants of an object
        return self.documents

    # ----------------------------------------------------------------------
    # Method     : add_descendants
    # Description: Adds a document to the project given a document and its
    #              position.
    # Date       : 26/04/2023
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def add_descendant(self, document: Object, position: int = None) -> None:
        """
        Method that adds a document to the project.

        :param document: Document to be added to the project.
        :param position: Position of the document in the project.
        """

        # If position is not specified, add the document at the end
        if position is None:
            position = len(self.documents)

        # Check if the document is a valid object
        assert isinstance(
            document, Object
        ), f"Document {document} is not a valid PROTEUS object."

        # Check if the document is a Proteus document
        assert (
            PROTEUS_DOCUMENT in document.classes
        ), f"The object is not a Proteus document. Object is class: {document.classes}"

        # Add the document to the project
        self.documents.insert(position, document)
        document.parent = self

        # Set dirty flag
        self.state = ProteusState.DIRTY

        # Add the document id to the ids set
        self.ids.add(document.id)

    # ----------------------------------------------------------------------
    # Method     : accept_descendant
    # Description: Checks if a child is accepted by a PROTEUS object.
    # Date       : 09/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def accept_descendant(self, child: Object) -> bool:
        """
        Checks if a child is accepted by a PROTEUS project. Projects only
        accept documents.

        :param child: Child Object to be checked.
        """
        # Check if the child is a valid object
        assert isinstance(
            child, Object
        ), f"Child {child} is not a valid PROTEUS object."

        # Check if the child is a document
        return PROTEUS_DOCUMENT in child.classes
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
        :return: an XML element for the project.
        """
        # Create <project> element and set ID
        project_element = ET.Element(PROJECT_TAG)
        project_element.set(ID_ATTRIBUTE, self.id)

        # Create <properties> element
        super().generate_xml_properties(project_element)

        # Create <documents> element
        documents_element = ET.SubElement(project_element, DOCUMENTS_TAG)

        # Create <document> subelements
        for document in self.documents:
            if document.state != ProteusState.DEAD:
                document_element = ET.SubElement(documents_element, DOCUMENT_TAG)
                document_element.set(ID_ATTRIBUTE, document.id)

        # Create <xsl_templates> element
        xsl_templates_element = ET.SubElement(project_element, XSL_TEMPLATES_TAG)

        # Create <xsl_template> subelements
        for xsl_template in self.xsl_templates:
            xsl_template_element = ET.SubElement(
                xsl_templates_element, XLS_TEMPLATE_TAG
            )
            xsl_template_element.set(NAME_ATTRIBUTE, xsl_template)

        return project_element

    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: It saves a project in the system.
    # Date       : 01/05/2023
    # Version    : 0.2
    # Author     : Pablo Rivera Jiménez
    #              José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def save_project(self) -> None:
        """
        It saves a project in the system.
        """
        # Save all the documents
        documents = list(self.documents)
        for document in documents:
            document.save()

        # Persist the project only if it is DIRTY or FRESH
        if self.state == ProteusState.DIRTY or self.state == ProteusState.FRESH:
            root = self.generate_xml()

            # Get the elementTree, save it in the project path and set state to clean
            tree = ET.ElementTree(root)
            tree.write(
                self.path, pretty_print=True, xml_declaration=True, encoding="utf-8"
            )
            self.state = ProteusState.CLEAN

        # Set the ids set to None to recalculate them when they are needed
        # This is done to delete the ids of the deleted documents
        self._ids = None

        log.info(f"Project saved successfully.")

    # ----------------------------------------------------------------------
    # Method     : clone_project
    # Description: It clones a project into the selected system path.
    # Date       : 13/04/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------

    def clone_project(
        self, filename_path_to_save: str, new_project_dir_name: str
    ) -> None:
        """
        Method that creates a new project from an existing project.

        :param filename: Path where we want to save the project.
        :param new_project_dir_name: Name of the new project directory.
        :return: The new project.
        """
        log.info(
            f"Cloning project {self.id} into {filename_path_to_save} with name {new_project_dir_name}"
        )

        assert os.path.isdir(
            filename_path_to_save
        ), f"The given path is not a directory: {filename_path_to_save}"

        # Directory where we save the project
        target_dir = (
            pathlib.Path(filename_path_to_save).resolve() / new_project_dir_name
        )

        # Directory where the project is located
        project_dir = pathlib.Path(self.path).parent.resolve()

        # Check the objects directory and the project file exists (or project archetype file)
        assert os.path.isdir(
            project_dir / OBJECTS_REPOSITORY
        ), f"The objects directory does not exist: {project_dir / OBJECTS_REPOSITORY}"
        assert os.path.isfile(project_dir / PROJECT_FILE_NAME) or os.path.isfile(
            project_dir / "project.xml"
        ), f"The project file does not exist in {project_dir}"

        shutil.copytree(project_dir, target_dir)

        # Check if the project is an archetype then change the project file
        project_arquetype_file = target_dir / "project.xml"
        if os.path.isfile(project_arquetype_file):
            project_file = target_dir / PROJECT_FILE_NAME
            os.rename(project_arquetype_file, project_file)

        # Load the new project to check if it is correct
        cloned_project: Project = Project.load(target_dir)
        assert (
            cloned_project is not None
        ), f"Error loading the cloned project {target_dir}"

        log.info(f"Project cloned successfully.")
        return cloned_project
