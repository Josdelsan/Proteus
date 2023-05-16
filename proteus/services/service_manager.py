# ==========================================================================
# File: service_manager.py
# Description: Service manager for the PROTEUS application. It is used to
#              manage the services instances.
# Date: 15/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.services.archetype_service import ArchetypeService
from proteus.services.project_service import ProjectService

# --------------------------------------------------------------------------
# Class: ServiceManager
# Description: Class for service management
# Date: 15/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@dataclass(init=False)
class ServiceManager:
    """
    Service manager for the PROTEUS application. It is used to manage the
    services instances providing a simple interface to access them.
    """

    # Instance attributes
    archetype_service: ArchetypeService = None
    _project_service: ProjectService = None

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor
    # Date       : 15/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self):
        """
        Class constructor
        """
        # Create an ArchetypeService instance
        self.archetype_service = ArchetypeService()

        # Create a ProjectService instance as None
        # It will be created when a project is opened
        self._project_service = None
        
    # ----------------------------------------------------------------------
    # Property   : project_service
    # Description: Getter for the project service instance
    # Date       : 15/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @property
    def project_service(self) -> ProjectService:
        """
        Getter for the project service instance. Check if the instance
        exists before returning it.
        """
        assert isinstance(self._project_service, ProjectService), \
            "You must load a project before using project service."
        
        return self._project_service
    
    # ----------------------------------------------------------------------
    # Method     : load_project
    # Description: Load a project and create the project service instance
    # Date       : 15/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def load_project(self, project_path: str) -> None:
        """
        Load a project and create the project service instance
        """
        assert project_path is not None, "Project path cannot be None"

        # Create a ProjectService instance
        self._project_service = ProjectService(project_path)


