# ==========================================================================
# File: command_stack.py
# Description: Command stack to manage undo and redo operations.
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict, Union

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoStack

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

import proteus
from proteus.controller.commands.update_properties import UpdatePropertiesCommand
from proteus.services.project_service import ProjectService
from proteus.services.archetype_service import ArchetypeService
from proteus.views.utils.event_manager import EventManager, Event
from proteus.model.object import Object
from proteus.model.project import Project


# --------------------------------------------------------------------------
# Class: CommandStack
# Description: Command stack class to manage undo and redo operations.
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class Command():
    """
    Command class to manage backend operations in the PROTEUS presentation
    layer. It provides undo and redo operations if the command is undoable.
    Notifies the frontend components when the command is executed.
    """

    # Class attributes
    _stack : QUndoStack = None

    # ----------------------------------------------------------------------
    # Method     : get_instance
    # Description: Get the command stack instance
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def _get_instance(cls) -> QUndoStack:
        """
        Get the command stack instance, creating it if it does not exist.
        """
        if cls._stack is None:
            cls._stack = QUndoStack()
        return cls._stack
    
    # ----------------------------------------------------------------------
    # Method     : push
    # Description: Push a command to the command stack
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def _push(cls, command):
        """
        Push a command to the command stack.

        :param command: The command to push to the command stack.
        """
        cls._get_instance().push(command)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the last command
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def undo(cls):
        """
        Undo the last command. Only works if the command is undoable.
        """
        proteus.logger.info("Undoing last command")
        cls._get_instance().undo()

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the last command
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def redo(cls):
        """
        Redo the last command. Only works if the command is
        undoable/redoable.
        """
        proteus.logger.info("Redoing last command")
        cls._get_instance().redo()

    # ======================================================================
    # Project methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_properties
    # Description: Update the properties of an element given its id. It
    #              pushes the command to the command stack.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def update_properties(cls, element_id, new_properties):
        """
        Update the properties of an element given its id. It pushes the
        command to the command stack.

        Notify the frontend components when the command is executed passing
        the element_id as a parameter. MODIFY_OBJECT event is triggered.

        :param element_id: The id of the element to update its properties.
        :param new_properties: The new properties of the element.
        """
        # Push the command to the command stack
        proteus.logger.info(f"Updating properties of element with id: {element_id}")
        cls._push(UpdatePropertiesCommand(element_id, new_properties))

    # ----------------------------------------------------------------------
    # Method     : load_project
    # Description: Load a project from a given path.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def load_project(cls, project_path):
        """
        Load a project from a given path.

        Notify the frontend components when the command is executed. OPEN_PROJECT
        event is triggered.

        :param project_path: The path of the project to load.
        """
        proteus.logger.info(f"Loading project from path: {project_path}")
        ProjectService.load_project(project_path)
        EventManager().notify(event=Event.OPEN_PROJECT)

    # ----------------------------------------------------------------------
    # Method     : get_object_structure
    # Description: Get the structure of an object given its id.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_object_structure(cls, object_id) -> Dict[Object, List]:
        """
        Get the structure of an object given its id.
        """
        proteus.logger.info(f"Getting structure of object with id: {object_id}")
        return ProjectService.get_object_structure(object_id)
    
    # ----------------------------------------------------------------------
    # Method     : get_project_structure
    # Description: Get the structure of the current project.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_project_structure(cls) -> List[Object]:
        """
        Get the structure of the current project.
        """
        proteus.logger.info("Getting structure of current project")
        return ProjectService.get_project_structure()
    
    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: Save the current project state including all the children
    #              objects and documents.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def save_project(cls):
        """
        Save the current project state including all the children objects
        and documents.
        """
        proteus.logger.info("Saving current project")
        ProjectService.save_project()
        cls._get_instance().clear()
        EventManager().notify(event=Event.SAVE_PROJECT)
    
    # ----------------------------------------------------------------------
    # Method     : get_element
    # Description: Get the element given its id.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_element(cls, element_id) -> Union[Object, Project]:
        """
        Get the element given its id.
        """
        proteus.logger.info(f"Getting element with id: {element_id}")
        return ProjectService._get_element_by_id(element_id)
    
    # ======================================================================
    # Archetype methods
    # ======================================================================
    
    # ----------------------------------------------------------------------
    # Method     : create_project
    # Description: Create a new project with the given archetype id, name
    #              and path.
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def create_project(cls, archetype_id, name, path):
        """
        Create a new project with the given archetype id, name and path.

        :param archetype_id: The id of the archetype to create the project.
        :param name: The name of the project.
        :param path: The path of the project.
        """
        proteus.logger.info(f"Creating project with archetype id: {archetype_id}, name: {name} and path: {path}")
        ArchetypeService.create_project(archetype_id, name, path)
        project_path : str = f"{path}/{name}"
        cls.load_project(project_path)


    # ----------------------------------------------------------------------
    # Method     : get_project_archetypes
    # Description: Get project archetypes.
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_project_archetypes(cls) -> List[Project]:
        """
        Get project archetypes.
        """
        proteus.logger.info("Getting project archetypes")
        return ArchetypeService.get_project_archetypes()

    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes
    # Description: Get object archetypes.
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_object_archetypes(cls) -> Dict[str, List[Object]]:
        """
        Get object archetypes.
        """
        proteus.logger.info("Getting object archetypes")
        return ArchetypeService.get_object_archetypes()