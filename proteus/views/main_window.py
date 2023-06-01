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

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_menu import MainMenu
from proteus.views.components.document_list import DocumentList
from proteus.views.utils.decorators import subscribe_to
from proteus.views.utils.event_manager import Event


# --------------------------------------------------------------------------
# Class: MainWindow
# Description: Main window class for the PROTEUS application.
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@subscribe_to(update_events=[Event.OPEN_PROJECT])
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
        Class constructor, invoke the parents class constructors and create
        the component.
        """
        super().__init__(*args, **kwargs)

        # Create the component
        self.create_component()

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
        self.resize(800, 600)

        # Create archeype tab menu
        main_menu = MainMenu("Archetype menu", self)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea,main_menu)

        # Create document list menu
        self.document_list = DocumentList(self)
        self.setCentralWidget(self.document_list)

        # Create the status bar
        self.statusBar().showNormal()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the main menu for the PROTEUS application
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self, *args, **kwargs) -> None:
        """
        Update the main window when a new project is opened.
        """
        # TODO: Check for unsaved changes

        # Delete the existing document list widget
        if self.document_list is not None:
            self.document_list.setParent(None)

        # Create document list menu
        self.document_list = DocumentList(self)
        self.setCentralWidget(self.document_list)
