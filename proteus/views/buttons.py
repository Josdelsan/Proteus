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

from PyQt6.QtWidgets import (
    QWidget,
    QToolButton,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtGui import QIcon, QFontMetrics
from PyQt6.QtCore import Qt, QSize

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils.dynamic_icons import DynamicIcons
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "new-project")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "open-project")
    open_button.setIcon(button_icon)
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "save")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "undo")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "redo")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "edit")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "new-file")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "delete-file")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "settings")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "export")
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
    button_icon = DynamicIcons().icon(ProteusIconType.MainMenu, "info")
    info_button.setIcon(QIcon(button_icon))
    info_button.setIconSize(button_icon.actualSize(QSize(32, 32)))

    # Set tooltip
    info_button.setToolTip(_("information_button.tooltip"))
    info_button.setStatusTip(_("information_button.statustip"))

    # Set text
    info_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    info_button.setText(_("information_button.text"))

    return info_button

# --------------------------------------------------------------------------
def button_group(buttons, section_name_code=None):
    # Create the main widget
    widget = QWidget()

    # Create the grid layout
    layout = QGridLayout(widget)

    # Add the buttons in the first row of the layout
    for column, button in enumerate(buttons):
        layout.addWidget(button, 0, column)

    if section_name_code is not None:
        # Add a centered label with the text "section" in the second row of the layout
        section_label = QLabel(_(section_name_code))
        section_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(section_label, 1, 0, 1, len(buttons))

    # Set layout settings
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    layout.setSpacing(0)

    return widget
    
# --------------------------------------------------------------------------
def archetype_button_group(buttons) -> QWidget:
    # Create the main widget
    widget = QWidget()
    widget.setObjectName("archetype_button_group")

    # Create the grid layout
    layout = QHBoxLayout(widget)

    # Add the buttons in the first row of the layout
    for button in buttons:
        layout.addWidget(button)

    # Set layout settings
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    layout.setSpacing(0)

    # Create a scroll area and set its widget
    scroll_area = QScrollArea()
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(widget)

    # Set up the scroll bar
    scroll_bar = scroll_area.horizontalScrollBar()
    scroll_bar.setSingleStep(20)

    return scroll_area


# --------------------------------------------------------------------------
def get_separator(vertical: bool = False) -> QFrame:
    """
    Returns a horizontal or vertical separator.

    :param vertical: If True, the separator will be vertical. If False, the
                        separator will be horizontal.
    """
    separator = QFrame()
    if vertical:
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setObjectName("v-separator")
    else:
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("h-separator")
    separator.setFrameShadow(QFrame.Shadow.Sunken)
    return separator


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
        self.setObjectName("archetype_menu_button")
        
        # Set icon
        archetype_icon = QIcon()

        # Add icon
        archetype_icon = DynamicIcons().icon(ProteusIconType.Archetype, object_class)
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

        # Set minimum width based on the text
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.averageCharWidth() * int(len(translated_name) * 1.2)
        text_width = max(text_width, 80)
        self.setMinimumWidth(text_width)
