# ==========================================================================
# File: settings_dialog.py
# Description: PyQT6 settings dialog component for the PROTEUS application
# Date: 27/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
# TODO:

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict
from pathlib import Path
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QDialogButtonBox,
)


# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.model.archetype_manager import ArchetypeManager
from proteus.utils.config import SETTING_LANGUAGE, SETTING_ARCHETYPE_REPOSITORY
from proteus.controller.command_stack import Controller
from proteus.utils import ProteusIconType
from proteus.views.forms.directory_edit import DirectoryEdit
from proteus.views.components.abstract_component import ProteusComponent


# logging configuration
log = logging.getLogger(__name__)


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
    def __init__(self, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Create properties to store the new document data.
        """
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.language_combo: QComboBox = None
        self.default_repository_checkbox: QCheckBox = None

        # Error message labels
        self.error_language_label: QLabel = None
        self.error_default_repository_label: QLabel = None

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
        # -------------------------------------------
        # Component general setup
        # -------------------------------------------
        # Set the dialog title
        self.setWindowTitle(self._translator.text("settings_dialog.title"))

        # Set window icon
        proteus_icon: Path = self._config.get_icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(QIcon(proteus_icon.as_posix()))

        # Create Save and Cancel buttons
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect the buttons to the slots, combo current text is the view name
        button_box.accepted.connect(self.save_button_clicked)
        button_box.rejected.connect(self.cancel_button_clicked)

        # Setting message label
        setting_info_label: QLabel = QLabel(
            self._translator.text("settings_dialog.info.label")
        )
        setting_info_label.setStyleSheet("font-weight: bold")

        # -------------------------------------------
        # Layouts
        # -------------------------------------------
        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        # Specific settings layouts
        language_layout: QVBoxLayout = self.create_language_layout()
        default_repository_layout: QVBoxLayout = self.create_default_repository_layout()

        # Add the widgets to the layout
        layout.addWidget(setting_info_label)
        layout.addLayout(language_layout)
        layout.addLayout(default_repository_layout)
        layout.addWidget(button_box)

    # ======================================================================
    # Layouts methods (create the component sub layouts)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_language_layout
    # Description: Create the language layout
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_language_layout(self) -> QVBoxLayout:
        """
        Create the language layout that contains the language label, combo
        box and error message label.

        It iterates over the i18n directory to get the available languages
        and add them to the combo box. The current language is selected by
        default (stored in the config file).
        """
        # Language layout
        language_layout: QVBoxLayout = QVBoxLayout()

        # Get available languages from i18n directory
        i18n_dir: Path = self._config.i18n_directory
        languages: List[str] = [lang.stem for lang in i18n_dir.glob("*.yaml")]

        # Create a combo box with the available views
        lang_label: QLabel = QLabel(
            self._translator.text("settings_dialog.language.label")
        )
        self.language_combo: QComboBox = QComboBox()

        for lang in languages:
            self.language_combo.addItem(self._translator.text(lang), lang)

        # Set the current language
        current_lang: str = self._config.current_config_file_user_settings.get(
            SETTING_LANGUAGE, None
        )
        assert (
            current_lang is not None or current_lang == ""
        ), f"Error getting current language from configuration"

        index: int = self.language_combo.findData(current_lang)
        self.language_combo.setCurrentIndex(index)

        # Error message label
        self.error_language_label: QLabel = QLabel()
        self.error_language_label.setObjectName("error_label")
        self.error_language_label.setWordWrap(True)
        self.error_language_label.setHidden(True)

        # Add the widgets to the layout
        language_layout.addWidget(lang_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addWidget(self.error_language_label)
        language_layout.setContentsMargins(0, 0, 0, 0)

        return language_layout

    # ---------------------------------------------------------------------
    # Method     : create_default_repository_layout
    # Description: Create the default repository layout
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def create_default_repository_layout(self) -> QVBoxLayout:
        """
        Create the default repository layout that contains the default
        repository label, checkbox, directory edit and error message label.
        """
        # Default repository layout
        default_repository_layout: QVBoxLayout = QVBoxLayout()

        # Default repository label
        default_repository_label: QLabel = QLabel(
            self._translator.text("settings_dialog.default_repository.label")
        )

        # Default repository checkbox
        self.default_repository_checkbox: QCheckBox = QCheckBox(
            self._translator.text("settings_dialog.default_repository.checkbox")
        )
        using_default_repository: bool
        current_repository: str = self._config.current_config_file_user_settings.get(
            SETTING_ARCHETYPE_REPOSITORY, None
        )

        assert (
            current_repository is not None
        ), f"Error getting current repository from configuration"

        # If the current repository is the default one, check the checkbox
        if current_repository == "":
            using_default_repository = True
        else:
            using_default_repository = False

        self.default_repository_checkbox.setChecked(using_default_repository)

        # Directory edit
        self.default_repository_edit: DirectoryEdit = DirectoryEdit()
        # If it is not using the default repository, set the directory
        self.default_repository_edit.setEnabled(not using_default_repository)
        if not using_default_repository:
            self.default_repository_edit.setDirectory(current_repository)

        # Error message label
        self.error_default_repository_label: QLabel = QLabel()
        self.error_default_repository_label.setObjectName("error_label")
        self.error_default_repository_label.setWordWrap(True)
        self.error_default_repository_label.setHidden(True)

        # Connect checkbox signal to the directory edit setEnabled
        # NOTE: 2 is the state of the checkbox when it is checked
        self.default_repository_checkbox.stateChanged.connect(
            lambda state: self.default_repository_edit.setEnabled(not state == 2)
        )

        # Add the widgets to the layout
        default_repository_layout.addWidget(default_repository_label)
        default_repository_layout.addWidget(self.default_repository_checkbox)
        default_repository_layout.addWidget(self.default_repository_edit)
        default_repository_layout.addWidget(self.error_default_repository_label)
        default_repository_layout.setContentsMargins(0, 0, 0, 0)

        return default_repository_layout

    # ======================================================================
    # Validators
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : validate_language
    # Description: Validate the language
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate_language(self) -> bool:
        """
        Validate if the language input is correct. It checks if the language
        is in the available languages list.

        It shows an error message if the language is not correct. Otherwise,
        it hides the error message if it was shown before.

        :return: True if the language is correct, False otherwise
        """
        language: str = self.language_combo.currentData()
        if language is None or language == "":
            self.error_language_label.setText(
                self._translator.text("settings_dialog.error.invalid_language")
            )
            self.error_language_label.setHidden(False)
            return False

        self.error_language_label.setHidden(True)
        return True

    # ---------------------------------------------------------------------
    # Method     : validate_default_repository
    # Description: Validate the default repository
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def validate_default_repository(self) -> bool:
        """
        Validate if the default repository input is correct. It checks if the
        path exists and if it is a valid repository.

        It shows an error message if the path is not correct. Otherwise,
        it hides the error message if it was shown before.

        :return: True if the path is correct, False otherwise
        """
        default_repository: bool = self.default_repository_checkbox.isChecked()
        repository_path: str = self.default_repository_edit.directory()

        # If it is using custom repository, check if it is correct
        if not default_repository:
            # Check if the path is empty
            if repository_path == "":
                self.error_default_repository_label.setText(
                    self._translator.text("settings_dialog.error.repository.empty_path")
                )
                self.error_default_repository_label.setHidden(False)
                return False

            # Check if the path exists
            _repo_path: Path = Path(repository_path)
            if not _repo_path.exists():
                self.error_default_repository_label.setText(
                    self._translator.text(
                        "settings_dialog.error.repository.invalid_path"
                    )
                )
                self.error_default_repository_label.setHidden(False)
                return False

            # Check if it is a valid repository using ArchetypeManager
            try:
                ArchetypeManager.load_object_archetypes(_repo_path)
                ArchetypeManager.load_document_archetypes(_repo_path)
                ArchetypeManager.load_project_archetypes(_repo_path)
            except Exception as e:
                log.error(f"Error loading custom archetypes from repository: {e}")
                self.error_default_repository_label.setText(
                    self._translator.text(
                        "settings_dialog.error.repository.invalid_repository"
                    )
                )
                self.error_default_repository_label.setHidden(False)
                return False

        # If we reach this point, there are no errors
        self.error_language_label.setHidden(True)
        return True

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
    def save_button_clicked(self) -> None:
        """
        Manage the save button clicked event. It saves the current settings
        """
        # ---------------------
        # Validate settings
        # ---------------------
        valid_settings: bool = True
        valid_settings = self.validate_language() and valid_settings
        valid_settings = self.validate_default_repository() and valid_settings

        # If there are errors, do not save the settings
        if not valid_settings:
            return

        # ---------------------
        # Store validated settings
        # ---------------------
        settings: Dict[str, str] = {}

        # Store language
        language: str = self.language_combo.currentData()
        settings[SETTING_LANGUAGE] = language

        # Store default repository
        default_repository: bool = self.default_repository_checkbox.isChecked()
        repository_path: str = ""
        # If it is not using the default repository, store the path
        if not default_repository:
            repository_path = self.default_repository_edit.directory()
        settings[SETTING_ARCHETYPE_REPOSITORY] = str(repository_path)

        # ---------------------
        # Save settings
        # ---------------------
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
        dialog = SettingsDialog(controller=controller)
        dialog.exec()
        return dialog
