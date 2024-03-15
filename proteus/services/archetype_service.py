# ==========================================================================
# File: archetype_service.py
# Description: Archetypes repository interface
# Date: 07/04/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import Union, List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.application.configuration.config import Config
from proteus.model import ProteusID, PROTEUS_ANY, ProteusClassTag
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.archetype_repository import ArchetypeRepository

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: ArchetypeService
# Description: Class for Archetypes repository interface
# Date: 07/04/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ArchetypeService:
    """
    Acts as an interface for the Archetypes repository.
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
        self._project_archetypes: List[Project] = None
        self._document_archetypes: List[Object] = None

        self._object_archetypes: Dict[str, Dict[str, List[Object]]] = None
        self._unordered_object_archetypes: List[Object] = None

        self.archetype_index: Dict[ProteusID, Union[Project, Object]] = {}

        log.info("ArchetypeService initialized")

    # ----------------------------------------------------------------------
    # Property   : get_project_archetypes
    # Description: Project_archetypes getter. Loads the list of
    #              project archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_project_archetypes(self) -> List[Project]:
        """
        Project_archetypes getter. Loads the list of project archetypes on demand.
        """
        # Lazy loading of project archetypes
        if self._project_archetypes is None:
            # Load project archetypes using ArchetypeRepository
            self._project_archetypes = ArchetypeRepository.load_project_archetypes(
                archetypes_folder=Config().profile_settings.selected_archetype_repository_path
            )

            # Check that the list of project archetypes is a list
            assert isinstance(
                self._project_archetypes, list
            ), f"Could not load project archetypes. ArchetypeRepository returned {self._project_archetypes}"

            # Populate the archetype index
            for project in self._project_archetypes:
                # Check for collisions
                assert (
                    project.id not in self.archetype_index
                ), f"Project archetype id {project.id} already exists in the archetype index"

                # Add the project archetype to the archetype index
                self.archetype_index[project.id] = project

        return self._project_archetypes

    # ----------------------------------------------------------------------
    # Property   : get_document_archetypes
    # Description: Document_archetypes getter. Loads the list of
    #              document archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_document_archetypes(self) -> List[Object]:
        """
        Document_archetypes getter. Loads the list of document archetypes on demand.
        """
        # Lazy loading of document archetypes
        if self._document_archetypes is None:
            # Load document archetypes using the ArchetypeRepository
            self._document_archetypes = ArchetypeRepository.load_document_archetypes(
                archetypes_folder=Config().profile_settings.selected_archetype_repository_path
            )

            # Check that the list of document archetypes is a list
            assert isinstance(
                self._document_archetypes, list
            ), f"Could not load document archetypes. ArchetypeRepository returned {self._document_archetypes}"

            # Populate the archetype index
            for document in self._document_archetypes:
                # Check for collisions
                assert (
                    document.id not in self.archetype_index
                ), f"Document archetype id {document.id} already exists in the archetype index"

                # Add the document archetype to the archetype index
                self.archetype_index[document.id] = document

        return self._document_archetypes

    # ----------------------------------------------------------------------
    # Property   : get_object_archetypes
    # Description: Object_archetypes getter. Loads the list of
    #              object archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_archetypes(self) -> Dict[str, Dict[str, List[Object]]]:
        """
        Object_archetypes getter. Loads the list of object archetypes on demand.
        """
        # Lazy loading of object archetypes
        if self._object_archetypes is None:
            # Load object archetypes using the ArchetypeRepository
            self._object_archetypes = ArchetypeRepository.load_object_archetypes(
                archetypes_folder=Config().profile_settings.selected_archetype_repository_path
            )

            # Check that the dict of object archetypes is a dict
            assert isinstance(
                self._object_archetypes, dict
            ), f"Could not load object archetypes. ArchetypeRepository returned {self._object_archetypes}"

            # ------------------------------------------------------------------
            # Populate non ordered list of object archetypes
            self._unordered_object_archetypes = []
            for arch_by_class in self._object_archetypes.values():
                for arch_list in arch_by_class.values():
                    self._unordered_object_archetypes.extend(arch_list)

            # ------------------------------------------------------------------
            # Populate the archetype index
            for object in self._unordered_object_archetypes:
                # Check for collisions
                assert (
                    object.id not in self.archetype_index
                ), f"Object archetype id {object.id} already exists in the archetype index"

                # Add the object archetype to the archetype index
                self.archetype_index[object.id] = object

        return self._object_archetypes

    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes_groups
    # Description: Returns the list of object archetypes groups
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_archetypes_groups(self) -> List[str]:
        """
        Returns the list of object archetypes types.
        """
        return list(self.get_object_archetypes().keys())

    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes_by_type
    # Description: Returns the list of object archetypes for a given group
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_archetypes_by_group(self, group: str) -> Dict[str, List[Object]]:
        """
        Returns the list of object archetypes for a given type.
        """
        return self.get_object_archetypes()[group]

    # ----------------------------------------------------------------------
    # Method     : get_first_level_object_archetypes
    # Description: Returns the list of first level object archetypes
    # Date       : 31/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_first_level_object_archetypes(self) -> Dict[str, Dict[str, List[Object]]]:
        """
        Returns the list of first level object archetypes.
        """
        # Copy the dict of object archetypes to pop second level objects
        archetypes: Dict[str, Dict[str, List[Object]]] = (
            self.get_object_archetypes().copy()
        )

        # Iterate over the archetype groups and classes
        for group in archetypes.keys():

            empty_keys: List[str] = []

            for _class in archetypes[group].keys():
                # Remove the second level objects
                for object in archetypes[group][_class]:
                    if PROTEUS_ANY not in object.acceptedParents:
                        archetypes[group][_class].remove(object)
                        if len(archetypes[group][_class]) == 0:
                            empty_keys.append(_class)

            # Remove empty keys
            for key in empty_keys:
                archetypes[group].pop(key)

        return archetypes

    # ----------------------------------------------------------------------
    # Method     : get_accepted_object_archetypes
    # Description: Returns the dict of accepted object archetypes for a given
    #              accepted children list. Archetype must accept the given
    #              parent explicitly in the acceptedParents list.
    # Date       : 31/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_accepted_object_archetypes(self, object: Object) -> Dict[str, List[Object]]:
        """
        Returns the dict of accepted object archetypes for a given
        object. The given object must accept the archetype explicitly
        in the acceptedChildren list.

        Dictionary store accepted objects by their classes. This is
        done to group objects by their class when displaying.

        :param accepted_children: List of accepted children classes
        :return: Dictionary of accepted object archetypes by object class
        """
        # Dict to store the accepted object archetypes
        dict: Dict[str, List[Object]] = {}

        # Iterate over the archetypes
        for archetype in self._unordered_object_archetypes:
            # Check acceptation conditions
            # object must accept the archetype
            condition_1: bool = object.accept_descendant(archetype)

            # archetype class must be explicitly in acceptedChildren
            # NOTE: This is done to avoid showing all the accepted archetypes,
            # sections accept :Proteus-any so the list would be huge
            accepted_children_common_classes = [
                c for c in object.acceptedChildren if c in archetype.classes
            ]
            condition_2: bool = len(accepted_children_common_classes) > 0

            # If BOTH conditions are met, add the archetype to its corresponding list
            if condition_1 and condition_2:
                # Check if the archetype class is already in the dict
                archetype_main_class: ProteusClassTag = archetype.classes[-1]
                if archetype_main_class in dict:
                    # Add the archetype to the list
                    dict[archetype_main_class].append(archetype)
                else:
                    # Create a new list with the archetype
                    dict[archetype_main_class] = [archetype]

        return dict

    # ----------------------------------------------------------------------
    # Method     : get_archetype_by_id
    # Description: Returns the archetype with the given id
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _get_archetype_by_id(self, archetype_id: ProteusID) -> Union[Project, Object]:
        """
        Returns the archetype with the given id.
        """
        # Check that the archetype id is valid
        assert (
            archetype_id in self.archetype_index
        ), f"Archetype with id {archetype_id} was not found"

        return self.archetype_index[archetype_id]

    # ----------------------------------------------------------------------
    # Method     : create_project
    # Description: Creates a new project from an archetype given a path,
    #              a name and an archetype id.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_project(
        self, archetype_id: ProteusID, project_name: str, save_path: str
    ) -> None:
        """
        Creates a new project from an archetype given a path,
        a name and an archetype id.
        """
        # Check that the project name is not empty
        assert (
            project_name != "" and project_name is not None
        ), "Project must have a valid name"

        # Get the project archetype
        project_archetype = self._get_archetype_by_id(archetype_id)

        # Check that the archetype is a project archetype
        assert isinstance(
            project_archetype, Project
        ), f"Archetype with id {archetype_id} is not a project archetype"

        # Create the project from the archetype
        project_archetype.clone_project(save_path, project_name)

    # ----------------------------------------------------------------------
    # Method     : create_object
    # Description: Creates a new object/document from an archetype given the
    # new parent, project and an archetype id.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_object(
        self, archetype_id: ProteusID, parent: Object, project: Project
    ) -> Object:
        """
        Creates a new object/document from an archetype given the new parent,
        project and an archetype id.
        """
        # Get the object archetype
        object_archetype = self._get_archetype_by_id(archetype_id)

        # Check that the archetype is an object archetype
        assert isinstance(
            object_archetype, Object
        ), f"Archetype with id {archetype_id} is not an object archetype"

        # Create the object from the archetype
        return object_archetype.clone_object(parent, project)
