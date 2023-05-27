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

from typing import Dict, Callable, Tuple

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QDateEdit, QVBoxLayout, QTextEdit, QFormLayout

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
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



def _string_property_widget(property: StringProperty) -> Tuple[QWidget, QLineEdit]:
    widget = QWidget()

    layout = QFormLayout()
    widget.setLayout(layout)

    label = QLabel(f"{property.name}:")
    string_edit = QLineEdit()
    string_edit.setText(property.value)

    layout.addRow(label, string_edit)

    return widget, string_edit

def _date_property_widget(property) -> Tuple[QWidget, QDateEdit]:
    widget = QWidget()

    layout = QFormLayout()
    widget.setLayout(layout)

    label = QLabel(f"{property.name}:")
    date_edit = QDateEdit()
    date_edit.setDate(property.value)

    layout.addRow(label, date_edit)

    return widget, date_edit

def _markdown_property_widget(property) -> Tuple[QWidget, QTextEdit]:
    widget = QWidget()

    layout = QVBoxLayout()
    widget.setLayout(layout)

    label = QLabel(f"{property.name}:")
    markdown_edit = QTextEdit()
    markdown_edit.setPlainText(property.value)

    layout.addWidget(label)
    layout.addWidget(markdown_edit)

    return widget, markdown_edit

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
        StringProperty: _string_property_widget,
        DateProperty: _date_property_widget,
        MarkdownProperty: _markdown_property_widget,
    }

    widget_conversion_map: Dict[type[QWidget], Callable[[QWidget], str]] = {
        QLineEdit: lambda widget: widget.text(),
        QDateEdit: lambda widget: widget.date(),
        QTextEdit: lambda widget: widget.toPlainText(),
    }

    # ----------------------------------------------------------------------
    # Method     : create
    # Description: Creates a property input widget for the given property.
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def create(cls, property: Property):
        try:
            return cls.property_input_map[type(property)](property)
        except KeyError:
            proteus.logger.error(f"Property input for {type(property)} not found")
            return None
    
    # ----------------------------------------------------------------------
    # Method     : widget_to_value
    # Description: Converts the given widget to a string value depending on
    #              the widget type.
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def widget_to_value(cls, widget) -> str:
        widget_type = type(widget)
        if widget_type in cls.widget_conversion_map:
            conversion_func = cls.widget_conversion_map[widget_type]
            return conversion_func(widget)
        else:
            proteus.logger.error(f"Unsupported widget type {widget_type} when converting to string")
            return None
