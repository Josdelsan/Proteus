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

from proteus.config import Config
from proteus.model import ProteusID
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.views import APP_ICON_TYPE
from proteus.views.components.main_menu import MainMenu
from proteus.views.components.project_container import ProjectContainer
from proteus.views.utils.event_manager import Event, EventManager
from proteus.views.utils.state_manager import StateManager
from proteus.views.utils.translator import Translator
from proteus.controller.command_stack import Controller

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: MainWindow
# Description: Main window class for the PROTEUS application.
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class MainWindow(QMainWindow):
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
        super().__init__(*args, **kwargs)
        # Create Controller instance
        self._controller: Controller = Controller()

        # Get the translator instance
        self.translator = Translator()

        # Create the configuration instance
        self.config = Config()

        # Create the component
        self.create_component()

        # Subscribe to events
        EventManager.attach(Event.OPEN_PROJECT, self.update_on_project_open, self)
        EventManager.attach(Event.SELECT_OBJECT, self.update_on_select_object, self)
        EventManager.attach(Event.MODIFY_OBJECT, self.update_on_modify_object, self)

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
        self.setWindowTitle(self.translator.text("main_window.title"))

        # Set the window icon
        proteus_icon: Path = self.config.get_icon(APP_ICON_TYPE, "proteus_icon")
        self.setWindowIcon(QIcon(proteus_icon.as_posix()))

        # Set the window size
        self.resize(1200, 800)

        # Create main menu
        main_menu = MainMenu(self, self._controller)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, main_menu)

        # Create document list menu
        self.project_container = QWidget(self)
        self.setCentralWidget(self.project_container)

        # Create the status bar
        self.statusBar().showNormal()

        log.info("Main window component created")

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_on_project_open
    # Description: Update the main window when a new project is opened.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_project_open(self, *args, **kwargs) -> None:
        """
        Update the main window when a new project is opened. It is used to
        load the document list menu and update the window title.

        Triggered by: Event.OPEN_PROJECT
        """
        # Delete the existing document list widget
        if self.project_container is not None:
            self.project_container.setParent(None)

        # Create document list menu
        self.project_container = ProjectContainer(self, self._controller)
        self.setCentralWidget(self.project_container)

        project = self._controller.get_current_project()
        self.setWindowTitle(
            f"{self.translator.text('main_window.title')} - {project.get_property('name').value}"
        )

    # ----------------------------------------------------------------------
    # Method     : update_on_select_object
    # Description: Update the status bar when a new object is selected.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_select_object(self, *args, **kwargs) -> None:
        """
        Update the status bar when a new object is selected. It is used to
        show information about the current selected object to the user.

        Triggered by: Event.SELECT_OBJECT
        """
        # NOTE: Adding a permanent message to the status bar is discouraged
        #       due to the fact that it is not possible to remove it just
        #       hide it using removeWidget() method.
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qstatusbar.html#qstatusbar-permanent-message

        # Get the selected object id
        selected_object_id: ProteusID = StateManager.get_current_object()

        # If there is no selected object, return
        if selected_object_id is None:
            return

        # Get the selected object and its name
        selected_object: Object = self._controller.get_element(selected_object_id)
        object_name = selected_object.properties["name"].value

        # Message to show in the status bar
        message: str = self.translator.text(
            "main_window.statusbar.text.selected_object",
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
    def update_on_modify_object(self, *args, **kwargs) -> None:
        """
        Update the window title when the project name is modified. Check if
        the modified object is the project and update the window title.

        Triggered by: Event.MODIFY_OBJECT
        """
        # Get element id
        element_id: ProteusID = kwargs["element_id"]

        # Check the element id is not None
        assert element_id is not None, "Element id is None on MODIFY_OBJECT event"

        # Get project
        project: Project = self._controller.get_current_project()

        # Check if element id is project id
        if element_id == project.id:
            self.setWindowTitle(
                f"{self.translator.text('main_window.title')} - {project.get_property('name').value}"
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
    def closeEvent(self, event):
        """
        Handle the close event for the main window. Check if the project
        has unsaved changes and show a confirmation dialog to the user.
        """

        def close_without_saving():
            # Clean the command stack
            self._controller.stack.clear()

            # Close the application
            event.accept()

        def close_with_saving():
            # Save the project
            self._controller.save_project()

            # Delete unused assets
            self._controller.delete_unused_assets()

            # Close the application
            event.accept()

        def cancel(*args, **kwargs):
            # Do nothing
            event.ignore()

        # Check if the project has unsaved changes
        unsaved_changes: bool = not self._controller.stack.isClean()

        if unsaved_changes:
            # Show a confirmation dialog
            confirmation_dialog = QMessageBox()
            confirmation_dialog.setIcon(QMessageBox.Icon.Warning)
            confirmation_dialog.setWindowTitle(
                self.translator.text("main_window.exit_dialog.title")
            )
            confirmation_dialog.setText(
                self.translator.text("main_window.exit_dialog.text")
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
