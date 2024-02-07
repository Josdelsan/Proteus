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

from typing import List
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QWidget,
    QToolButton,
    QFrame,
    QGridLayout,
    QLabel,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils.config import Config
from proteus.utils import ProteusIconType
from proteus.model import ProteusClassTag
from proteus.utils.translator import Translator

# Module configuration
_ = Translator().text  # Translator

# --------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------


def new_project_button(parent: QWidget) -> QToolButton:
    """
    Creates a new project button adapted to the PROTEUS application style.
    """
    # Create button with parent
    new_button = QToolButton(parent)
    new_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "new-project")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    new_button.setIcon(button_icon)
    new_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    new_button.setToolTip(_("new_project_button.tooltip"))
    new_button.setStatusTip(_("new_project_button.statustip"))

    # Set text
    new_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    new_button.setText(_("new_project_button.text"))

    # Set shortcut
    new_button.setShortcut("Ctrl+N")

    return new_button


def open_project_button(parent: QWidget) -> QToolButton:
    """
    Creates an open project button adapted to the PROTEUS application style.
    """
    # Create button with parent
    open_button = QToolButton(parent)
    open_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "open-project")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    open_button.setIcon(QIcon(button_icon))
    open_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    open_button.setToolTip(_("open_project_button.tooltip"))
    open_button.setStatusTip(_("open_project_button.statustip"))

    # Set text
    open_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    open_button.setText(_("open_project_button.text"))

    # Set shortcut
    open_button.setShortcut("Ctrl+O")

    return open_button


def save_project_button(parent: QWidget) -> QToolButton:
    """
    Creates a save project button adapted to the PROTEUS application style.
    """
    # Create button with parent
    save_button = QToolButton(parent)
    save_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "save")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    save_button.setIcon(button_icon)
    save_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    save_button.setToolTip(_("save_project_button.tooltip"))
    save_button.setStatusTip(_("save_project_button.statustip"))

    # Set text
    save_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    save_button.setText(_("save_project_button.text"))

    # Set shortcut
    save_button.setShortcut("Ctrl+S")

    # Set enabled initial value
    save_button.setEnabled(False)

    return save_button


def undo_button(parent: QWidget) -> QToolButton:
    """
    Creates an undo button adapted to the PROTEUS application style.
    """
    # Create button with parent
    undo_button = QToolButton(parent)
    undo_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "undo")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    undo_button.setIcon(button_icon)
    undo_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    undo_button.setToolTip(_("undo_button.tooltip"))
    undo_button.setStatusTip(_("undo_button.statustip"))

    # Set text
    undo_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    undo_button.setText(_("undo_button.text"))

    # Set shortcut
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
    redo_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "redo")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    redo_button.setIcon(button_icon)
    redo_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    redo_button.setToolTip(_("redo_button.tooltip"))
    redo_button.setStatusTip(_("redo_button.statustip"))

    # Set text
    redo_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    redo_button.setText(_("redo_button.text"))

    # Set shortcut
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
    properties_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "edit")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    properties_button.setIcon(button_icon)
    properties_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    properties_button.setToolTip(_("project_properties_button.tooltip"))
    properties_button.setStatusTip(_("project_properties_button.statustip"))

    # Set text
    properties_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    properties_button.setText(_("project_properties_button.text"))

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
    add_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "new-file")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    add_button.setIcon(button_icon)
    add_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    add_button.setToolTip(_("add_document_button.tooltip"))
    add_button.setStatusTip(_("add_document_button.statustip"))

    # Set text
    add_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    add_button.setText(_("add_document_button.text"))

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
    delete_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "delete-file")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    delete_button.setIcon(button_icon)
    delete_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    delete_button.setToolTip(_("delete_document_button.tooltip"))
    delete_button.setStatusTip(_("delete_document_button.statustip"))

    # Set text
    delete_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    delete_button.setText(_("delete_document_button.text"))

    # Set enabled initial value
    delete_button.setEnabled(False)

    return delete_button


def settings_button(parent: QWidget) -> QToolButton:
    """
    Creates a settings button adapted to the PROTEUS application style.
    """
    # Create button with parent
    settings_button = QToolButton(parent)
    settings_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "settings")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    settings_button.setIcon(button_icon)
    settings_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    settings_button.setToolTip(_("settings_button.tooltip"))
    settings_button.setStatusTip(_("settings_button.statustip"))

    # Set text
    settings_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    settings_button.setText(_("settings_button.text"))

    return settings_button


def export_button(parent: QWidget) -> QToolButton:
    """
    Creates a export button adapted to the PROTEUS application style.
    """
    # Create button with parent
    export_button = QToolButton(parent)
    export_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "export")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    export_button.setIcon(button_icon)
    export_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    export_button.setToolTip(_("export_button.tooltip"))
    export_button.setStatusTip(_("export_button.statustip"))

    # Set text
    export_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    export_button.setText(_("export_button.text"))

    # Set initial disabled value
    export_button.setEnabled(False)

    return export_button


def info_button(parent: QWidget) -> QToolButton:
    """
    Creates a info button adapted to the PROTEUS application style.
    """
    # Create button with parent
    info_button = QToolButton(parent)
    info_button.setMinimumWidth(55)

    # Set file icon
    icon_path: Path = Config().get_icon(ProteusIconType.MainMenu, "info")
    button_icon = QIcon()
    button_icon.addFile(icon_path.as_posix(), QSize(32, 32))
    info_button.setIcon(QIcon(button_icon))
    info_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    info_button.setToolTip(_("information_button.tooltip"))
    info_button.setStatusTip(_("information_button.statustip"))

    # Set text
    info_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    info_button.setText(_("information_button.text"))

    return info_button


def button_group(section_name_code: str, buttons: List[QToolButton]) -> QWidget:
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
    section_label = QLabel(_(section_name_code))
    section_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(section_label, 2, 0, 1, len(buttons))

    # Set layout margins and spacing
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    return widget


# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------


# NOTE: ArchetypesMenuDropdown is set as menu for each button in the
# MainMenu component when the application is initialized.
class ArchetypeMenuButton(QToolButton):
    """
    Class that creates a button for the archetype menu. The dropdown menu
    is created in the MainMenu component using the ArchetypesMenuDropdown
    class.
    """

    def __init__(self, parent: QWidget, object_class: ProteusClassTag) -> None:
        super().__init__(parent)

        # Button settings
        self.setMinimumWidth(80)

        # Set icon
        archetype_icon = QIcon()

        # Build icon path from object_class or use default icon
        icon_path: Path = Config().get_icon(ProteusIconType.Archetype, object_class)

        # Add icon
        archetype_icon.addFile(icon_path.as_posix(), QSize(32, 32))
        self.setIcon(archetype_icon)
        self.setIconSize(QSize(32, 32))

        # Set tooltip
        translated_name = _(
            f"archetype.class.{object_class}", alternative_text=object_class
        )
        self.setToolTip(translated_name)

        # Set text
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setText(translated_name)

        # Set enabled initial value
        self.setEnabled(False)
