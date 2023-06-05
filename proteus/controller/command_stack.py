# ==========================================================================
# File: command_stack.py
# Description: Controller stack to manage undo and redo operations.
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

from PyQt6.QtGui import QUndoStack, QUndoCommand
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

import proteus
from proteus.model import ProteusID
from proteus.controller.commands.update_properties import UpdatePropertiesCommand
from proteus.controller.commands.clone_archetype_object import (
    CloneArchetypeObjectCommand,
)
from proteus.controller.commands.clone_archetype_document import (
    CloneArchetypeDocumentCommand,
)
from proteus.controller.commands.delete_object import DeleteObjectCommand
from proteus.services.project_service import ProjectService
from proteus.services.archetype_service import ArchetypeService
from proteus.views.utils.event_manager import EventManager, Event
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.model.properties import Property


# --------------------------------------------------------------------------
# Class: CommandStack
# Description: Controller stack class to manage undo and redo operations.
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class Controller:
    """
    Controller class to manage backend operations in the PROTEUS presentation
    layer. It provides undo and redo operations if the command is undoable.
    Notifies the frontend components when the command is executed.
    """

    # Class attributes
    _stack: QUndoStack = None
    _last_selected_item: ProteusID = None

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
            # Create the command stack
            cls._stack = QUndoStack()

            # Connect the signals to the event manager to notify the frontend
            cls._stack.canRedoChanged.connect(
                lambda: EventManager().notify(event=Event.STACK_CHANGED)
            )
            cls._stack.canUndoChanged.connect(
                lambda: EventManager().notify(event=Event.STACK_CHANGED)
            )
            cls._stack.cleanChanged.connect(
                lambda: EventManager().notify(event=Event.STACK_CHANGED)
            )
        return cls._stack

    # ----------------------------------------------------------------------
    # Method     : push
    # Description: Push a command to the command stack
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def _push(cls, command: QUndoCommand) -> None:
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
    def undo(cls) -> None:
        """
        Undo the last command. Only works if the command is undoable.
        """
        proteus.logger.info(f"Undoing last command: {cls._get_instance().undoText()}")
        cls._get_instance().undo()

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the last command
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def redo(cls) -> None:
        """
        Redo the last command. Only works if the command is
        undoable/redoable.
        """
        proteus.logger.info(f"Redoing last command: {cls._get_instance().redoText()}")
        cls._get_instance().redo()

    # ----------------------------------------------------------------------
    # Method     : select_object
    # Description: Store last selected object id by the user.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def select_object(cls, object_id: ProteusID) -> None:
        """
        Store last selected object id by the user.

        :param object_id: The id of the object selected by the user.
        """
        # Deselect the last selected object if it exists
        if cls._last_selected_item is not None:
            cls.deselect_object()
        
        # Select the new object
        cls._last_selected_item: ProteusID = object_id
        EventManager().notify(event=Event.SELECT_OBJECT)

    # ----------------------------------------------------------------------
    # Method     : deselect_object
    # Description: Deselect the last selected object id by the user.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def deselect_object(cls) -> None:
        """
        Deselect the last selected object id by the user.
        """
        deselected_object_id = cls._last_selected_item
        cls._last_selected_item: ProteusID = None
        EventManager().notify(event=Event.DESELECT_OBJECT, element_id=deselected_object_id)

    # ----------------------------------------------------------------------
    # Method     : get_selected_object
    # Description: Get last selected object id by the user.
    # Date       : 02/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_selected_object_id(cls) -> ProteusID:
        """
        Get last selected object id by the user.
        """
        assert cls._last_selected_item is not None, "No object selected"

        return cls._last_selected_item

    # ----------------------------------------------------------------------
    # Method     : get_selected_object
    # Description: Get last selected object by the user.
    # Date       : 02/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_selected_object(cls) -> Object:
        """
        Get last selected object by the user.
        """
        return ProjectService._get_element_by_id(cls.get_selected_object_id())

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
    def update_properties(
        cls, element_id: ProteusID, new_properties: List[Property]
    ) -> None:
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
    # Method     : delete_object
    # Description: Delete an object given its id. It pushes the command to
    #              the command stack.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def delete_object(cls, object_id: ProteusID) -> None:
        """
        Delete an object given its id. It pushes the command to the command
        stack.

        Notify the frontend components when the command is executed passing
        the object_id as a parameter. DELETE_OBJECT event is triggered.

        :param object_id: The id of the object to delete.
        """
        # Push the command to the command stack
        proteus.logger.info(f"Deleting object with id: {object_id}")
        cls._push(DeleteObjectCommand(object_id))

    # ----------------------------------------------------------------------
    # Method     : load_project
    # Description: Load a project from a given path.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def load_project(cls, project_path: str) -> None:
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
    def get_object_structure(cls, object_id: ProteusID) -> Dict[Object, List]:
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
    def save_project(cls) -> None:
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
    def get_element(cls, element_id: ProteusID) -> Union[Object, Project]:
        """
        Get the element given its id.
        """
        return ProjectService._get_element_by_id(element_id)

    # ----------------------------------------------------------------------
    # Method     : get_current_project_id
    # Description: Get the id of the current project.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_current_project(cls) -> Project:
        """
        Get the id of the current project.
        """
        current_project: Project = ProjectService.project

        assert current_project is not None, "Project is not loaded"

        return ProjectService.project

    # ----------------------------------------------------------------------
    # Method     : get_document_xml
    # Description: Get the xml of a document given its id.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_document_xml(cls, document_id: ProteusID) -> str:
        """
        Get the xml of a document given its id.
        """
        proteus.logger.info(f"Getting xml of document with id: {document_id}")
        document_xml: ET.Element = ProjectService.generate_document_xml(document_id)
        return ET.tostring(
            document_xml, xml_declaration=True, encoding="utf-8", pretty_print=True
        ).decode()

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
    def create_project(cls, archetype_id, name, path) -> None:
        """
        Create a new project with the given archetype id, name and path.

        :param archetype_id: The id of the archetype to create the project.
        :param name: The name of the project.
        :param path: The path of the project.
        """
        proteus.logger.info(
            f"Creating project with archetype id: {archetype_id}, name: {name} and path: {path}"
        )
        ArchetypeService.create_project(archetype_id, name, path)
        project_path: str = f"{path}/{name}"
        cls.load_project(project_path)

    # ----------------------------------------------------------------------
    # Method     : create_object
    # Description: Create a new object with the given archetype id
    #              and parent id.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def create_object(cls, archetype_id) -> None:
        """
        Create a new object with the given archetype id and parent id.

        :param archetype_id: The id of the archetype to create the object.
        """
        proteus.logger.info(
            f"Creating object from archetype: {archetype_id} and parent id: {cls.get_selected_object_id()}"
        )
        cls._push(
            CloneArchetypeObjectCommand(archetype_id, cls.get_selected_object_id())
        )

    # ----------------------------------------------------------------------
    # Method     : create_document
    # Description: Create a new document with the given archetype id
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def create_document(cls, archetype_id: ProteusID) -> None:
        """
        Create a new document with the given archetype id.

        :param archetype_id: The id of the archetype to create the document.
        """
        proteus.logger.info(f"Creating document from archetype: {archetype_id}")
        cls._push(CloneArchetypeDocumentCommand(archetype_id))

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

    # ----------------------------------------------------------------------
    # Method     : get_document_archetypes
    # Description: Get document archetypes.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_document_archetypes(cls) -> List[Object]:
        """
        Get document archetypes.
        """
        proteus.logger.info("Getting document archetypes")
        return ArchetypeService.get_document_archetypes()

    # ----------------------------------------------------------------------
    # Method     : get_archetype_by_id
    # Description: Get archetype by id.
    # Date       : 02/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_archetype_by_id(cls, archetype_id) -> Union[Object, Project]:
        """
        Get archetype by id.
        """
        return ArchetypeService._get_archetype_by_id(archetype_id)
