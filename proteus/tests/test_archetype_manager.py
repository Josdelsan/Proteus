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

import datetime
import enum
import os
from pathlib import Path


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.app import ProteusApplication
from proteus.config import Config
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.archetype_proxys import DocumentArchetypeProxy, ProjectArchetypeProxy
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.model.property import BooleanProperty, DateProperty, EnumProperty, FloatProperty, IntegerProperty, StringProperty, TimeProperty

# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
app : Config = Config()
test_project : Project = Project.load(app.base_directory / "tests" / "project")


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

        # Get each project folder and their files
        project_dir = os.path.dirname(project_arch.path)
        project_files = [file for file in os.listdir(project_dir)]

        # Check if the project has assets and objects
        assert  all(elem in project_files for elem in ["assets", "objects"])

        # Check if the project has at least one .xml file (the project file)
        assert len([x for x in project_files if x.endswith('.xml')]) >= 1
            
            
def test_document_archetype_manager():

    # Get the number of documents in archetypes documents
    dir_path = str(app.archetypes_directory / "documents")
    number_of_documents = len(os.listdir(dir_path))
    
    # Check if load document function return all the documents
    documents = ArchetypeManager.load_document_archetypes()
    assert len(documents) == number_of_documents

    # Check if the document is a DocumentArchetypeProxy and has all the attributes
    for document_arch in documents:
        assert all(x for x in [type(document_arch) is DocumentArchetypeProxy, 
                               document_arch.path, document_arch.id, document_arch.name, document_arch.description,
                               document_arch.author, document_arch.date])
        
        # Check we can get an instance of the document.
        document = document_arch.get_document(test_project)
        assert type(document) is Object

        # Get each document folder and their files
        document_dir = os.path.dirname(os.path.dirname(document_arch.path))
        document_files = [file for file in os.listdir(document_dir)]

        # Check if the document has assets and objects
        assert all(elem in document_files for elem in ["assets", "objects"])

        # Check if the document archetype has a document.xml file
        assert len([x for x in document_files if (x == "document.xml")]) == 1
