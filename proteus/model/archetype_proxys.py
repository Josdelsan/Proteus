# ==========================================================================
# File: archetype_proxys.py
# Description: PROTEUS project archetype proxy
# Date: 07/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
# ==========================================================================
import datetime
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.object import Object
from proteus.model.project import Project


# --------------------------------------------------------------------------
# Class: ProjectArchetypeProxy
# Description: Proxy class for managing PROTEUS archetypes
# Date: 07/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class ProjectArchetypeProxy: 


    # ----------------------------------------------------------------------
    # Method: load (static)
    # Description: It loads a PROTEUS project archetypes
    # Date: 07/10/2022
    # Version: 0.1
    # Author: Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    @staticmethod
    def load():
        project_archetypes = ArchetypeManager.load_project_archetypes()
        result: list = []
        for project_archetype in project_archetypes:
            archetype_proxy = ProjectArchetypeProxy(project_archetype)
            result.append(archetype_proxy)
        return result


    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a ProjectArchetypeProxy object.
    # Date       : 07/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def __init__(self, data :list):
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
    def get_project(self) -> Project:
        return Project(self.path)


# --------------------------------------------------------------------------
# Class: DocumentArchetypeProxy
# Description: Proxy class for managing PROTEUS archetypes
# Date: 08/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class DocumentArchetypeProxy: 


    # ----------------------------------------------------------------------
    # Method: load (static)
    # Description: It loads a PROTEUS document archetypes
    # Date: 08/10/2022
    # Version: 0.1
    # Author: Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    @staticmethod
    def load():
        document_archetypes = ArchetypeManager.load_document_archetypes()
        result: list = []
        for document_archetype in document_archetypes:
            archetype_proxy = DocumentArchetypeProxy(document_archetype)
            result.append(archetype_proxy)
        return result


    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a DocumentArchetypeProxy object.
    # Date       : 08/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def __init__(self, data :list):
        self.path : str = data["path"]
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.description : str = data["description"]
        self.author : str = data["author"]
        self.date : datetime = data["date"] 
        
    # ----------------------------------------------------------------------
    # Method     : get_project
    # Description: It returns an instance of a project.
    # Date       : 08/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def get_project(self, project: Project) -> Object:
        return Project(project, self.path)