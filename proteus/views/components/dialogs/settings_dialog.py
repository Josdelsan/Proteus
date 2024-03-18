# ==========================================================================
# File: settings_dialog.py
# Description: PyQT6 settings dialog component for the PROTEUS application
# Date: 18/03/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List
from pathlib import Path
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QGroupBox,
)


# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.application.configuration.config import Config
from proteus.application.configuration.profile_settings import ProfileSettings
from proteus.controller.command_stack import Controller
from proteus.application.resources.icons import Icons, ProteusIconType
from proteus.application.resources.translator import Translator
from proteus.views.forms.directory_edit import DirectoryEdit
from proteus.views.components.dialogs.base_dialogs import ProteusDialog


# Module configuration
log = logging.getLogger(__name__)
_ = Translator().text  # Translator


# --------------------------------------------------------------------------
# Class: SettingsDialog
# Description: PyQT6 settings dialog component for the PROTEUS application
# Date: 18/03/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class SettingsDialog(ProteusDialog):
    """
    Settings dialog component class for the PROTEUS application. It provides a
    dialog form to change the application settings.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 18/03/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Create properties to store the new document data.
        """
        super(SettingsDialog, self).__init__(*args, **kwargs)

        # Settings edit widgets
        self.language_combo: QComboBox = None
        self.view_combo: QComboBox = None
        self.default_repository_combo: QComboBox = None

        self.custom_profile_edit: DirectoryEdit = None
        self.default_profile_checkbox: QCheckBox = None

        # Error message labels
        self.error_profile_label: QLabel = None

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component
    # Date       : 18/03/2024
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
        proteus_icon = Icons().icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(proteus_icon)

        # Connect the buttons to the slots
        self.accept_button.setText(_("dialog.save_button"))
        self.accept_button.clicked.connect(self.save_button_clicked)
        self.reject_button.clicked.connect(self.cancel_button_clicked)

        # Setting message label
        setting_info_label: QLabel = QLabel(_("settings_dialog.info.label"))
        setting_info_label.setStyleSheet("font-weight: bold")

        # -------------------------------------------
        # Layouts
        # -------------------------------------------
        layout: QVBoxLayout = QVBoxLayout()

        # Specific settings group boxes
        language_box: QGroupBox = self.create_language_box()
        profile_box: QGroupBox = self.create_profile_box()
        profile_specific_settings: QGroupBox = (
            self.create_profile_specific_settings_box()
        )

        # Add the widgets to the layout
        layout.addWidget(setting_info_label)
        layout.addWidget(language_box)
        layout.addWidget(profile_specific_settings)
        layout.addWidget(profile_box)
        layout.addStretch()

        self.set_content_layout(layout)

    # ======================================================================
    # Layouts methods (create the component sub layouts)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_language_box
    # Description: Create the language group box
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_language_box(self) -> QGroupBox:
        """
        Create the language group box that contains the language combo box.

        Available languages are obtained from the translator instance.
        """
        # Language layout
        language_layout: QVBoxLayout = QVBoxLayout()

        # Get available languages from translator instance
        languages: List[str] = Translator().available_languages

        # Create a combo box with the available views
        self.language_combo: QComboBox = QComboBox()

        for lang in languages:
            self.language_combo.addItem(
                _(f"settings.language.{lang}", alternative_text=lang),
                lang,
            )

        # Set the current language
        current_lang: str = Config().app_settings_copy.language

        assert (
            current_lang is not None or current_lang == ""
        ), f"Error getting current language from configuration"

        index: int = self.language_combo.findData(current_lang)
        self.language_combo.setCurrentIndex(index)

        # Add the widgets to the layout
        language_layout.addWidget(self.language_combo)

        # Group box
        language_group: QGroupBox = QGroupBox(_("settings_dialog.language.group"))
        language_group.setLayout(language_layout)

        return language_group

    # ---------------------------------------------------------------------
    # Method     : create_profile_box
    # Description: Create the profile group box
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def create_profile_box(self) -> QGroupBox:
        """
        Create the repository group box that contains the profile settings
        (default or custom profile path)
        """
        profile_layout: QVBoxLayout = QVBoxLayout()

        self.default_profile_checkbox: QCheckBox = QCheckBox(
            _("settings_dialog.default_profile.checkbox")
        )
        custom_profile_path: Path = Config().app_settings_copy.custom_profile_path
        custom_profile_dir_str: str
        if custom_profile_path is None:
            custom_profile_dir_str = ""
        else:
            custom_profile_dir_str = custom_profile_path.as_posix()

        using_default_profile: bool = Config().app_settings_copy.using_default_profile

        self.default_profile_checkbox.setChecked(using_default_profile)

        # Directory edit
        self.custom_profile_edit: DirectoryEdit = DirectoryEdit()
        self.custom_profile_edit.setEnabled(not using_default_profile)
        self.custom_profile_edit.setDirectory(custom_profile_dir_str)

        # Error message label
        self.error_profile_label: QLabel = QLabel()
        self.error_profile_label.setObjectName("error_label")
        self.error_profile_label.setWordWrap(True)
        self.error_profile_label.setHidden(True)

        # Connect checkbox signal to the directory edit and combo setEnabled
        # NOTE: 2 is the state of the checkbox when it is checked
        self.default_profile_checkbox.stateChanged.connect(
            lambda state: self.custom_profile_edit.setEnabled(not state == 2)
        )

        # Add the widgets to the layout
        profile_layout.addWidget(self.default_profile_checkbox)
        profile_layout.addWidget(self.custom_profile_edit)
        profile_layout.addWidget(self.error_profile_label)

        # Group box
        profile_group: QGroupBox = QGroupBox(
            _("settings_dialog.default_profile.group")
        )
        profile_group.setLayout(profile_layout)

        return profile_group

    # ---------------------------------------------------------------------
    # Method     : create_profile_specific_settings_box
    # Description: Create the profile specific settings group box
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def create_profile_specific_settings_box(self) -> QGroupBox:
        """
        Create the profile specific settings group box that contains the
        the selected default view and the selected archetype repository.
        """
        # View layout
        layout: QVBoxLayout = QVBoxLayout()

        # Default view -------------------------------------
        default_view_label: QLabel = QLabel(_("settings_dialog.default_view.label"))
        self.default_view_combo: QComboBox = QComboBox()
        for view_name in self._controller.get_available_xslt():
            self.default_view_combo.addItem(
                _(f"xslt_templates.{view_name}", alternative_text=view_name),
                view_name,
            )

        # Set the current view
        current_default_view: str = Config().app_settings_copy.default_view
        index: int = self.default_view_combo.findData(current_default_view)
        self.default_view_combo.setCurrentIndex(index)

        # Selected repository -------------------------------------
        default_repository_label: QLabel = QLabel(
            _("settings_dialog.default_repository.label")
        )

        # Default repository combo
        self.default_repository_combo: QComboBox = QComboBox()
        for repository in Config().profile_settings.listed_archetype_repositories:
            self.default_repository_combo.addItem(
                _(f"settings.repository.{repository}", alternative_text=repository),
                repository,
            )
            self.default_repository_combo.setItemIcon(
                self.default_repository_combo.count() - 1,
                Icons().icon(ProteusIconType.Repository, repository),
            )

        current_default_repository: str = Config().app_settings_copy.default_archetype_repository

        self.default_repository_combo.setCurrentIndex(
            self.default_repository_combo.findData(current_default_repository)
        )

        # Add the widgets to the layout
        layout.addWidget(default_view_label)
        layout.addWidget(self.default_view_combo)
        layout.addWidget(default_repository_label)
        layout.addWidget(self.default_repository_combo)

        # Group box
        group: QGroupBox = QGroupBox(
            _("settings_dialog.profile_settings.group")
        )
        group.setLayout(layout)

        return group

    # ======================================================================
    # Validators
    # ======================================================================

    # ---------------------------------------------------------------------
    # Method     : validate_profile
    # Description: Validate the selected profile
    # Date       : 25/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def validate_repository(self) -> bool:
        """
        Validate if the custom profile can be loaded from the selected path.

        :return: True if the profile can be loaded, False otherwise
        """
        default_profile: bool = self.default_profile_checkbox.isChecked()
        profile_path: str = self.custom_profile_edit.directory()

        # If it is using custom repository, check if it is correct
        if not default_profile:
            # Check if the path is empty
            if profile_path == "":
                self.error_profile_label.setText(
                    _("settings_dialog.error.profile.empty_path")
                )
                self.error_profile_label.setHidden(False)
                return False

            # Check if the path exists
            _profile_path: Path = Path(profile_path)
            if not _profile_path.exists():
                self.error_profile_label.setText(
                    _("settings_dialog.error.profile.invalid_path")
                )
                self.error_profile_label.setHidden(False)
                return False

            # Check if it is a valid profile using profile settings loader
            try:
                ProfileSettings.load(_profile_path)
            except Exception as e:
                log.error(f"Error loading custom profile from path {_profile_path} error: {e}")
                self.error_profile_label.setText(
                    _("settings_dialog.error.profile.invalid_profile", e)
                )
                self.error_profile_label.setHidden(False)
                return False

        # If we reach this point, there are no errors
        self.error_profile_label.setHidden(True)
        return True

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Save button clicked event handler
    # Date       : 18/03/2024
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
        valid_settings = self.validate_repository() and valid_settings

        # If there are errors, do not save the settings
        if not valid_settings:
            return

        # ---------------------
        # Store validated settings
        # ---------------------

        config = Config()

        config.app_settings_copy = config.app_settings_copy.clone(
            language=self.language_combo.currentData(),
            default_view=self.default_view_combo.currentData(),
            using_default_profile=self.default_profile_checkbox.isChecked(),
            default_archetype_repository=self.default_repository_combo.currentData(),
            custom_profile_path=self.custom_profile_edit.directory(),
        )

        # ---------------------
        # Save settings
        # ---------------------
        config.app_settings_copy.save()

        # Close the form window
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Cancel button clicked event handler
    # Date       : 18/03/2024
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
    # Date       : 18/03/2024
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
