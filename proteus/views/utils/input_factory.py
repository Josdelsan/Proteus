# ==========================================================================
# File: property_input.py
# Description: Implementation of a property input factory to handle the
#              creation of property input widgets.
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import shutil
from typing import Dict, Callable, Tuple
import logging
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QLineEdit, QDateEdit, QTextEdit, QCheckBox, QFileDialog, QPushButton
from PyQt6.QtCore import Qt

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ASSETS_REPOSITORY
from proteus.config import Config
from proteus.model.properties.property import Property
from proteus.model.properties.string_property import StringProperty
from proteus.model.properties.boolean_property import BooleanProperty
from proteus.model.properties.date_property import DateProperty
from proteus.model.properties.time_property import TimeProperty
from proteus.model.properties.markdown_property import MarkdownProperty
from proteus.model.properties.integer_property import IntegerProperty
from proteus.model.properties.float_property import FloatProperty
from proteus.model.properties.enum_property import EnumProperty
from proteus.model.properties.file_property import FileProperty
from proteus.model.properties.url_property import UrlProperty
from proteus.model.properties.classlist_property import ClassListProperty

# logging configuration
log = logging.getLogger(__name__)

def _string_property_input(property: StringProperty) -> Tuple[QWidget, QLineEdit]:
    string_input = QLineEdit()
    string_input.setText(property.value)
    return string_input

def _date_property_input(property) -> Tuple[QWidget, QDateEdit]:
    date_input = QDateEdit()
    date_input.setDate(property.value)
    return date_input

def _markdown_property_input(property) -> Tuple[QWidget, QTextEdit]:
    markdown_input = QTextEdit()
    markdown_input.setPlainText(property.value)
    return markdown_input

def _boolean_property_input(property) -> QLineEdit:
    boolean_input = QCheckBox()
    state = Qt.CheckState.Checked if bool(property.value) else Qt.CheckState.Unchecked
    boolean_input.setCheckState(state)
    return  boolean_input

def _float_property_input(property) -> QLineEdit:
    # TODO: Perform validation to prevent non-numeric values
    float_input = QLineEdit()
    float_input.setText(str(property.value))
    return float_input

def _integer_property_input(property) -> QLineEdit:
    # TODO: Perform validation to prevent non-numeric values
    float_input = QLineEdit()
    float_input.setText(str(property.value))
    return float_input

def _enum_property_input(property) -> QLineEdit:
    enum_input = QLineEdit()
    enum_input.setText(property.value)
    return enum_input

def _file_property_input(property) -> QLineEdit:
    
    def _open_file_dialog(*args, **kwargs):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpeg *.jpg, *.gif, *.svg)")
        file_dialog.exec()

        # Get the name of the selected file
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            selected_file = selected_files[0]

            # Build file path
            file_path: Path = Path(selected_file)
            
            # NOTE: We copy the file to the project directory
            # so we can perform undo/redo operations. If we don't
            # copy it now, we cannot access the file when properties
            # are updated. Every file that is not used by any property
            # must be deleted when the project closes.
            assets_path = f"{Config().current_project_path}/{ASSETS_REPOSITORY}"
            shutil.copy(file_path, assets_path)

            # Get file name
            # NOTE: It will be stored in the property value and
            # used to create the path to the file relative to
            # the project directory
            file_name = file_path.name
            file_input.setText(file_name)

    file_input = QLineEdit()
    file_input.setText(property.value)

    # Connect click event to open file dialog
    file_input.mousePressEvent = _open_file_dialog
    return file_input    

# --------------------------------------------------------------------------
# Class: PropertyInputFactory
# Description: Implementation of a property input factory to handle the
#              creation of property input widgets.
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class PropertyInputFactory():

    property_input_map : Dict[type[Property], Callable] = {
        StringProperty: _string_property_input,
        DateProperty: _date_property_input,
        MarkdownProperty: _markdown_property_input,
        BooleanProperty: _boolean_property_input,
        FloatProperty: _float_property_input,
        IntegerProperty: _integer_property_input,
        EnumProperty: _enum_property_input,
        FileProperty: _file_property_input,
    }

    widget_conversion_map: Dict[type[QWidget], Callable[[QWidget], str]] = {
        QLineEdit: lambda widget: widget.text(),
        QDateEdit: lambda widget: widget.date().toPyDate(),
        QTextEdit: lambda widget: widget.toPlainText(),
        QCheckBox: lambda widget: widget.isChecked(),
    }

    # ----------------------------------------------------------------------
    # Method     : create
    # Description: Creates a property input widget for the given property.
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create(property: Property):
        try:
            return PropertyInputFactory.property_input_map[type(property)](property)
        except KeyError:
            log.error(f"Property input widget for {type(property)} was not found")
            return None
    
    # ----------------------------------------------------------------------
    # Method     : widget_to_value
    # Description: Converts the given widget to a string value depending on
    #              the widget type.
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def widget_to_value(widget) -> str:
        widget_type = type(widget)
        if widget_type in PropertyInputFactory.widget_conversion_map:
            conversion_func = PropertyInputFactory.widget_conversion_map[widget_type]
            return conversion_func(widget)
        else:
            log.error(f"Unsupported widget type {widget_type} when converting to string")
            return None
