# ==========================================================================
# File: buttons.py
# Description: File containing different buttons functions for the PROTEUS
#              application
# Date: 29/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import typing
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QDockWidget, \
                            QToolButton, QStyle, QApplication, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.config import Config
from proteus.model.object import Object

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

config : Config = Config()

# --------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------

def new_project_button(parent: QWidget) -> QToolButton:
    """
    Creates a new project button adapted to the PROTEUS application style.
    """
    # Create button with parent
    new_button = QToolButton(parent)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
    new_button.setIcon(QIcon(file_icon))
    new_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    new_button.setToolTip("Create new project\nCtrl+N")
    new_button.setStatusTip("Create new project from a project template. Shortcut: Ctrl+N")
    
    # Set text
    new_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    new_button.setText("New")

    # Set shorcut
    new_button.setShortcut("Ctrl+N")

    return new_button

def open_project_button(parent: QWidget) -> QToolButton:
    """
    Creates a open project button adapted to the PROTEUS application style.
    """
    # Create button with parent
    open_button = QToolButton(parent)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
    open_button.setIcon(QIcon(file_icon))
    open_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    open_button.setToolTip("Open existing project\nCtrl+O")
    open_button.setStatusTip("Open existing project from a project template. Shortcut: Ctrl+O")
    
    # Set text
    open_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    open_button.setText("Open")

    # Set shorcut
    open_button.setShortcut("Ctrl+O")

    return open_button

def save_project_button(parent: QWidget) -> QToolButton:
    """
    Creates a save project button adapted to the PROTEUS application style.
    """
    # Create button with parent
    save_button = QToolButton(parent)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
    save_button.setIcon(QIcon(file_icon))
    save_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    save_button.setToolTip("Save project\nCtrl+S")
    save_button.setStatusTip("Save all project changes. Saved actions cannot be reverted. Shortcut: Ctrl+S")
    
    # Set text
    save_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    save_button.setText("Save")

    # Set shorcut
    save_button.setShortcut("Ctrl+S")

    # Set enabled initial value
    save_button.setEnabled(False)

    return save_button

def undo_button(parent: QWidget) -> QToolButton:
    """
    Creates a undo button adapted to the PROTEUS application style.
    """
    # Create button with parent
    undo_button = QToolButton(parent)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
    undo_button.setIcon(QIcon(file_icon))
    undo_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    undo_button.setToolTip("Undo last action\nCtrl+Z")
    undo_button.setStatusTip("Undo last action. Shortcut: Ctrl+Z")
    
    # Set text
    undo_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    undo_button.setText("Undo")

    # Set shorcut
    undo_button.setShortcut("Ctrl+Z")

    # Set enabled initial value
    undo_button.setEnabled(False)

    return undo_button

def redo_button(parent: QWidget) -> QToolButton:
    """
    Creates a redo button adapted to the PROTEUS application style.
    """
    # Create button with parent
    redo_button = QToolButton(parent)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
    redo_button.setIcon(QIcon(file_icon))
    redo_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    redo_button.setToolTip("Redo last action\nCtrl+Y")
    redo_button.setStatusTip("Redo last action. Shortcut: Ctrl+Y")
    
    # Set text
    redo_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    redo_button.setText("Redo")

    # Set shorcut
    redo_button.setShortcut("Ctrl+Y")

    # Set enabled initial value
    redo_button.setEnabled(False)

    return redo_button


def project_properties_button(parent: QWidget) -> QToolButton:
    """
    Creates a project properties button adapted to the PROTEUS application style.
    """
    # Create button with parent
    properties_button = QToolButton(parent)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
    properties_button.setIcon(QIcon(file_icon))
    properties_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    properties_button.setToolTip("Project properties\nCtrl+P")
    properties_button.setStatusTip("Show project properties. Shortcut: Ctrl+P")
    
    # Set text
    properties_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    properties_button.setText("Project properties")

    # Set shorcut
    properties_button.setShortcut("Ctrl+P")

    # Set enabled initial value
    properties_button.setEnabled(False)

    return properties_button



def add_document_button(parent: QWidget) -> QToolButton:
    """
    Creates a add document button adapted to the PROTEUS application style.
    """
    # Create button with parent
    add_button = QToolButton(parent)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
    add_button.setIcon(QIcon(file_icon))
    add_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    add_button.setToolTip("Add document\nCtrl+D")
    add_button.setStatusTip("Add document to the project. Shortcut: Ctrl+D")
    
    # Set text
    add_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    add_button.setText("Add document")

    # Set shorcut
    add_button.setShortcut("Ctrl+D")

    # Set enabled initial value
    add_button.setEnabled(False)

    return add_button

# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------

class ArchetypeMenuButton(QToolButton):
    """
    Class that implements a button for the archetype menu.
    """

    def __init__(self, parent: QWidget, archetype : Object) -> None:
        super().__init__(parent)

        # Set icon
        archetype_icon = QIcon()

        # Get icon path
        icon_directory_path = f"{config.icons_directory}/archetypes"
        icon_path = f"{icon_directory_path}/{archetype.id}.svg"

        # Check if icon exists
        if not os.path.isfile(icon_path):
            icon_path = f"{icon_directory_path}/default.svg"

        # Add icon
        archetype_icon.addFile(icon_path, QSize(32, 32))
        self.setIcon(archetype_icon)
        self.setIconSize(QSize(32, 32))

        # Set tooltip
        arch_name = archetype.properties["name"].value
        self.setToolTip(f"{arch_name}")
        self.setStatusTip(f"Archetype {arch_name}, class {archetype.classes}")

        # Set text
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setText(arch_name)

        # Set enabled initial value
        self.setEnabled(False)




