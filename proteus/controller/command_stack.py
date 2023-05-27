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

from proteus.controller.commands.update_properties import UpdatePropertiesCommand
from proteus.services.project_service import ProjectService
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
        cls._get_instance().redo()


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
        # Get the old properties before updating the properties
        old_properties_dict = ProjectService.get_properties(element_id)
        old_properties = [old_properties_dict[prop.name] for prop in new_properties]

        # Push the command to the command stack
        cls._push(UpdatePropertiesCommand(element_id, old_properties, new_properties))

        # Notify the frontend components
        EventManager().notify(Event.MODIFY_OBJECT, element_id=element_id)

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
        ProjectService.load_project(project_path)
        EventManager().notify(Event.OPEN_PROJECT)

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
        return ProjectService.get_project_structure()
    
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
        return ProjectService._get_element_by_id(element_id)