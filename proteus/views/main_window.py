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

from proteus.services.service_manager import ServiceManager
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

    def create_component(self):
        # Create an ArchetypeService instance
        self.service_manager = ServiceManager()

        # Set the window title
        self.setWindowTitle("Proteus application")

        # Create the main top menu
        mainmenu = MainMenu(self)
        self.setMenuBar(mainmenu)

        # Create document list menu
        document_list = DocumentList(self)
        self.setCentralWidget(document_list)

    def update_component(self):
        # TODO: Implement update on open project
        pass



