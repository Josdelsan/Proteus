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

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.controller.command_stack import Controller
from proteus.model.properties.property import Property
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
class PropertyInput(QWidget):
    """
    Property input widget that wraps a property input widget and adds a label
    to display errors.
    """

    def __init__(self, property: Property, controller: Controller=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize controller
        self.controller: Controller = controller

        # Initialize input widget by calling the abstract method
        self.input: QWidget = None
        self.create_input(property)

        # Initialize error label
        self.error_label: QLabel = QLabel()
        self.error_label.setObjectName("error_label")
        self.error_label.hide()

        # Initialize layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.error_label)
        self.setLayout(self.layout)

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
    def get_value(self) -> str:
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
    def create_input(self, property: Property) -> None:
        """
        Creates the input widget based on the property type.
        """
        pass
