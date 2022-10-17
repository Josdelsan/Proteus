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

import proteus
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

def test_properties():

    # Get the property and check it's value is not "media" because we will chage it into "media".
    old_enum_property : EnumProperty = test_project.get_property("stability")
    assert old_enum_property.value is not "media"
    
    # Set the property to "media" and check the property value has changed.
    test_project.set_property(EnumProperty(old_enum_property.name, "media", old_enum_property.get_choices_as_str()))
    new_enum_property : EnumProperty = test_project.get_property("stability")
    assert new_enum_property.value == "media"

    # For each document in the project
    for document in test_project.documents.values():
        # Get the property and check it's value is not "NewName" because we will chage it into "NewName".
        old_string_property: StringProperty = document.get_property("name")
        assert old_string_property.value is not "NewName"

        # Set the property to "media" and check the property value has changed.
        document.set_property(StringProperty(old_string_property.name, "NewName"))
        new_string_property: StringProperty = document.get_property("name")
        assert new_string_property.value == "NewName"

def test_properties_value_error():
    # Check if we set a wrong value that is not in the choices, the property selects a random choice.
    enum_prop: EnumProperty = test_project.get_property("stability")
    test_project.set_property(EnumProperty(enum_prop.name, "thisIsATest", enum_prop.get_choices_as_str()))
    new_enum_property: EnumProperty = test_project.get_property(enum_prop.name)
    assert ("thisIsATest" not in new_enum_property.get_choices_as_str()) and (new_enum_property.value in enum_prop.get_choices_as_str())

    # Check if we set a non valid date value if the property is set to date (actually today's date)
    date_prop: DateProperty = test_project.get_property("created")
    test_project.set_property(DateProperty(date_prop.name, "thisIsATest"))
    new_date_property: DateProperty = test_project.get_property(date_prop.name)
    assert (new_date_property.value == datetime.date.today())

    # Check if we set a non valid integer value if the property is set to int (actually 0)
    int_prop: IntegerProperty = test_project.get_property("numberOfUsers")
    test_project.set_property(IntegerProperty(int_prop.name, "thisIsATest"))
    new_int_property: IntegerProperty = test_project.get_property(int_prop.name)
    assert (new_int_property.value == 0)

    # Check if we set a non valid float value if the property is set to float (actually 0.0)
    float_prop: FloatProperty = test_project.get_property("money")
    test_project.set_property(FloatProperty(float_prop.name, "thisIsATest"))
    new_float_property: FloatProperty = test_project.get_property(float_prop.name)
    assert (new_float_property.value == 0.0)

    # Check if we set a non valid bool value if the property is set to bool (actually False)
    bool_prop: BooleanProperty = test_project.get_property("info")
    test_project.set_property(BooleanProperty(bool_prop.name, "thisIsATest"))
    new_bool_property: BooleanProperty = test_project.get_property(bool_prop.name)
    assert (new_bool_property.value == False)

    # Check if we set a non valid time value if the property is set to datetime (actually right now)
    time_prop: TimeProperty = test_project.get_property("time")
    test_project.set_property(TimeProperty(time_prop.name, "thisIsATest"))
    new_time_property: TimeProperty = test_project.get_property(time_prop.name)
    assert (new_time_property.value == datetime.datetime.now().time())