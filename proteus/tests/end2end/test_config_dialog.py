# ==========================================================================
# File: test_config_dialog.py
# Description: pytest file for the PROTEUS pyqt config fialog
# Date: 29/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from copy import deepcopy

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtWidgets import QDialogButtonBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.application.resources.translator import Translator
from proteus.application.configuration.config import Config
from proteus.application.configuration.app_settings import AppSettings
from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.settings_dialog import SettingsDialog
from proteus.tests.end2end.fixtures import app, get_dialog

# --------------------------------------------------------------------------
# Fixtures / Helper functions
# --------------------------------------------------------------------------


@pytest.fixture(scope="function")
def app_settings():
    """
    Return app settings and restore them after the test. Restoration is done
    by saving the settings (not app_settings_copy).
    """
    # Config singleton
    config = Config()

    # Return settings
    yield config.app_settings

    # Restore settings
    config.app_settings.save()


# # --------------------------------------------------------------------------
# # End to end "config dialog" tests
# # --------------------------------------------------------------------------


def test_config_dialog_open(app, app_settings: AppSettings):
    """
    Opens the config dialog and checks if the settings are correctly
    loaded.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    # Get config button
    settings_button = main_window.main_menu.settings_button

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Open config dialog
    dialog: SettingsDialog = get_dialog(settings_button.click)

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check if dialog was created correctly
    assert isinstance(
        dialog, SettingsDialog
    ), f"Dialog is not an instance of SettingsDialog but {type(dialog)}"

    # Check language setting was correctly set in the combo box
    current_language = dialog.language_combo.currentData()

    assert (
        current_language == app_settings.language
    ), f"Language setting is {current_language} but should be {app_settings.language}"

    # Check default view setting was correctly set in the combo box
    current_default_view = dialog.default_view_combo.currentData()

    assert (
        current_default_view == app_settings.default_view
    ), f"Default view setting is {current_default_view} but should be {app_settings.default_view}"

    # Check selected profile setting was correctly set in the combo box
    current_selected_profile = dialog.profile_combo.currentData()

    assert (
        current_selected_profile == app_settings.selected_profile
    ), f"Selected profile setting is {current_selected_profile} but should be {app_settings.selected_profile}"

    # Check using_default_profile setting was correctly set in the checkbox
    current_using_default_profile = dialog.default_profile_checkbox.isChecked()

    assert (
        current_using_default_profile == app_settings.using_default_profile
    ), f"Using default profile setting is {current_using_default_profile} but should be {app_settings.using_default_profile}"

    # Check custom_profile_path setting was correctly set in directory edit and checkbox
    current_custom_profile_path = dialog.custom_profile_edit.directory()

    custom_profile_path = app_settings.custom_profile_path.as_posix() if app_settings.custom_profile_path else ""

    assert (
        current_custom_profile_path == custom_profile_path
    ), f"Custom profile path setting is {current_custom_profile_path} but should be {app_settings.custom_profile_path}"


def test_config_dialog_change_settings(app, app_settings: AppSettings):
    """
    Opens the config dialog and changes the settings. Then checks if
    the settings were correctly changed (file and dialog).

    app_settings fixture is used to restore the settings file to its
    original state. It also works when the test fails.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    # Get config button
    settings_button = main_window.main_menu.settings_button

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Change settings
    new_language = "es_ES"
    new_default_view = "figures"

    # Open config dialog
    dialog: SettingsDialog = get_dialog(settings_button.click)

    # Change language
    new_lang_index = dialog.language_combo.findData(new_language)
    dialog.language_combo.setCurrentIndex(new_lang_index)

    # Change default view
    new_default_view_index = dialog.default_view_combo.findData(new_default_view)
    dialog.default_view_combo.setCurrentIndex(new_default_view_index)

    # Save settings
    dialog.accept_button.click()
    dialog.deleteLater()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # ---------------------
    # Check dialog
    # ---------------------

    # Open again the config dialog and check if the settings were correctly changed
    second_dialog: SettingsDialog = get_dialog(settings_button.click)

    # Check language setting was correctly set in the combo box
    current_language = second_dialog.language_combo.currentData()

    assert (
        current_language == new_language
    ), f"Language setting is {current_language} but should be {new_language}"

    # Check default view setting was correctly set in the combo box
    current_default_view = second_dialog.default_view_combo.currentData()

    assert (
        current_default_view == new_default_view
    ), f"Default view setting is {current_default_view} but should be {new_default_view}"


    # ---------------------
    # Check file
    # ---------------------

    # Read settings file and check if the setting were correctly changed
    # Creates config parser using Config to make code easier
    new_app_settings = AppSettings.load(proteus.PROTEUS_APP_PATH)

    app_settings_copy = Config().app_settings_copy

    # Check language setting
    assert (
        new_app_settings.language == new_language == app_settings_copy.language
    ), f"Language settings was not correctly saved. It is {new_app_settings.language} but should be {new_language} | {app_settings_copy.language}"

    # Check default view setting
    assert (
        new_app_settings.default_view == new_default_view == app_settings_copy.default_view
    ), f"Default view settings was not correctly saved. It is {new_app_settings.default_view} but should be {new_default_view} | {app_settings_copy.default_view}"
