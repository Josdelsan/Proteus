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
@dataclass
class ServiceManager:
    """
    Service manager for the PROTEUS application. It is used to manage the
    services instances providing a simple interface to access them.
    """

    # Class attributes
    archetype_service: ArchetypeService = None
    project_service: ProjectService = None

    @classmethod
    def get_archetype_service_instance(cls) -> ArchetypeService:
        if not cls.archetype_service:
            cls.archetype_service = ArchetypeService()
        return cls.archetype_service
    
    @classmethod
    def get_project_service_instance(cls) -> ProjectService:
        if not cls.project_service:
            cls.project_service = ProjectService()
        return cls.project_service


