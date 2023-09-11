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
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoStack, QUndoCommand
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

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
from proteus.services.render_service import RenderService
from proteus.views.utils.event_manager import EventManager, Event
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.model.properties import Property

# logging configuration
log = logging.getLogger(__name__)


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

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Initialize the Controller object.
    # Date       : 07/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        project_service: ProjectService = None,
        archetype_service: ArchetypeService = None,
        render_service: RenderService = None,
    ) -> None:
        """
        Initialize the Controller object.
        """
        # Dependency injection ------------------
        if project_service is None:
            project_service = ProjectService()
        if archetype_service is None:
            archetype_service = ArchetypeService()
        if render_service is None:
            render_service = RenderService()

        # Set the services
        self._project_service = project_service
        self._archetype_service = archetype_service
        self._render_service = render_service

        # Command stack ------------------------
        self.stack: QUndoStack = QUndoStack()

        # Connect the signals to the event manager to notify the frontend
        self.stack.canRedoChanged.connect(
            lambda: EventManager().notify(event=Event.STACK_CHANGED)
        )
        self.stack.canUndoChanged.connect(
            lambda: EventManager().notify(event=Event.STACK_CHANGED)
        )
        self.stack.cleanChanged.connect(
            lambda: EventManager().notify(event=Event.STACK_CHANGED)
        )

    # ======================================================================
    # Command stack methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : push
    # Description: Push a command to the command stack
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _push(self, command: QUndoCommand) -> None:
        """
        Push a command to the command stack.

        :param command: The command to push to the command stack.
        """
        self.stack.push(command)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the last command
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self) -> None:
        """
        Undo the last command. Only works if the command is undoable.
        """
        log.info(f"Undoing last command [ {self.stack.undoText()} ]")
        self.stack.undo()

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the last command
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self) -> None:
        """
        Redo the last command. Only works if the command is
        undoable/redoable.
        """
        log.info(f"Redoing last command [ {self.stack.redoText()} ]")
        self.stack.redo()

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
    def update_properties(
        self, element_id: ProteusID, new_properties: List[Property]
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
        log.info(
            f"Updating properties of element with id: {element_id}. New properties: {new_properties}"
        )
        self._push(
            UpdatePropertiesCommand(
                element_id=element_id,
                new_properties=new_properties,
                project_service=self._project_service,
            )
        )

    # ----------------------------------------------------------------------
    # Method     : clone_object
    # Description: Clone an object given its id. It pushes the command to
    #              the command stack.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def clone_object(self, object_id: ProteusID) -> None:
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
        log.info(f"Cloning object with id: {object_id}")
        self._push(
            CloneObjectCommand(
                object_id=object_id, project_service=self._project_service
            )
        )

    # ----------------------------------------------------------------------
    # Method     : delete_object
    # Description: Delete an object given its id. It pushes the command to
    #              the command stack.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_object(self, object_id: ProteusID) -> None:
        """
        Delete an object given its id. It pushes the command to the command
        stack.

        Notify the frontend components when the command is executed passing
        the object_id as a parameter. DELETE_OBJECT event is triggered.

        :param object_id: The id of the object to delete.
        """
        # Push the command to the command stack
        log.info(f"Deleting object with id: {object_id}")
        self._push(
            DeleteObjectCommand(
                object_id=object_id, project_service=self._project_service
            )
        )

    # ----------------------------------------------------------------------
    # Method     : change_object_position
    # Description: Change the position of an object given its id. It pushes
    #              the command to the command stack.
    # Date       : 13/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def change_object_position(
        self, object_id: ProteusID, new_position: int, new_parent_id: ProteusID
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
        # Check the object is accepted by the parent
        parent: Union[Project, Object] = self._project_service._get_element_by_id(
            new_parent_id
        )

        # Get the object
        object: Object = self._project_service._get_element_by_id(object_id)

        # Check the object is accepted by the parent
        assert parent.accept_descendant(
            object
        ), f"Object {object_id} is not accepted by parent {new_parent_id}"

        # Push the command to the command stack
        log.info(f"Changing position of object with id: {object_id} to {new_position}")
        self._push(
            ChangeObjectPositionCommand(
                object_id=object_id,
                new_position=new_position,
                new_parent_id=new_parent_id,
                project_service=self._project_service,
            )
        )

    # ----------------------------------------------------------------------
    # Method     : change_document_position
    # Description: Change the position of a document given its id. It pushes
    #              the command to the command stack.
    # Date       : 09/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    # NOTE: This action is not undoable. This decision was made because of
    # the behaviour of tabMoved signal of QTabBar, which while moving tabs
    # instead of emitting the signal once is dropped. In projects with multiple
    # documents this might cause a lot of undo commands to be pushed to the
    # command stack obfuscating the undo/redo history.
    def change_document_position(
        self, document_id: ProteusID, new_position: int
    ) -> None:
        """
        Change the position of a document given its id. It pushes the command
        to the command stack. If position is None, the document is moved to the
        end of the project.
        """
        assert document_id is not None, "Document id can not be None"

        # Get the document
        document: Object = self._project_service._get_element_by_id(document_id)

        # Check the document is accepted by the project
        assert self._project_service.project.accept_descendant(
            document
        ), f"Object {document_id} is not accepted by project. Object classes: {document.classes}"

        # Push the command to the command stack
        log.info(
            f"Changing position of document with id: {document_id} to {new_position}"
        )
        # Call ProjectService method
        self._project_service.change_object_position(
            document.id, new_position, self._project_service.project
        )

        # Notify that this action requires saving even if the command is not
        # undoable
        EventManager.notify(Event.REQUIRED_SAVE_ACTION)

    # ----------------------------------------------------------------------
    # Method     : delete_document
    # Description: Delete a document given its id. It pushes the command to
    #              the command stack.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_document(self, document_id: ProteusID) -> None:
        """
        Delete a document given its id. It pushes the command to the command
        stack.

        Notify the frontend components when the command is executed passing
        the document_id as a parameter. DELETE_DOCUMENT event is triggered.

        :param document_id: The id of the document to delete.
        """
        # Push the command to the command stack
        log.info(f"Deleting document with id: {document_id}")
        self._push(
            DeleteDocumentCommand(
                document_id=document_id, project_service=self._project_service
            )
        )

    # ----------------------------------------------------------------------
    # Method     : load_project
    # Description: Load a project from a given path.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def load_project(self, project_path: str) -> None:
        """
        Load a project from a given path.

        Notify the frontend components when the command is executed. OPEN_PROJECT
        event is triggered.

        :param project_path: The path of the project to load.
        """
        log.info(f"Loading project from path: {project_path}")
        self._project_service.load_project(project_path)
        EventManager().notify(event=Event.OPEN_PROJECT)

    # ----------------------------------------------------------------------
    # Method     : get_object_structure
    # Description: Get the structure of an object given its id.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_object_structure(self, object_id: ProteusID) -> Dict[Object, List]:
        """
        Get the structure of an object given its id.
        """
        log.info(f"Getting structure of object with id: {object_id}")
        return self._project_service.get_object_structure(object_id)

    # ----------------------------------------------------------------------
    # Method     : get_project_structure
    # Description: Get the structure of the current project.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_project_structure(self) -> List[Object]:
        """
        Get the structure of the current project.
        """
        log.info("Getting structure of current project")
        return self._project_service.get_project_structure()

    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: Save the current project state including all the children
    #              objects and documents.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_project(self) -> None:
        """
        Save the current project state including all the children objects
        and documents.
        """
        log.info("Saving current project")
        self._project_service.save_project()
        self.stack.clear()
        EventManager().notify(event=Event.SAVE_PROJECT)

    # ----------------------------------------------------------------------
    # Method     : get_element
    # Description: Get the element given its id.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_element(self, element_id: ProteusID) -> Union[Object, Project]:
        """
        Get the element given its id.
        """
        return self._project_service._get_element_by_id(element_id)

    # ----------------------------------------------------------------------
    # Method     : get_current_project_id
    # Description: Get the id of the current project.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_current_project(self) -> Project:
        """
        Get the id of the current project.
        """
        current_project: Project = self._project_service.project

        assert current_project is not None, "Project is not loaded"

        return self._project_service.project

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
    def get_document_view(
        self, document_id: ProteusID, xslt_name: str = "default"
    ) -> str:
        """
        Get the string representation of the document view given its id. The
        view is generated using the xslt file specified in the xslt_name. If
        the xslt_name is not specified, the default xslt is used.

        XSLT files are located in the xslt folder, defined in the config file.

        :param document_id: The id of the document to get the view.
        :param xslt_name: The name of the xslt file to use.
        """
        log.info(f"Getting {xslt_name} view of document with id: {document_id}")

        # Get the document xml
        xml: ET.Element = self._project_service.generate_document_xml(document_id)

        html_string: str = self._render_service.render(xml, xslt_name)

        return html_string

    # ----------------------------------------------------------------------
    # Method     : get_available_xslt
    # Description: Get the available xslt templates in the xslt folder.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_available_xslt(self) -> List[str]:
        """
        Get the available xslt templates in the xslt folder.
        """
        return self._render_service.get_available_xslt()

    # ----------------------------------------------------------------------
    # Method     : get_project_templates
    # Description: Get the available project templates in the templates folder.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_project_templates(self) -> List[str]:
        """
        Get the project templates in the proteus.xml project file. Note that
        templates that are not in the app installation are ignored and not
        saved when the project is saved.
        """
        project: Project = self._project_service.project
        return project.xsl_templates

    # ----------------------------------------------------------------------
    # Method     : add_project_template
    # Description: Add a new project template to the project.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_project_template(self, template_name: str) -> None:
        """
        Add a new project template to the project.

        Triggers: Event.ADD_VIEW

        :param template_name: The name of the template to add.
        """
        log.info(f"Adding '{template_name}' template to the project")

        self._project_service.add_project_template(template_name)

        # Trigger ADD_VIEW event notifying the new template
        EventManager.notify(Event.ADD_VIEW, xslt_name=template_name)

        # Notify that this action requires saving even if the command is not
        # undoable
        EventManager.notify(Event.REQUIRED_SAVE_ACTION)

    # ----------------------------------------------------------------------
    # Method     : delete_project_template
    # Description: Delete a project template from the project.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_project_template(self, template_name: str) -> None:
        """
        Remove a project template from the project.

        Triggers: Event.DELETE_VIEW

        :param template_name: The name of the template to remove.
        """
        log.info(f"Removing '{template_name}' template from the project")

        self._project_service.delete_project_template(template_name)

        # Trigger REMOVE_VIEW event
        EventManager.notify(Event.DELETE_VIEW, xslt_name=template_name)

        # Notify that this action requires saving even if the command is not
        # undoable
        EventManager.notify(Event.REQUIRED_SAVE_ACTION)

    # ----------------------------------------------------------------------
    # Method     : delete_unused_assets
    # Description: Delete the assets that are not used in the project.
    # Date       : 12/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_unused_assets(self) -> None:
        """
        Delete the assets that are not used in the project.

        This operation may be performed when the project is saved or close.
        It can be costly in terms of performance due to the way fileProperties
        are accessed in the objects.
        """
        log.info("Deleting unused assets from the project")

        self._project_service.delete_unused_assets()

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
    def create_project(self, archetype_id, name, path) -> None:
        """
        Create a new project with the given archetype id, name and path.

        :param archetype_id: The id of the archetype to create the project.
        :param name: The name of the project.
        :param path: The path of the project.
        """
        log.info(
            f"Creating project with archetype id: {archetype_id}, name: {name} and path: {path}"
        )
        self._archetype_service.create_project(archetype_id, name, path)
        project_path: str = f"{path}/{name}"
        self.load_project(project_path)

    # ----------------------------------------------------------------------
    # Method     : create_object
    # Description: Create a new object with the given archetype id
    #              and parent id.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_object(self, archetype_id: ProteusID, parent_id: ProteusID) -> None:
        """
        Create a new object with the given archetype id and parent id.

        :param archetype_id: The id of the archetype to create the object.
        """
        log.info(
            f"Creating object from archetype: {archetype_id} and parent id: {parent_id}"
        )
        self._push(
            CloneArchetypeObjectCommand(
                archetype_id=archetype_id,
                parent_id=parent_id,
                project_service=self._project_service,
                archetype_service=self._archetype_service,
            )
        )

    # ----------------------------------------------------------------------
    # Method     : create_document
    # Description: Create a new document with the given archetype id
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_document(self, archetype_id: ProteusID) -> None:
        """
        Create a new document with the given archetype id.

        :param archetype_id: The id of the archetype to create the document.
        """
        log.info(f"Creating document from archetype: {archetype_id}")
        self._push(
            CloneArchetypeDocumentCommand(
                archetype_id=archetype_id,
                project_service=self._project_service,
                archetype_service=self._archetype_service,
            )
        )

    # ----------------------------------------------------------------------
    # Method     : get_project_archetypes
    # Description: Get project archetypes.
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_project_archetypes(self) -> List[Project]:
        """
        Get project archetypes.
        """
        log.info("Getting project archetypes")
        return self._archetype_service.get_project_archetypes()

    # ----------------------------------------------------------------------
    # Method     : get_object_archetypes
    # Description: Get object archetypes.
    # Date       : 31/08/2023
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_first_level_object_archetypes(self) -> Dict[str, Dict[str, List[Object]]]:
        """
        Get object archetypes.
        """
        log.info("Getting first level object archetypes")
        return self._archetype_service.get_first_level_object_archetypes()

    # ----------------------------------------------------------------------
    # Method     : get_accepted_object_archetypes
    # Description: Get object archetypes accepted by the parent.
    # Date       : 31/08/2023
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_accepted_object_archetypes(
        self, parent_id: ProteusID
    ) -> Dict[str, List[Object]]:
        """
        Get object archetypes accepted by the parent. It return second level
        archetypes grouped by object class.
        """
        log.info(
            f"Getting second level object archetypes accepted by parent: {parent_id}"
        )
        parent: Object = self._project_service._get_element_by_id(parent_id)
        return self._archetype_service.get_accepted_object_archetypes(parent)

    # ----------------------------------------------------------------------
    # Method     : get_document_archetypes
    # Description: Get document archetypes.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_document_archetypes(self) -> List[Object]:
        """
        Get document archetypes.
        """
        log.info("Getting document archetypes")
        return self._archetype_service.get_document_archetypes()

    # ----------------------------------------------------------------------
    # Method     : get_archetype_by_id
    # Description: Get archetype by id.
    # Date       : 02/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_archetype_by_id(self, archetype_id) -> Union[Object, Project]:
        """
        Get archetype by id.
        """
        return self._archetype_service._get_archetype_by_id(archetype_id)
