# ==========================================================================
# File: main_window.py
# Description: PyQT6 main view for the PROTEUS application
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QMessageBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.utils import ProteusIconType
from proteus.views.components.abstract_component import ProteusComponent
from proteus.views.components.main_menu import MainMenu
from proteus.views.components.project_container import ProjectContainer
from proteus.utils.events import SelectObjectEvent, OpenProjectEvent, ModifyObjectEvent
from proteus.utils.state_restorer import write_state_to_file

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: MainWindow
# Description: Main window class for the PROTEUS application.
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class MainWindow(QMainWindow, ProteusComponent):
    """
    Main window for the PROTEUS application. It is used to display the main
    menu and the documents tab menu. Update the main window when a new
    project is opened.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the main window.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.
        """
        super(MainWindow, self).__init__(*args, **kwargs)

        # Variables
        self.main_menu: MainMenu = None
        self.project_container: ProjectContainer = None

        # Create the component
        self.create_component()

        # Subscribe to events
        self.subscribe()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the main window for the PROTEUS application.
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the main window for the PROTEUS application.
        """
        # Set the window title
        self.setWindowTitle(self._translator.text("main_window.title"))

        # Set the window icon
        proteus_icon: Path = self._config.get_icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(QIcon(proteus_icon.as_posix()))

        # Set the window size
        self.resize(1200, 800)

        # Create main menu
        self.main_menu = MainMenu(parent=self)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.main_menu)

        # Create document list menu
        self.project_container = QWidget(self)
        self.setCentralWidget(self.project_container)

        # Create the status bar
        self.statusBar().showNormal()

        log.info("Main window component created")

    # ---------------------------------------------------------------------
    # Method     : subscribe
    # Description: Subscribe the component to the events.
    # Date       : 15/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def subscribe(self) -> None:
        """
        Subscribe the component to the events.

        MainMenu component subscribes to the following events:
            - OPEN PROJECT -> update_on_open_project
            - SELECT OBJECT -> update_on_select_object
            - MODIFY OBJECT -> update_on_modify_object
        """

        OpenProjectEvent().connect(self.update_on_open_project)
        SelectObjectEvent().connect(self.update_on_select_object)
        ModifyObjectEvent().connect(self.update_on_modify_object)

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_on_open_project
    # Description: Update the main window when a new project is opened.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_open_project(self) -> None:
        """
        Update the main window when a new project is opened. It is used to
        load the document list menu and update the window title.

        Triggered by: OpenProjectEvent
        """
        # Delete the existing widget or container
        if self.project_container.__class__ == QWidget:
            self.project_container.setParent(None)
        elif self.project_container.__class__ == ProjectContainer:
            self.project_container.delete_component()

        # Create document list menu
        self.project_container = ProjectContainer(self)
        self.setCentralWidget(self.project_container)

        project = self._controller.get_current_project()
        self.setWindowTitle(
            f"{self._translator.text('main_window.title')} - {project.get_property(PROTEUS_NAME).value}"
        )

    # ----------------------------------------------------------------------
    # Method     : update_on_select_object
    # Description: Update the status bar when a new object is selected.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_select_object(
        self, selected_object_id: ProteusID, document_id: ProteusID
    ) -> None:
        """
        Update the status bar when a new object is selected. It is used to
        show information about the current selected object to the user.

        Triggered by: SelectObjectEvent

        :param selected_object_id: Id of the selected object
        :param document_id: Id of the document where the object is located
        """
        # NOTE: Adding a permanent message to the status bar is discouraged
        #       due to the fact that it is not possible to remove it just
        #       hide it using removeWidget() method.
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qstatusbar.html#qstatusbar-permanent-message

        # If there is no selected object, return
        if selected_object_id is None or selected_object_id == "":
            return

        assert (
            document_id is not None or document_id != ""
        ), "Document id is None on SELECT OBJECT event"

        # If the selected object is not in the current document, return
        if document_id != self._state_manager.get_current_document():
            return

        # Get the selected object and its name
        selected_object: Object = self._controller.get_element(selected_object_id)
        object_name = selected_object.get_property(PROTEUS_NAME).value

        # Message to show in the status bar
        message: str = self._translator.text(
            "main_window.statusbar.text.selected_object",
            selected_object_id,
            object_name,
            selected_object.acceptedChildren,
        )

        # Update the status bar with the temporary message
        self.statusBar().showMessage(message)

    # ----------------------------------------------------------------------
    # Method     : update_on_modify_object
    # Description: Update the window title when the project name is modified.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_modify_object(self, object_id: ProteusID) -> None:
        """
        Update the window title when the project name is modified. Check if
        the modified object is the project and update the window title.

        Triggered by: ModifyObjectEvent

        :param object_id: Id of the modified object
        """
        # Check the element id is not None
        assert object_id is not None, "Object id is None on MODIFY_OBJECT event"

        # Get project
        project: Project = self._controller.get_current_project()

        # Check if element id is project id
        if object_id == project.id:
            self.setWindowTitle(
                f"{self._translator.text('main_window.title')} - {project.get_property(PROTEUS_NAME).value}"
            )

    # ======================================================================
    # Component slots methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : closeEvent
    # Description: Handle the close event for the main window.
    # Date       : 15/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    # NOTE: This method overrides the default closeEvent method for the
    #       QMainWindow class. Close window dialog may be moved to its
    #       own class in the dialog package but closeEvent method must
    #       be overriden anyway.
    def closeEvent(self, event) -> None:
        """
        Handle the close event for the main window. Check if the project
        has unsaved changes and show a confirmation dialog to the user.

        Write the state to a file inside project folder if the user saves
        the project or close the application and no changes are discarded.

        :param event: Close event
        """

        def close_without_saving():
            # Clean the command stack
            self._controller.stack.clear()

            if not unsaved_changes:
                # Write the state to a file if there is a project opened
                if self._controller.get_current_project() is not None:
                    project_path: str = self._controller.get_current_project().path
                    write_state_to_file(Path(project_path).parent, self._state_manager)
            # Close the application
            event.accept()

        def close_with_saving():
            # Save the project
            self._controller.save_project()

            # Write the state to a file
            project_path: str = self._controller.get_current_project().path
            write_state_to_file(Path(project_path).parent, self._state_manager)

            # Close the application
            event.accept()

        def cancel(*args, **kwargs):
            # Do nothing
            event.ignore()

        # Check if the project has unsaved changes
        unsaved_changes: bool = self._controller.check_unsaved_changes()

        if unsaved_changes:
            # Show a confirmation dialog
            confirmation_dialog = QMessageBox()
            confirmation_dialog.setIcon(QMessageBox.Icon.Warning)
            confirmation_dialog.setWindowTitle(
                self._translator.text("main_window.exit_dialog.title")
            )
            confirmation_dialog.setText(
                self._translator.text("main_window.exit_dialog.text")
            )
            confirmation_dialog.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            confirmation_dialog.setDefaultButton(QMessageBox.StandardButton.No)
            confirmation_dialog.accepted.connect(close_with_saving)
            confirmation_dialog.rejected.connect(close_without_saving)
            confirmation_dialog.closeEvent = cancel
            confirmation_dialog.exec()
        else:
            close_without_saving()
