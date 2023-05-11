# ==========================================================================
# File: qt.py
# Description: PyQT6 main view for the PROTEUS application
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
# TODO: Refactor this file

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.services.archetype_service import ArchetypeService


# --------------------------------------------------------------------------
# Class: MainWindow
# Description: Main window for the PROTEUS application
# Date: 11/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create an ArchetypeService instance
        self.archetype_service = ArchetypeService()

        layout = QVBoxLayout()

        # Get project archetypes
        archetypes = self.archetype_service.get_project_archetypes()
        for project_arch in archetypes:
            label =QLabel(f"{project_arch.id} \n \t {project_arch.documents.keys()} \n")
            layout.addWidget(label)

        # Set the layout for the main window
        self.setLayout(layout)
