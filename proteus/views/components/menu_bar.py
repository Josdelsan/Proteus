# ==========================================================================
# File: menu_bar.py
# Description: PyQT6 menubar for the PROTEUS application
# Date: 16/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QMenuBar, QFileDialog, QWidget
from PyQt6.QtGui import QAction


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.services.service_manager import ServiceManager


# --------------------------------------------------------------------------
# Class: MenuBar
# Description: PyQT6 menubar class for the PROTEUS application menus
# Date: 16/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@dataclass
class MenuBar(QMenuBar):
    """
    Menubar for the PROTEUS application. It is used to manage the
    creation of the menubar and its actions.
    """

    # Instance attributes
    parent: QWidget = None
    service_manager: ServiceManager = None

    # ----------------------------------------------------------------------
    # Method     : __post_init__
    # Description: Class post constructor
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __post_init__(self):
        """
        Class post constructor
        """
        super(QMenuBar, self).__init__(self.parent)

        # Create the menubar
        self.create_menu_bar()

    # ----------------------------------------------------------------------
    # Method     : create_menu_bar
    # Description: Create the menubar for the PROTEUS application
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_menu_bar(self):
        """
        Create the menubar for the PROTEUS application
        """

        # ---------------------------------------------
        # File menu
        # ---------------------------------------------
        file_menu = self.addMenu("File")

        # Open action
        open_action = QAction("Open...", self.parent)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        # Close save action
        file_menu.addActions(
            [
                QAction("Close", self.parent),
                QAction("Save", self.parent),
            ]
        )

        # ---------------------------------------------
        # Edit menu
        # ---------------------------------------------
        edit_menu = self.addMenu("Edit")
        edit_menu.addActions(
            [
                QAction("Undo", self.parent),
                QAction("Cut", self.parent),
                QAction("Copy", self.parent),
                QAction("Paste", self.parent),
            ]
        )

    # ----------------------------------------------------------------------
    # Method     : open_file
    # Description: Open a project using a file dialog and load it
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def open_project(self):
        """
        Open a file using a file dialog and perform some action with the selected path.
        """
        directory_dialog = QFileDialog(self)
        directory_path = directory_dialog.getExistingDirectory(
            None, "Open Directory", ""
        )

        if directory_path:
            self.service_manager.load_project(directory_path)

            # TODO: This is a temporary solution for testing purposes.
            # This should be implemented using observers.

            # Reload the StructureMenu widget in the MainWindow
            main_window = self.parent
            main_window.reload_structure_menu()
