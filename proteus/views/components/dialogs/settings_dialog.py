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
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QDialogButtonBox,
    QGroupBox,
)


# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.model.archetype_manager import ArchetypeManager
from proteus.utils.config import (
    SETTING_LANGUAGE,
    SETTING_CUSTOM_ARCHETYPE_REPOSITORY,
    SETTING_DEFAULT_ARCHETYPE_REPOSITORY,
    SETTING_USING_CUSTOM_REPOSITORY,
)
from proteus.controller.command_stack import Controller
from proteus.utils import ProteusIconType
from proteus.utils.dynamic_icons import DynamicIcons
from proteus.utils.translator import Translator
from proteus.views.forms.directory_edit import DirectoryEdit
from proteus.views.components.abstract_component import ProteusComponent


# Module configuration
log = logging.getLogger(__name__)
_ = Translator().text  # Translator


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

        # Button box
        self.button_box: QDialogButtonBox = None

        # Settings edit widgets
        self.language_combo: QComboBox = None
        self.custom_repository_edit: DirectoryEdit = None
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
        self.setWindowTitle(_("settings_dialog.title"))

        # Set window icon
        proteus_icon = DynamicIcons().icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(proteus_icon)

        # Create Save and Cancel buttons
        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect the buttons to the slots, combo current text is the view name
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)

        # Setting message label
        setting_info_label: QLabel = QLabel(_("settings_dialog.info.label"))
        setting_info_label.setStyleSheet("font-weight: bold")

        # -------------------------------------------
        # Layouts
        # -------------------------------------------
        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        # Specific settings layouts
        language_layout: QVBoxLayout = self.create_language_layout()
        repository_layout: QVBoxLayout = self.create_repository_layout()

        # Add the widgets to the layout
        layout.addWidget(setting_info_label)
        layout.addLayout(language_layout)
        layout.addLayout(repository_layout)
        layout.addWidget(self.button_box)

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

        # Get available languages from translator instance
        languages: List[str] = Translator().available_languages

        # Create a combo box with the available views
        lang_label: QLabel = QLabel(_("settings_dialog.language.label"))
        self.language_combo: QComboBox = QComboBox()

        for lang in languages:
            self.language_combo.addItem(
                _(f"settings.language.{lang}", alternative_text=lang),
                lang,
            )

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
    # Method     : create_repository_layout
    # Description: Create the repository layout
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def create_repository_layout(self) -> QVBoxLayout:
        """
        Create the repository layout that contains the default repository label,
        combo box, custom repository checkbox, custom repository edit and error
        message label.
        """
        # Default repository layout
        repository_layout: QVBoxLayout = QVBoxLayout()

        # Default repository label
        default_repository_label: QLabel = QLabel(
            _("settings_dialog.default_repository.label")
        )

        # Default repository combo
        self.default_repository_combo: QComboBox = QComboBox()
        for repository in self._config.archetypes_repositories.keys():
            self.default_repository_combo.addItem(
                _(f"settings.repository.{repository}", alternative_text=repository),
                repository,
            )
            self.default_repository_combo.setItemIcon(
                self.default_repository_combo.count() - 1,
                DynamicIcons().icon(ProteusIconType.Repository, repository),
            )

        current_default_repository: str = (
            self._config.current_config_file_user_settings.get(
                SETTING_DEFAULT_ARCHETYPE_REPOSITORY
            )
        )

        self.default_repository_combo.setCurrentIndex(
            self.default_repository_combo.findData(current_default_repository)
        )

        # Use default repository checkbox
        self.default_repository_checkbox: QCheckBox = QCheckBox(
            _("settings_dialog.default_repository.checkbox")
        )
        current_custom_repository: str = (
            self._config.current_config_file_user_settings.get(
                SETTING_CUSTOM_ARCHETYPE_REPOSITORY, None
            )
        )

        using_custom_repository_str: str = (
            self._config.current_config_file_user_settings.get(
                SETTING_USING_CUSTOM_REPOSITORY
            )
        )
        using_custom_repository: bool = using_custom_repository_str == "True"

        self.default_repository_checkbox.setChecked(not using_custom_repository)

        # Directory edit
        self.custom_repository_edit: DirectoryEdit = DirectoryEdit()
        # If it is not using the default repository, set the directory
        self.custom_repository_edit.setEnabled(using_custom_repository)
        self.default_repository_combo.setEnabled(not using_custom_repository)
        self.custom_repository_edit.setDirectory(current_custom_repository)

        # Error message label
        self.error_default_repository_label: QLabel = QLabel()
        self.error_default_repository_label.setObjectName("error_label")
        self.error_default_repository_label.setWordWrap(True)
        self.error_default_repository_label.setHidden(True)

        # Connect checkbox signal to the directory edit and combo setEnabled
        # NOTE: 2 is the state of the checkbox when it is checked
        self.default_repository_checkbox.stateChanged.connect(
            lambda state: self.custom_repository_edit.setEnabled(not state == 2)
        )
        self.default_repository_checkbox.stateChanged.connect(
            lambda state: self.default_repository_combo.setEnabled(state == 2)
        )

        # Add the widgets to the layout
        repository_layout.addWidget(default_repository_label)
        repository_layout.addWidget(self.default_repository_combo)
        repository_layout.addWidget(self.default_repository_checkbox)
        repository_layout.addWidget(self.custom_repository_edit)
        repository_layout.addWidget(self.error_default_repository_label)

        # Group box and wrapper layout
        default_repository_group: QGroupBox = QGroupBox(
            _("settings_dialog.default_repository.group")
        )
        default_repository_group.setLayout(repository_layout)

        wrapper_layout: QVBoxLayout = QVBoxLayout()
        wrapper_layout.addWidget(default_repository_group)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)

        return wrapper_layout

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
                _("settings_dialog.error.invalid_language")
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
    def validate_repository(self) -> bool:
        """
        Validate if the default repository input is correct. It checks if the
        path exists and if it is a valid repository.

        It shows an error message if the path is not correct. Otherwise,
        it hides the error message if it was shown before.

        :return: True if the path is correct, False otherwise
        """
        default_repository: bool = self.default_repository_checkbox.isChecked()
        repository_path: str = self.custom_repository_edit.directory()

        # If it is using custom repository, check if it is correct
        if not default_repository:
            # Check if the path is empty
            if repository_path == "":
                self.error_default_repository_label.setText(
                    _("settings_dialog.error.repository.empty_path")
                )
                self.error_default_repository_label.setHidden(False)
                return False

            # Check if the path exists
            _repo_path: Path = Path(repository_path)
            if not _repo_path.exists():
                self.error_default_repository_label.setText(
                    _("settings_dialog.error.repository.invalid_path")
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
                    _("settings_dialog.error.repository.invalid_repository")
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
        valid_settings = self.validate_repository() and valid_settings

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

        # Store using custom repository
        using_custom_repository: bool = not self.default_repository_checkbox.isChecked()
        settings[SETTING_USING_CUSTOM_REPOSITORY] = str(using_custom_repository)

        # Store default repository
        default_repository: str = self.default_repository_combo.currentData()
        settings[SETTING_DEFAULT_ARCHETYPE_REPOSITORY] = default_repository

        # Store custom repository
        repository_path = self.custom_repository_edit.directory()
        settings[SETTING_CUSTOM_ARCHETYPE_REPOSITORY] = str(repository_path)

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
