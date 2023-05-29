# ==========================================================================
# File: archetype_service.py
# Description: Archetypes repository interface
# Date: 07/04/2023
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
from proteus.model.archetype_manager import ArchetypeManager

# --------------------------------------------------------------------------
# Class: ArchetypeService
# Description: Class for Archetypes repository interface
# Date: 07/04/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ArchetypeService():
    """
    Acts as an interface for the Archetypes repository.
    """

    # Class attributes
    _project_archetypes  : List[Project]                           = None
    _document_archetypes : List[Object]                            = None
    _object_archetypes   : Dict[str, List[Object]]                 = None
    archetype_index      : Dict[ProteusID,Union[Project, Object]]  = {}

    # ----------------------------------------------------------------------
    # Property   : get_project_archetypes
    # Description: Project_archetypes getter. Loads the list of
    #              project archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_project_archetypes(cls) -> List[Project]:
        """
        Project_archetypes getter. Loads the list of project archetypes on demand.
        """
        # Lazy loading of project archetypes
        if cls._project_archetypes is None:
            # Load project archetypes using the ArchetypeManager
            cls._project_archetypes = ArchetypeManager.load_project_archetypes()

            # Check that the list of project archetypes is a list
            assert isinstance(cls._project_archetypes,list), \
                f"Could not load project archetypes. ArchetypeManager returned {cls._project_archetypes}"
            
            # Populate the archetype index
            for project in cls._project_archetypes:
                # Check for collisions
                assert project.id not in cls.archetype_index, \
                    f"Project archetype id {project.id} already exists in the archetype index"

                # Add the project archetype to the archetype index
                cls.archetype_index[project.id] = project

        return cls._project_archetypes
    
    # ----------------------------------------------------------------------
    # Property   : get_document_archetypes
    # Description: Document_archetypes getter. Loads the list of
    #              document archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_document_archetypes(cls) -> List[Object]:
        """
        Document_archetypes getter. Loads the list of document archetypes on demand.
        """
        # Lazy loading of document archetypes
        if cls._document_archetypes is None:
            # Load document archetypes using the ArchetypeManager
            cls._document_archetypes = ArchetypeManager.load_document_archetypes()

            # Check that the list of document archetypes is a list
            assert isinstance(cls._document_archetypes,list), \
                f"Could not load document archetypes. ArchetypeManager returned {cls._document_archetypes}"
            
            # Populate the archetype index
            for document in cls._document_archetypes:
                # Check for collisions
                assert document.id not in cls.archetype_index, \
                    f"Document archetype id {document.id} already exists in the archetype index"
                
                # Add the document archetype to the archetype index
                cls.archetype_index[document.id] = document

        return cls._document_archetypes

    # ----------------------------------------------------------------------
    # Property   : get_object_archetypes
    # Description: Object_archetypes getter. Loads the list of
    #              object archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_object_archetypes(cls) -> Dict[str, List[Object]]:
        """
        Object_archetypes getter. Loads the list of object archetypes on demand.
        """
        # Lazy loading of object archetypes
        if cls._object_archetypes is None:
            # Load object archetypes using the ArchetypeManager
            cls._object_archetypes = ArchetypeManager.load_object_archetypes()

            # Check that the list of object archetypes is a list
            assert isinstance(cls._object_archetypes,dict), \
                f"Could not load object archetypes. ArchetypeManager returned {cls._object_archetypes}"
            
            # Populate the archetype index
            for object_type in cls._object_archetypes.keys():
                for object in cls._object_archetypes[object_type]:
                    # Check for collisions
                    assert object.id not in cls.archetype_index, \
                        f"Object archetype id {object.id} already exists in the archetype index"

                    # Add the object archetype to the archetype index
                    cls.archetype_index[object.id] = object

        return cls._object_archetypes
    
    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes_classes
    # Description: Returns the list of object archetypes classes
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_object_archetypes_classes(cls) -> List[str]:
        """
        Returns the list of object archetypes classes.
        """
        return list(cls.get_object_archetypes().keys())
    
    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes_by_class
    # Description: Returns the list of object archetypes for a given class
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_object_archetypes_by_class(cls, object_class : str) -> List[Object]:
        """
        Returns the list of object archetypes for a given class.
        """
        return cls.get_object_archetypes()[object_class]
    
    # ----------------------------------------------------------------------
    # Method     : get_archetype_by_id
    # Description: Returns the archetype with the given id
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def _get_archetype_by_id(cls, archetype_id : ProteusID) -> Union[Project, Object]:
        """
        Returns the archetype with the given id.
        """
        # Check that the archetype id is valid
        assert archetype_id in cls.archetype_index, \
            f"Archetype with id {archetype_id} was not found"

        return cls.archetype_index[archetype_id]
    
    # ----------------------------------------------------------------------
    # Method     : create_project
    # Description: Creates a new project from an archetype given a path,
    #              a name and an archetype id.
    # Date       : 06/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def create_project(cls,
                       archetype_id : ProteusID,
                       project_name : str,
                       save_path : str
                       ) -> None:
        """
        Creates a new project from an archetype given a path,
        a name and an archetype id.
        """
        # Check that the project name is not empty
        assert project_name != "" and project_name is not None, \
            "Project must have a valid name"

        # Get the project archetype
        project_archetype = cls._get_archetype_by_id(archetype_id)

        # Check that the archetype is a project archetype
        assert isinstance(project_archetype, Project), \
            f"Archetype with id {archetype_id} is not a project archetype"

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
    @classmethod
    def create_object(cls,
                      archetype_id : ProteusID,
                      parent : Object,
                      project : Project
                      ) -> None:
        """
        Creates a new object/document from an archetype given the new parent,
        project and an archetype id.
        """
        # Get the object archetype
        object_archetype = cls._get_archetype_by_id(archetype_id)

        # Check that the archetype is an object archetype
        assert isinstance(object_archetype, Object), \
            f"Archetype with id {archetype_id} is not an object archetype"

        # Create the object from the archetype
        object_archetype.clone_object(parent, project)