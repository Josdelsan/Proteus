# ==========================================================================
# File: information_dialog.py
# Description: PyQT6 information dialog component.
# Date: 09/08/2023
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

from PyQt6.QtCore import QByteArray, QMarginsF
from PyQt6.QtGui import QPageLayout, QPageSize
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialogButtonBox,
    QDialog,
    QLineEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
    QPushButton,
    QComboBox,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.object import Object
from proteus.controller.command_stack import Controller
from proteus.views.utils.translator import Translator
from proteus.views.utils.state_manager import StateManager


# --------------------------------------------------------------------------
# Class: InformationDialog
# Description: Class for the PROTEUS application information dialog.
# Date: 09/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class InformationDialog(QDialog):
    """
    Class for the PROTEUS application information dialog.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the page object and the controller instance.
        """
        super().__init__(*args, **kwargs)
        self.translator = Translator()
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the component.
        """
        # Set the dialog title
        self.setWindowTitle(self.translator.text("information_dialog.title"))

        # App name and version
        app_name = QLabel("PROTEUS")
        app_name.setStyleSheet("font-size: 20px; font-weight: bold;")

        app_version = QLabel("v1.0.0-alpha.1")
        app_version.setStyleSheet("font-size: 16px; font-weight: bold;")
        app_version.setContentsMargins(0, 0, 0, 20)

        # App description
        app_description = QLabel(
            self.translator.text(
                "information_dialog.description.text"
            )
        )
        app_description.setWordWrap(True)
        app_description.setContentsMargins(0, 0, 0, 20)

        # License
        license = QLabel(
            self.translator.text("information_dialog.license.text")
        )
        license.setWordWrap(True)
        license.setContentsMargins(0, 0, 0, 20)

        # Terms of use and privacy policy
        terms_of_use = QLabel(
            self.translator.text("information_dialog.terms_of_use.text")
        )
        terms_of_use.setWordWrap(True)
        terms_of_use.setContentsMargins(0, 0, 0, 20)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(app_name)
        layout.addWidget(app_version)
        layout.addWidget(app_description)
        layout.addWidget(license)
        layout.addWidget(terms_of_use)

        # Set the layout
        self.setLayout(layout)
    

    # ======================================================================
    # Dialog slots methods (connected to the component signals and helpers)
    # ======================================================================


    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : object_property_dialog (static)
    # Description: Handle the creation and display of the form window.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog():
        """
        Handle the creation and display of the form window.
        """
        # Create the form window
        form_window = InformationDialog()

        # Show the form window
        form_window.exec()
