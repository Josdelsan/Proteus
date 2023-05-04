# ==========================================================================
# File: archetype_service.py
# Description: Archetypes repository interface
# Date: 07/04/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass, field
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
@dataclass
class ArchetypeService():
    """
    Acts as an interface for the Archetypes repository.
    """

    _project_archetypes  : List[Project]                           = None
    _document_archetypes : List[Object]                            = None
    _object_archetypes   : Dict[str, List[Object]]                 = None
    archetype_index      : Dict[ProteusID, Union[Project, Object]] = field(default_factory=dict)

    # ----------------------------------------------------------------------
    # Property   : project_archetypes
    # Description: Property project_archetypes getter. Loads the list of
    #              project archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @property
    def project_archetypes(self) -> List[Project]:
        """
        Property for the list of project archetypes.
        """
        # Lazy loading of project archetypes
        if self._project_archetypes is None:
            # Load project archetypes using the ArchetypeManager
            self._project_archetypes = ArchetypeManager.load_project_archetypes()

            # Check that the list of project archetypes is a list
            assert isinstance(self._project_archetypes,list), \
                f"Could not load project archetypes. ArchetypeManager returned {self._project_archetypes}"
            
            # Populate the archetype index
            for project in self._project_archetypes:
                # Check for collisions
                assert project.id not in self.archetype_index, \
                    f"Project archetype id {project.id} already exists in the archetype index"

                # Add the project archetype to the archetype index
                self.archetype_index[project.id] = project

        return self._project_archetypes
    
    # ----------------------------------------------------------------------
    # Property   : document_archetypes
    # Description: Property document_archetypes getter. Loads the list of
    #              document archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @property
    def document_archetypes(self) -> List[Object]:
        """
        Property for the list of document archetypes.
        """
        # Lazy loading of document archetypes
        if self._document_archetypes is None:
            # Load document archetypes using the ArchetypeManager
            self._document_archetypes = ArchetypeManager.load_document_archetypes()

            # Check that the list of document archetypes is a list
            assert isinstance(self._document_archetypes,list), \
                f"Could not load document archetypes. ArchetypeManager returned {self._document_archetypes}"
            
            # Populate the archetype index
            for document in self._document_archetypes:
                # Check for collisions
                assert document.id not in self.archetype_index, \
                    f"Document archetype id {document.id} already exists in the archetype index"
                
                # Add the document archetype to the archetype index
                self.archetype_index[document.id] = document

        return self._document_archetypes

    # ----------------------------------------------------------------------
    # Property   : object_archetypes
    # Description: Property object_archetypes getter. Loads the list of
    #              object archetypes on demand.
    # Date       : 02/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @property
    def object_archetypes(self) -> Dict[str, List[Object]]:
        """
        Property for the list of object archetypes.
        """
        # Lazy loading of object archetypes
        if self._object_archetypes is None:
            # Load object archetypes using the ArchetypeManager
            self._object_archetypes = ArchetypeManager.load_object_archetypes()

            # Check that the list of object archetypes is a list
            assert isinstance(self._object_archetypes,dict), \
                f"Could not load object archetypes. ArchetypeManager returned {self._object_archetypes}"
            
            # Populate the archetype index
            for object_type in self._object_archetypes.keys():
                for object in self._object_archetypes[object_type]:
                    # Check for collisions
                    assert object.id not in self.archetype_index, \
                        f"Object archetype id {object.id} already exists in the archetype index"

                    # Add the object archetype to the archetype index
                    self.archetype_index[object.id] = object

        return self._object_archetypes
    
    # ----------------------------------------------------------------------
    # Method     : get_project_archetypes
    # Description: Returns the list of project archetypes
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_project_archetypes(self) -> List[Project]:
        """
        Returns the list of project archetypes.
        """
        return self.project_archetypes
    
    # ----------------------------------------------------------------------
    # Method     : get_document_archetypes
    # Description: Returns the list of document archetypes
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_document_archetypes(self) -> List[Object]:
        """
        Returns the list of document archetypes.
        """
        return self.document_archetypes
    
    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes_classes
    # Description: Returns the list of object archetypes classes
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_archetypes_classes(self) -> List[str]:
        """
        Returns the list of object archetypes classes.
        """
        return list(self.object_archetypes.keys())
    
    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes_by_class
    # Description: Returns the list of object archetypes for a given class
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_archetypes_by_class(self, object_class : str) -> List[Object]:
        """
        Returns the list of object archetypes for a given class.
        """
        return self.object_archetypes[object_class]
    
    # ----------------------------------------------------------------------
    # Method     : get_archetype_by_id
    # Description: Returns the archetype with the given id
    # Date       : 04/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_archetype_by_id(self, archetype_id : ProteusID) -> Union[Project, Object]:
        """
        Returns the archetype with the given id.
        """
        return self.archetype_index[archetype_id]