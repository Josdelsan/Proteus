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

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QSizePolicy, QSplitter

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.services.service_manager import ServiceManager
from proteus.views.components.menu_bar import MenuBar
from proteus.views.components.structure_menu import StructureMenu


# --------------------------------------------------------------------------
# Class: MainWindow
# Description: Main window for the PROTEUS application
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create an ArchetypeService instance
        self.service_manager = ServiceManager()

        # Set the window title
        self.setWindowTitle("Proteus application")

        # Create the menu bar
        menubar = MenuBar(self, self.service_manager)
        self.setMenuBar(menubar)

        # Create structure menu
        structure_menu = StructureMenu(self, self.service_manager)

        # Create the main container layout
        self.create_main_layout(structure_menu)

        # Get project archetypes
        """ archetypes = self.archetype_service.get_project_archetypes()
        for project_arch in archetypes:
            label =QLabel(f"{project_arch.id} \n \t {project_arch.documents.keys()} \n")
            layout.addWidget(label) """

    def create_main_layout(self, structure_menu: QWidget):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Splitter
        splitter = QSplitter()
        splitter.setStyleSheet("QSplitter::handle { background-color: #666666; }")

        # Structure container
        structure_menu.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        splitter.addWidget(structure_menu)

        container2 = QWidget()
        container2.setStyleSheet("background-color: #FFFFFF;")
        container2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        splitter.addWidget(container2)

        main_layout.addWidget(splitter)

        self.setCentralWidget(main_widget)

    # TODO: This is a temporary solution for testing purposes.
    # This should be implemented using observers.
    def reload_structure_menu(self):
        """
        Reload the StructureMenu widget in the MainWindow
        """
        self.centralWidget().layout().itemAt(0).widget().deleteLater()

        structure_menu = StructureMenu(self, self.service_manager)
        self.create_main_layout(structure_menu)
