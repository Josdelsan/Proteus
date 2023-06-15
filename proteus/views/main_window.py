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

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QMessageBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model import ProteusID
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.views.components.main_menu import MainMenu
from proteus.views.components.document_list import DocumentList
from proteus.views.utils.event_manager import Event, EventManager
from proteus.controller.command_stack import Controller


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
        self.setWindowTitle("Proteus application")

        # Set the window size
        self.resize(1200, 800)

        # Create archeype tab menu
        main_menu = MainMenu("Archetype menu", self)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, main_menu)

        # Create document list menu
        self.document_list = QWidget(self)
        self.setCentralWidget(self.document_list)

        # Create the status bar
        self.statusBar().showNormal()

        proteus.logger.info("Main window component created")

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
        if self.document_list is not None:
            self.document_list.setParent(None)

        # Create document list menu
        self.document_list = DocumentList(self)
        self.setCentralWidget(self.document_list)

        project = Controller.get_current_project()
        self.setWindowTitle(
            f"Proteus application - {project.get_property('name').value}"
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
        # Get the selected object
        selected_object: Object = Controller.get_selected_object()

        # Update the status bar
        object_name = selected_object.properties["name"].value
        self.statusBar().showMessage(
            f"Current selected object: {object_name} | Accepted archetypes by the object: {selected_object.acceptedChildren}"
        )

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
        project: Project = Controller.get_current_project()

        # Check if element id is project id
        if element_id == project.id:
            self.setWindowTitle(
                f"Proteus application - {project.get_property('name').value}"
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
    def closeEvent(self, event):
        """
        Handle the close event for the main window. Check if the project
        has unsaved changes and show a confirmation dialog to the user.
        """
        def close_without_saving():
            # Clean the command stack
            Controller._get_instance().clear()
            # Close the application
            event.accept()

        def close_with_saving():
            # Save the project
            Controller.save_project()
            # Close the application
            event.accept()

        # Check if the project has unsaved changes
        unsaved_changes: bool = not Controller._get_instance().isClean()

        if unsaved_changes:
            # Show a confirmation dialog
            confirmation_dialog = QMessageBox()
            confirmation_dialog.setIcon(QMessageBox.Icon.Warning)
            confirmation_dialog.setWindowTitle("Exit Proteus without saving")
            confirmation_dialog.setText(
                "Do you want to save changes before exiting Proteus?"
            )
            confirmation_dialog.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            confirmation_dialog.setDefaultButton(QMessageBox.StandardButton.No)
            confirmation_dialog.accepted.connect(close_with_saving)
            confirmation_dialog.rejected.connect(close_without_saving)
            confirmation_dialog.exec()