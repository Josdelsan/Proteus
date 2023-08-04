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
from typing import Dict, Callable, List
import logging
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QDateEdit,
    QTextEdit,
    QCheckBox,
    QFileDialog,
    QLabel,
    QVBoxLayout,
)
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

# --------------------------------------------------------------------------
# String property input and validator
# --------------------------------------------------------------------------
def _string_property_input(property: StringProperty) -> QLineEdit:
    string_input = QLineEdit()
    string_input.setText(property.value)
    return string_input

def _string_property_validator(input: QLineEdit) -> str:
    # Get the input text
    text = input.text()

    # Check if the input is valid
    if not text:
        return "This field cannot be empty"
    
    # Return None if the input is valid
    return None

# --------------------------------------------------------------------------
# Date property input and validator
# --------------------------------------------------------------------------
def _date_property_input(property) -> QDateEdit:
    date_input = QDateEdit()
    date_input.setDate(property.value)
    return date_input

# NOTE: This validator is not used yet
def _date_property_validator(input: QDateEdit) -> str:
    pass


# --------------------------------------------------------------------------
# Markdown property input and validator
# --------------------------------------------------------------------------
def _markdown_property_input(property) -> QTextEdit:
    markdown_input = QTextEdit()
    markdown_input.setPlainText(property.value)
    return markdown_input

def _markdown_property_validator(input: QTextEdit) -> str:
    pass


# --------------------------------------------------------------------------
# Boolean property input and validator
# --------------------------------------------------------------------------
def _boolean_property_input(property) -> QCheckBox:
    boolean_input = QCheckBox()
    state = Qt.CheckState.Checked if bool(property.value) else Qt.CheckState.Unchecked
    boolean_input.setCheckState(state)
    return boolean_input

def _boolean_property_validator(input: QCheckBox) -> str:
    pass


# --------------------------------------------------------------------------
# Float property input and validator
# --------------------------------------------------------------------------
def _float_property_input(property) -> QLineEdit:
    # TODO: Perform validation to prevent non-numeric values
    float_input = QLineEdit()
    float_input.setText(str(property.value))
    return float_input

def _float_property_validator(input: QLineEdit) -> str:
    # Perform validation to prevent non-numeric values
    text = input.text()
    try:
        float(text)
    except ValueError:
        return "This field must be a number"
    
    # Return None if the input is valid
    return None

# --------------------------------------------------------------------------
# Integer property input and validator
# --------------------------------------------------------------------------
def _integer_property_input(property) -> QLineEdit:
    # TODO: Perform validation to prevent non-numeric values
    float_input = QLineEdit()
    float_input.setText(str(property.value))
    return float_input

def _integer_property_validator(input: QLineEdit) -> str:
    # Perform validation to prevent non-numeric values
    text = input.text()
    try:
        int(text)
    except ValueError:
        return "This field must be an integer"
    
    # Return None if the input is valid
    return None

# --------------------------------------------------------------------------
# Enum property input and validator
# --------------------------------------------------------------------------
def _enum_property_input(property) -> QLineEdit:
    enum_input = QLineEdit()
    enum_input.setText(property.value)
    return enum_input

def _enum_property_validator(input: QLineEdit) -> str:
    pass


# --------------------------------------------------------------------------
# Url property input and validator
# --------------------------------------------------------------------------
def _url_property_input(property) -> QLineEdit:
    url_input = QLineEdit()
    url_input.setText(property.value)
    return url_input

def _url_property_validator(input: QLineEdit) -> str:
    pass

# --------------------------------------------------------------------------
# File property input and validator
# --------------------------------------------------------------------------
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

def _file_property_validator(input: QLineEdit) -> str:
    pass


# --------------------------------------------------------------------------
# Class: PropertyInputWidget
# Description: Implementation of a property input widget that wraps a
#              property input widget and adds a label to display errors.
# Date: 04/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class PropertyInputWidget(QWidget):
    """
    Property input widget that wraps a property input widget and adds a label
    to display errors.
    """

    # Map of widget types to value conversion functions
    getter_conversion_map: Dict[type[QWidget], Callable[[QWidget], str]] = {
        QLineEdit: lambda widget: widget.text(),
        QDateEdit: lambda widget: widget.date().toPyDate(),
        QTextEdit: lambda widget: widget.toPlainText(),
        QCheckBox: lambda widget: widget.isChecked(),
    }

    def __init__(self, input: QWidget, validator: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check input and validator are provided
        assert input is not None, "Must provide an input widget"
        assert validator is not None, "Must provide a validator"

        # Initialize error label
        self.validator = validator
        self.input = input
        self.error_label: QLabel = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        # Initialize layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.error_label)
        self.setLayout(self.layout)

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> str:
        """
        Returns the value of the input widget. The value is converted to a
        string depending on the widget type.
        """
        widget_type = type(self.input)
        if widget_type in PropertyInputWidget.getter_conversion_map:
            conversion_func = PropertyInputWidget.getter_conversion_map[widget_type]
            return conversion_func(self.input)
        else:
            log.error(
                f"Unsupported widget type {widget_type} when converting to string"
            )
            return None

    # ----------------------------------------------------------------------
    # Method     : has_errors
    # Description: Returns true if the input has errors, false otherwise.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def has_errors(self) -> bool:
        """
        Returns true if the input has errors, false otherwise. If the input
        has errors, the error label will be shown.
        """
        error: str = self.validator(self.input)
        if error:
            self.error_label.setText(error)
            self.error_label.show()
            return True
        else:
            self.error_label.hide()
            return False

# --------------------------------------------------------------------------
# Class: PropertyInputFactory
# Description: Implementation of a property input factory to handle the
#              creation of property input widgets.
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class PropertyInputFactory:
    """
    Implementation of a property input factory to handle the creation of
    property input widgets.
    """
    # Map of property types to input creation functions
    property_input_map: Dict[type[Property], List[Callable]] = {
        StringProperty: (_string_property_input, _string_property_validator),
        DateProperty: (_date_property_input, _date_property_validator),
        MarkdownProperty: (_markdown_property_input, _markdown_property_validator),
        BooleanProperty: (_boolean_property_input, _boolean_property_validator),
        FloatProperty: (_float_property_input, _float_property_validator),
        IntegerProperty: (_integer_property_input, _integer_property_validator),
        EnumProperty: (_enum_property_input, _enum_property_validator),
        FileProperty: (_file_property_input, _file_property_validator),
        UrlProperty: (_url_property_input, _url_property_validator),
    }

    # ----------------------------------------------------------------------
    # Method     : create
    # Description: Creates a property input widget for the given property.
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create(property: Property) -> PropertyInputWidget:
        try:
            property_input, property_validator = PropertyInputFactory.property_input_map[type(property)]
            return PropertyInputWidget(property_input(property), property_validator)
        except KeyError:
            log.error(f"Property input widget for {type(property)} was not found")
            return None