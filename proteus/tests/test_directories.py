# ==========================================================================
# File: test_directories.py
# Description: pytest file for the PROTEUS application directories
# Date: 10/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
from pathlib import Path


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.app import ProteusApplication
from proteus.config import Config
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.archetype_proxys import ProjectArchetypeProxy
from proteus.model.project import Project

# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
app : Config = Config()

def test_application_directories():
    """
    It tests that essential PROTEUS directories exist.
    """
    assert app.resources_directory.is_dir()
    assert app.icons_directory.is_dir()
    assert app.archetypes_directory.is_dir()


def test_project_archetype_manager():

    # Get the number of projects in archetypes projects
    dir_path = str(app.archetypes_directory / "projects")
    number_of_projects = len(os.listdir(dir_path))
    
    # Check if load project function return all the projects
    projects = ArchetypeManager.load_project_archetypes()
    assert len(projects) == number_of_projects

    # Check if the project is a ProjectArchetypeProxy and has all the attributes
    for project_arch in projects:
        assert all(x for x in [type(project_arch) is ProjectArchetypeProxy, 
                               project_arch.path, project_arch.id, project_arch.name, project_arch.description,
                               project_arch.author, project_arch.date])
        
        # Check we can get an instance of the project.
        project = project_arch.get_project()
        assert type(project) is Project