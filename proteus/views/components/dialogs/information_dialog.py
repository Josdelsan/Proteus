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

from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QLabel,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_VERSION
from proteus.controller.command_stack import Controller
from proteus.utils import ProteusIconType
from proteus.utils.translator import Translator
from proteus.views.components.abstract_component import ProteusComponent


# --------------------------------------------------------------------------
# Class: InformationDialog
# Description: Class for the PROTEUS application information dialog.
# Date: 09/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
# NOTE: Due to the simplicity of this component, it is not necessary to
# inherit from the ProteusComponent class. It will access the translator
# singleton directly.
class InformationDialog(QDialog, ProteusComponent):
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
        super(InformationDialog, self).__init__(*args, **kwargs)
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

        # Set window icon
        proteus_icon: Path = self._config.get_icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(QIcon(proteus_icon.as_posix()))

        # App name and version
        app_name = QLabel("PROTEUS")
        app_name.setStyleSheet("font-size: 20px; font-weight: bold;")

        app_version = QLabel(PROTEUS_VERSION)
        app_version.setStyleSheet("font-size: 16px; font-weight: bold;")
        app_version.setContentsMargins(0, 0, 0, 20)

        # App description
        app_description = QLabel(
            self.translator.text("information_dialog.description.text")
        )
        app_description.setWordWrap(True)
        app_description.setContentsMargins(0, 0, 0, 20)

        # License
        license = QLabel(self.translator.text("information_dialog.license.text"))
        license.setWordWrap(True)
        license.setContentsMargins(0, 0, 0, 20)

        # Terms of use and privacy policy
        terms_of_use = QLabel(
            self.translator.text("information_dialog.terms_of_use.text")
        )
        terms_of_use.setWordWrap(True)
        terms_of_use.setContentsMargins(0, 0, 0, 20)

        # Important notes
        important_notes = QLabel(
            self.translator.text("information_dialog.important_notes.text")
        )
        important_notes.setStyleSheet("font-weight: bold;")
        important_notes.setWordWrap(True)
        important_notes.setContentsMargins(0, 0, 0, 20)

        # Icons8 attribution
        icons8_attribution = QLabel("Icons by <a href='https://icons8.com'>Icons8</a>")
        icons8_attribution.setOpenExternalLinks(True)
        icons8_attribution.setContentsMargins(0, 0, 0, 20)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(app_name)
        layout.addWidget(app_version)
        layout.addWidget(app_description)
        layout.addWidget(license)
        layout.addWidget(terms_of_use)
        layout.addWidget(important_notes)
        layout.addWidget(icons8_attribution)

        # Set the layout
        self.setLayout(layout)

    # ======================================================================
    # Dialog slots methods (connected to the component signals and helpers)
    # ======================================================================

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog (static)
    # Description: Handle the creation and display of the form window.
    # Date       : 09/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(controller: Controller) -> "InformationDialog":
        """
        Handle the creation and display of the form window.

        :param controller: The application controller.
        """
        # Create the form window
        form_window = InformationDialog(controller=controller)
        form_window.exec()
        return form_window
