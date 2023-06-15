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
from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QWidget,
    QToolButton,
    QStyle,
    QApplication,
    QFrame,
    QGridLayout,
    QLabel,
)
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

config: Config = Config()
ARCHETYPE_ICONS_PATH = f"{config.icons_directory}/archetypes"
MENU_ICONS_PATH = f"{config.icons_directory}/main_menu"

# --------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------


def new_project_button(parent: QWidget) -> QToolButton:
    """
    Creates a new project button adapted to the PROTEUS application style.
    """
    # Create button with parent
    new_button = QToolButton(parent)
    new_button.setFixedWidth(50)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
    new_button.setIcon(QIcon(file_icon))
    new_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    new_button.setToolTip("Create new project\nCtrl+N")
    new_button.setStatusTip(
        "Create new project from a project template. Shortcut: Ctrl+N"
    )

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
    open_button.setFixedWidth(50)

    # Set file icon
    file_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
    open_button.setIcon(QIcon(file_icon))
    open_button.setIconSize(file_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    open_button.setToolTip("Open existing project\nCtrl+O")
    open_button.setStatusTip(
        "Open existing project from a project template. Shortcut: Ctrl+O"
    )

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
    save_button.setFixedWidth(50)

    # Set file icon
    icon_path = f"{MENU_ICONS_PATH}/save-button.svg"
    button_icon = QIcon()
    button_icon.addFile(icon_path, QSize(32, 32))
    save_button.setIcon(button_icon)
    save_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    save_button.setToolTip("Save project\nCtrl+S")
    save_button.setStatusTip(
        "Save all project changes. Saved actions cannot be reverted. Shortcut: Ctrl+S"
    )

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
    undo_button.setFixedWidth(50)

    # Set file icon
    icon_path = f"{MENU_ICONS_PATH}/undo.svg"
    button_icon = QIcon()
    button_icon.addFile(icon_path, QSize(32, 32))
    undo_button.setIcon(button_icon)
    undo_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

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
    redo_button.setFixedWidth(50)

    # Set file icon
    icon_path = f"{MENU_ICONS_PATH}/redo.svg"
    button_icon = QIcon()
    button_icon.addFile(icon_path, QSize(32, 32))
    redo_button.setIcon(button_icon)
    redo_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

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
    properties_button.setFixedWidth(50)

    # Set file icon
    icon_path = f"{MENU_ICONS_PATH}/edit-button.svg"
    button_icon = QIcon()
    button_icon.addFile(icon_path, QSize(32, 32))
    properties_button.setIcon(button_icon)
    properties_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    properties_button.setToolTip("Project properties\nCtrl+P")
    properties_button.setStatusTip("Show project properties. Shortcut: Ctrl+P")

    # Set text
    properties_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    properties_button.setText("Edit")

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
    add_button.setFixedWidth(50)

    # Set file icon
    icon_path = f"{MENU_ICONS_PATH}/new-file-button.svg"
    button_icon = QIcon()
    button_icon.addFile(icon_path, QSize(32, 32))
    add_button.setIcon(button_icon)
    add_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    add_button.setToolTip("Add document\nCtrl+D")
    add_button.setStatusTip("Add document to the project. Shortcut: Ctrl+D")

    # Set text
    add_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    add_button.setText("Add")

    # Set shorcut
    add_button.setShortcut("Ctrl+D")

    # Set enabled initial value
    add_button.setEnabled(False)

    return add_button


def delete_document_button(parent: QWidget) -> QToolButton:
    """
    Creates a delete document button adapted to the PROTEUS application style.
    """
    # Create button with parent
    delete_button = QToolButton(parent)
    delete_button.setFixedWidth(50)

    # Set file icon
    icon_path = f"{MENU_ICONS_PATH}/delete-file-button.svg"
    button_icon = QIcon()
    button_icon.addFile(icon_path, QSize(32, 32))
    delete_button.setIcon(button_icon)
    delete_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    delete_button.setToolTip("Delete current document")
    delete_button.setStatusTip("Delete document from project.")

    # Set text
    delete_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    delete_button.setText("Delete")

    # Set enabled initial value
    delete_button.setEnabled(False)

    return delete_button


def button_group(section_name: str, buttons: List[QToolButton]) -> QWidget:
    # Create the main widget
    widget = QWidget()
    widget.setContentsMargins(0, 0, 5, 0)

    # Create the grid layout
    layout = QGridLayout(widget)

    # Add the buttons in the first row of the layout
    for column, button in enumerate(buttons):
        layout.addWidget(button, 0, column)

    # Add a separator line in the second row of the layout
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)
    layout.addWidget(separator, 1, 0, 1, len(buttons))

    # Add a centered label with the text "section" in the third row of the layout
    section_label = QLabel(section_name)
    section_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(section_label, 2, 0, 1, len(buttons))

    # Set layout margins and spacing
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    return widget


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------


class ArchetypeMenuButton(QToolButton):
    """
    Class that implements a button for the archetype menu.
    """

    def __init__(self, parent: QWidget, archetype: Object) -> None:
        super().__init__(parent)

        # Button settings
        self.setFixedWidth(80)

        # Set icon
        archetype_icon = QIcon()

        # Build icon path from archetype id or use default icon
        icon_path = f"{ARCHETYPE_ICONS_PATH}/{archetype.id}.svg"
        if not os.path.isfile(icon_path):
            icon_path = f"{ARCHETYPE_ICONS_PATH}/default.svg"

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
