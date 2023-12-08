# ==========================================================================
# File: property_input_factory.py
# Description: Property input to handle object and project properties forms
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import Union
from datetime import date

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.controller.command_stack import Controller
from proteus.model.properties.property import Property
from proteus.model.properties.code_property import ProteusCode
from proteus.model.trace import Trace
from proteus.views.utils.translator import Translator

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: PropertyInput
# Description: Implementation of a property input widget that wraps a
#              property input widget and adds a label to display errors.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
# TODO: This should be an abstract class but it has conflicts with the
#       metaclass of QWidget.
#       https://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
class PropertyInput(QWidget):
    """
    Property input widget that wraps a property input widget and adds a label
    to display errors.
    """

    def __init__(
        self,
        property: Union[Property, Trace],
        controller: Controller = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Initialize controller
        self.controller: Controller = controller

        # Initialize input widget by calling the abstract method
        self.input: QWidget = self.create_input(property, controller)
        self.property: Union[Property, Trace] = property

        # Initialize error label
        self.error_label: QLabel = QLabel()
        self.error_label.setObjectName("error_label")
        self.error_label.hide()

        # Horizontal layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.input)

        # Initialize inmutable checkbox, if the property is inmutable
        # the checkbox will be shown and the input will be disabled
        self.inmutable_checkbox: QCheckBox = None
        if isinstance(property, Property):
            inmutable: bool = property.inmutable
            if inmutable:
                self.inmutable_checkbox = QCheckBox()
                self.inmutable_checkbox.setChecked(inmutable)
                self.input.setEnabled(not inmutable)
                self.inmutable_checkbox.stateChanged.connect(self._update_enabled)
                horizontal_layout.addWidget(self.inmutable_checkbox)

        # Vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.error_label)
        self.setLayout(vertical_layout)

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
        error: str = self.validate()
        if error:
            error_msg: str = Translator().text(error)
            self.error_label.setText(error_msg)
            self.error_label.show()
            return True
        else:
            self.error_label.hide()
            return False

    # ----------------------------------------------------------------------
    # Method     : get_value (abstract)
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> Union[str, int, float, bool, date, list, ProteusCode]:
        """
        Returns the value of the input widget. The value is converted to a
        string.
        """
        pass

    # ----------------------------------------------------------------------
    # Method     : validate (abstract)
    # Description: Validates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> Union[str, None]:
        """
        Validates the input widget. Returns an error message if the input
        has errors, None otherwise.
        """
        pass

    # ----------------------------------------------------------------------
    # Method     : create_input (abstract)
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(property: Property, *args, **kwargs) -> QWidget:
        """
        Creates the input widget based on the property type.
        """
        pass

    # ======================================================================
    # Slots
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_enabled (slot)
    # Description: Updates the enabled state of the input widget.
    # Date       : 02/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _update_enabled(self, check_state: Qt.CheckState) -> None:
        """
        Updates the enabled state of the input widget.

        Only works for Property class properties.

        :param check_state: Check state of the inmutable checkbox.
        """
        # Check the state of the checkbox
        checked: bool = check_state == Qt.CheckState.Checked.value

        # Update the enabled state of the input widget
        self.input.setEnabled(not checked)

        # Trigger inmutable property warning
        if not checked:
            QMessageBox.warning(
                self,
                Translator().text("property_input.inmutable_property_warning.title"),
                Translator().text("property_input.inmutable_property_warning.text"),
            )
