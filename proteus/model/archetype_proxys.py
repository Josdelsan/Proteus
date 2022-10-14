# ==========================================================================
# File: archetype_proxys.py
# Description: PROTEUS project archetype proxy
# Date: 07/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
# ==========================================================================

# Avoid circle import
from __future__ import annotations

import datetime
import proteus.model.object as object
import proteus.model.project as project


# --------------------------------------------------------------------------
# Class: ProjectArchetypeProxy
# Description: Proxy class for managing PROTEUS archetypes
# Date: 07/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class ProjectArchetypeProxy: 

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a ProjectArchetypeProxy object.
    # Date       : 07/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def __init__(self, data : dict):
        self.path : str = data["path"]
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.description : str = data["description"]
        self.author : str = data["author"]
        self.date : datetime = data["date"]

    # ----------------------------------------------------------------------
    # Method     : get_project
    # Description: It returns an instance of a project.
    # Date       : 07/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def get_project(self) -> project.Project:
        return project.Project(self.path)


# --------------------------------------------------------------------------
# Class: DocumentArchetypeProxy
# Description: Proxy class for managing PROTEUS archetypes
# Date: 08/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class DocumentArchetypeProxy:


    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a DocumentArchetypeProxy object.
    # Date       : 08/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def __init__(self, data : dict):
        self.path : str = data["path"]
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.description : str = data["description"]
        self.author : str = data["author"]
        self.date : datetime = data["date"] 
        
    # ----------------------------------------------------------------------
    # Method     : get_project
    # Description: It returns an instance of a object.
    # Date       : 08/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # # ----------------------------------------------------------------------
    def get_document(self, project: project.Project) -> object.Object:
        return object.Object(project, self.path)