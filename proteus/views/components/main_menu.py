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


# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QMenuBar, QFileDialog
from PyQt6.QtGui import QAction


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.utils.decorators import subscribe_to
from proteus.controller.command_stack import Command
from proteus.views.components.abstract_component import AbstractComponent


# --------------------------------------------------------------------------
# Class: MenuBar
# Description: PyQT6 main manu class for the PROTEUS application menu
# Date: 16/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@subscribe_to()
class MainMenu(QMenuBar, AbstractComponent):
    """
    Menubar for the PROTEUS application. It is used to manage the
    creation of the menubar and its actions.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        AbstractComponent.__init__(self)

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the main menu for the PROTEUS application
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self):
        """
        Create the menubar for the PROTEUS application
        """

        # ---------------------------------------------
        # File menu
        # ---------------------------------------------
        file_menu = self.addMenu("File")

        # Open action
        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        # Close save action
        file_menu.addActions(
            [
                QAction("Close", self),
                QAction("Save", self),
            ]
        )

        # ---------------------------------------------
        # Edit menu
        # ---------------------------------------------
        edit_menu = self.addMenu("Edit")

        # Undo action
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)

        # Redo action
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addActions(
            [
                QAction("Cut", self),
                QAction("Copy", self),
                QAction("Paste", self),
            ]
        )

    # ----------------------------------------------------------------------
    # Method     : update_component
    # Description: Update the main menu for the PROTEUS application
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self) -> None:
        # TODO: Update main menu options depending on the current state
        #       of the application
        pass


    # ----------------------------------------------------------------------
    # Method     : open_project
    # Description: Manage the open project action, open a project using a
    #              file dialog and loads it.
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def open_project(self):
        """
        Manage the open project action, open a project using a file dialog
        and loads it.
        """
        directory_dialog = QFileDialog(self)
        directory_path = directory_dialog.getExistingDirectory(
            None, "Open Directory", ""
        )

        if directory_path:
            Command.load_project(project_path=directory_path)


    # ----------------------------------------------------------------------
    # Method     : undo_action
    # Description: Manage the undo action, undo the last action performed
    #              by the user if the action is undoable.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo_action(self):
        Command.undo()

    # ----------------------------------------------------------------------
    # Method     : redo_action
    # Description: Manage the redo action, redo the last undo action
    #              performed by the user.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo_action(self):
        Command.redo()