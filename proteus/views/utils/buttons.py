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

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QDockWidget, \
                            QToolButton, QStyle, QApplication, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

# --------------------------------------------------------------------------
# Project specific imports
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

    return redo_button



