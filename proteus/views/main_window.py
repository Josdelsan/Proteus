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

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_menu import MainMenu
from proteus.views.components.document_list import DocumentList
from proteus.views.utils.decorators import component
from proteus.views.utils.event_manager import Event


# --------------------------------------------------------------------------
# Class: MainWindow
# Description: Main window for the PROTEUS application
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@component(QMainWindow, update_events=[Event.OPEN_PROJECT])
class MainWindow(QMainWindow):

    def create_component(self) -> None:
        # Set the window title
        self.setWindowTitle("Proteus application")

        # Set the window size
        self.resize(800, 600)

        # Create the main top menu
        mainmenu = MainMenu(self)
        self.setMenuBar(mainmenu)

        # Create document list menu
        self.document_list = DocumentList(self)
        self.setCentralWidget(self.document_list)

    def update_component(self) -> None:
        # Delete the existing document list widget
        if self.document_list is not None:
            self.document_list.setParent(None)

        # Create document list menu
        self.document_list = DocumentList(self)
        self.setCentralWidget(self.document_list)



