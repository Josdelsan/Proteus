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
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoStack, QUndoCommand
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

import proteus
from proteus.config import Config
from proteus.model import ProteusID
from proteus.controller.commands.update_properties import UpdatePropertiesCommand
from proteus.controller.commands.clone_archetype_object import (
    CloneArchetypeObjectCommand,
)
from proteus.controller.commands.clone_archetype_document import (
    CloneArchetypeDocumentCommand,
)
from proteus.controller.commands.clone_object import CloneObjectCommand
from proteus.controller.commands.delete_object import DeleteObjectCommand
from proteus.controller.commands.delete_document import DeleteDocumentCommand
from proteus.controller.commands.change_object_position import (
    ChangeObjectPositionCommand,
)
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

    # ======================================================================
    # Command stack methods
    # ======================================================================

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
        proteus.logger.info(
            f"Undoing last command [ {cls._get_instance().undoText()} ]"
        )
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
        proteus.logger.info(
            f"Redoing last command [ {cls._get_instance().redoText()} ]"
        )
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
        proteus.logger.info(
            f"Updating properties of element with id: {element_id}. New properties: {new_properties}"
        )
        cls._push(UpdatePropertiesCommand(element_id, new_properties))

    # ----------------------------------------------------------------------
    # Method     : clone_object
    # Description: Clone an object given its id. It pushes the command to
    #              the command stack.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def clone_object(cls, object_id: ProteusID) -> None:
        """
        Clone an object given its id. It pushes the command to the command
        stack.

        Notify the frontend components when the command is executed passing
        the object_id as a parameter. ADD_OBJECT event is triggered.

        :param object_id: The id of the object to clone.
        """
        # Check object_id is not None
        assert object_id is not None, "Object id can not be None"

        # Push the command to the command stack
        proteus.logger.info(f"Cloning object with id: {object_id}")
        cls._push(CloneObjectCommand(object_id))

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
    # Method     : change_object_position
    # Description: Change the position of an object given its id. It pushes
    #              the command to the command stack.
    # Date       : 13/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def change_object_position(
        cls, object_id: ProteusID, new_position: int, new_parent_id: ProteusID
    ) -> None:
        """
        Change the position of an object given its id. It pushes the command
        to the command stack. If position is None, the object is moved to the
        end of the parent.

        Notify the frontend components when the command is executed passing
        the object_id and object in DELETE_OBJECT and ADD_OBJECT events.

        :param object_id: The id of the object to change its position.
        :param new_position: The new position of the object.
        :param new_parent_id: The new parent of the object.
        """
        # Push the command to the command stack
        proteus.logger.info(
            f"Changing position of object with id: {object_id} to {new_position}"
        )
        cls._push(ChangeObjectPositionCommand(object_id, new_position, new_parent_id))

    # ----------------------------------------------------------------------
    # Method     : delete_document
    # Description: Delete a document given its id. It pushes the command to
    #              the command stack.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def delete_document(cls, document_id: ProteusID) -> None:
        """
        Delete a document given its id. It pushes the command to the command
        stack.

        Notify the frontend components when the command is executed passing
        the document_id as a parameter. DELETE_DOCUMENT event is triggered.

        :param document_id: The id of the document to delete.
        """
        # Push the command to the command stack
        proteus.logger.info(f"Deleting document with id: {document_id}")
        cls._push(DeleteDocumentCommand(document_id))

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

    # ======================================================================
    # Document views methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : get_document_default_view
    # Description: Get the xml of a document given its id.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_document_view(
        cls, document_id: ProteusID, xslt_name: str = "default"
    ) -> str:
        """
        Get the string representation of the document view given its id. The
        view is generated using the xslt file specified in the xslt_name. If
        the xslt_name is not specified, the default xslt is used.

        XSLT files are located in the xslt folder, defined in the config file.

        :param document_id: The id of the document to get the view.
        :param xslt_name: The name of the xslt file to use.
        """
        proteus.logger.info(f"Getting {xslt_name} view of document with id: {document_id}")

        # Get the xslt file path and check if it exists in the app config
        xslt_routes: Dict[str, Path] = Config().xslt_routes
        assert (
            xslt_name in xslt_routes
        ), f"XSLT file {xslt_name} not found in config file"
        XSL_TEMPLATE = Config().xslt_routes[xslt_name]

        # Get the document xml
        xml: ET.Element = ProjectService.generate_document_xml(document_id)

        # Create the transformer from the xsl file
        transform = ET.XSLT(ET.parse(XSL_TEMPLATE))
        result_tree: ET._XSLTResultTree = transform(xml)

        # Serialize the HTML root to a string
        html_string = ET.tostring(result_tree, encoding="unicode", pretty_print=True)

        return html_string
    
    # ----------------------------------------------------------------------
    # Method     : get_available_xslt
    # Description: Get the available xslt templates in the xslt folder.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_available_xslt(cls) -> List[str]:
        """
        Get the available xslt templates in the xslt folder.
        """
        xslt_routes: Dict[str, Path] = Config().xslt_routes
        return list(xslt_routes.keys())

    # ----------------------------------------------------------------------
    # Method     : get_project_templates
    # Description: Get the available project templates in the templates folder.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_project_templates(cls) -> List[str]:
        """
        Get the project templates in the proteus.xml project file. Note that
        templates that are not in the app installation are ignored and not
        saved when the project is saved.
        """
        project: Project = ProjectService.project
        return project.xsl_templates
    
    # ----------------------------------------------------------------------
    # Method     : add_project_template
    # Description: Add a new project template to the project.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def add_project_template(cls, template_name: str) -> None:
        """
        Add a new project template to the project.

        Triggers: Event.ADD_VIEW

        :param template_name: The name of the template to add.
        """
        proteus.logger.info(f"Adding '{template_name}' template to the project")

        ProjectService.add_project_template(template_name)

        # Trigger ADD_VIEW event notifying the new template
        EventManager.notify(Event.ADD_VIEW, xslt_name=template_name)

    # ----------------------------------------------------------------------
    # Method     : delete_project_template
    # Description: Delete a project template from the project.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def delete_project_template(cls, template_name: str) -> None:
        """
        Remove a project template from the project.

        Triggers: Event.DELETE_VIEW

        :param template_name: The name of the template to remove.
        """
        proteus.logger.info(f"Removing '{template_name}' template from the project")

        ProjectService.delete_project_template(template_name)

        # Trigger REMOVE_VIEW event
        EventManager.notify(Event.DELETE_VIEW, xslt_name=template_name)


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
    def create_object(cls, archetype_id: ProteusID, parent_id: ProteusID) -> None:
        """
        Create a new object with the given archetype id and parent id.

        :param archetype_id: The id of the archetype to create the object.
        """
        proteus.logger.info(
            f"Creating object from archetype: {archetype_id} and parent id: {parent_id}"
        )
        cls._push(CloneArchetypeObjectCommand(archetype_id, parent_id))

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
