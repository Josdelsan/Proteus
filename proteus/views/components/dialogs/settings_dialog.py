# ==========================================================================
# File: settings_dialog.py
# Description: PyQT6 settings dialog component for the PROTEUS application
# Date: 27/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QDialogButtonBox,
)


# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.config import LANGUAGE
from proteus.controller.command_stack import Controller
from proteus.views.components.abstract_component import ProteusComponent


# --------------------------------------------------------------------------
# Class: SettingsDialog
# Description: PyQT6 settings dialog component for the PROTEUS application
# Date: 27/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class SettingsDialog(QDialog, ProteusComponent):
    """
    Settings dialog component class for the PROTEUS application. It provides a
    dialog form to change the application settings.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 27/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, controller: Controller, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Create properties to store the new document data.
        """
        super(SettingsDialog, self).__init__(controller, *args, **kwargs)

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component
    # Date       : 27/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        # Set the dialog title
        self.setWindowTitle(self._translator.text("settings_dialog.title"))

        # -------------------------------------------
        # Language settings
        # -------------------------------------------

        # Get available languages from i18n directory
        i18n_dir: Path = self._config.i18n_directory
        languages: List[str] = [lang.stem for lang in i18n_dir.glob("*.yaml")]

        # Create a combo box with the available views
        lang_label: QLabel = QLabel(
            self._translator.text("settings_dialog.language.label")
        )
        view_combo: QComboBox = QComboBox()

        # TODO: Set the current configuration and only update the values that
        #       are different from the current configuration
        # Add the languages to the combo box
        for lang in languages:
            view_combo.addItem(self._translator.text(lang), lang)

        # -------------------------------------------
        # Component general setup
        # -------------------------------------------
        # Create Save and Cancel buttons
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect the buttons to the slots, combo current text is the view name
        button_box.accepted.connect(
            lambda: self.save_button_clicked(view_combo.currentData())
        )
        button_box.rejected.connect(self.cancel_button_clicked)

        # Error message label
        self.error_label: QLabel = QLabel()
        self.error_label.setObjectName("error_label")

        # Setting message label
        setting_info_label: QLabel = QLabel(self._translator.text("settings_dialog.info.label"))
        setting_info_label.setStyleSheet("font-weight: bold")

        # Add the widgets to the layout
        layout.addWidget(lang_label)
        layout.addWidget(view_combo)
        layout.addWidget(self.error_label)
        layout.addWidget(setting_info_label)

        layout.addWidget(button_box)

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Save button clicked event handler
    # Date       : 27/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    # TODO: This method will handle more settings in the future
    def save_button_clicked(self, combo_text: str) -> None:
        """
        Manage the save button clicked event. It saves the current settings
        """
        if combo_text is None:
            self.error_label.setText(
                self._translator.text("settings_dialog.error.invalid_language")
            )
            return

        # Save the current settings to the config file
        settings: Dict[str, str] = {LANGUAGE: combo_text}
        self._config.save_user_settings(settings)

        # Close the form window
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Cancel button clicked event handler
    # Date       : 27/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def cancel_button_clicked(self) -> None:
        """
        Manage the cancel button clicked event. It closes the form window
        without saving any changes.
        """
        # Close the form window without saving any changes
        self.close()
        self.deleteLater()

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog
    # Description: Create a settings dialog and show it
    # Date       : 27/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(controller: Controller) -> "SettingsDialog":
        """
        Create a settings dialog and show it
        """
        dialog = SettingsDialog(controller)
        dialog.exec()
        return dialog
