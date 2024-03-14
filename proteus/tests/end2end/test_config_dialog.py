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

from proteus.utils.translator import Translator
from proteus.utils.config import (
    Config,
    SETTINGS,
    SETTING_LANGUAGE,
    SETTING_CUSTOM_ARCHETYPE_REPOSITORY,
    SETTING_DEFAULT_ARCHETYPE_REPOSITORY,
    SETTING_USING_CUSTOM_REPOSITORY,
)
from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.settings_dialog import SettingsDialog
from proteus.tests.end2end.fixtures import app, get_dialog

# --------------------------------------------------------------------------
# Fixtures / Helper functions
# --------------------------------------------------------------------------


@pytest.fixture(scope="function")
def file_settings():
    """
    Reads the settings file and returns its content as a dictionary. Then
    the content is overwritten with the previously read values to restore
    in case of failure.

    Uses the Config singleton to read the settings file and restore it.
    """
    # Config singleton
    config = Config()

    # Get settings from Config (copy settings var)
    settings = deepcopy(config.settings)

    # Return settings
    yield settings

    # Restore settings
    config.save_user_settings(settings)


# --------------------------------------------------------------------------
# End to end "config dialog" tests
# --------------------------------------------------------------------------


def test_config_dialog_open(app, file_settings):
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
        current_language == file_settings[SETTING_LANGUAGE]
    ), f"Language setting is {current_language} but should be {file_settings[SETTING_LANGUAGE]}"

    # Check default archetype repository setting was correctly set in directory edit and checkbox
    current_default_repository = dialog.default_repository_combo.currentData()

    assert (
        current_default_repository
        == file_settings[SETTING_DEFAULT_ARCHETYPE_REPOSITORY]
    ), f"Default repository setting is {current_default_repository} but should be {file_settings[SETTING_DEFAULT_ARCHETYPE_REPOSITORY]}"

    # Check the using custom repository setting was correctly set in the checkbox (unchecked)
    current_using_custom_repository = not dialog.default_repository_checkbox.isChecked()
    using_custom_repository_setting = (
        file_settings[SETTING_USING_CUSTOM_REPOSITORY] == "True"
    )

    assert (
        current_using_custom_repository == using_custom_repository_setting
    ), f"Using custom repository setting is {current_using_custom_repository} but should be {file_settings[SETTING_USING_CUSTOM_REPOSITORY]}"

    # Check custom archetype repository setting was correctly set in directory edit and checkbox
    current_archetype_repository = dialog.custom_repository_edit.directory()

    assert (
        current_archetype_repository
        == file_settings[SETTING_CUSTOM_ARCHETYPE_REPOSITORY]
    ), f"Archetype repository setting is {current_archetype_repository} but should be {file_settings[SETTING_CUSTOM_ARCHETYPE_REPOSITORY]}"

    # Check combo and text edit are enabled/disabled correctly
    if current_using_custom_repository:
        assert (
            dialog.custom_repository_edit.isEnabled() is True
        ), "Default repository directory edit should be enabled"

        assert (
            dialog.default_repository_combo.isEnabled() is False
        ), "Default repository combo should be disabled"
    else:
        assert (
            dialog.custom_repository_edit.isEnabled() is False
        ), "Default repository directory edit should be disabled"

        assert (
            dialog.default_repository_combo.isEnabled() is True
        ), "Default repository combo should be enabled"


def test_config_dialog_change_settings(app, file_settings):
    """
    Opens the config dialog and changes the settings. Then checks if
    the settings were correctly changed (file and dialog).

    file_settings fixture is used to restore the settings file to its
    original state. It also works when the test fails.

    NOTE: The archetype repository setting will be change to use a
    custom route but pointing to the built-in archetypes directory.
    This is done to avoid validation errors.
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
    new_archetype_repository = Config().current_archetype_repository.as_posix()

    # Open config dialog
    dialog: SettingsDialog = get_dialog(settings_button.click)

    # Change language
    new_lang_index = dialog.language_combo.findData(new_language)
    dialog.language_combo.setCurrentIndex(new_lang_index)

    # Change archetype repository
    dialog.default_repository_checkbox.setChecked(False)
    dialog.custom_repository_edit.setDirectory(new_archetype_repository)

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

    # Check archetype repository setting was correctly set in directory edit and checkbox
    current_archetype_repository = second_dialog.custom_repository_edit.directory()

    assert (
        current_archetype_repository == new_archetype_repository
    ), f"Archetype repository setting is {current_archetype_repository} but should be {new_archetype_repository}"

    assert (
        second_dialog.custom_repository_edit.isEnabled() is True
    ), "Default repository directory edit should be enabled"

    assert (
        second_dialog.default_repository_checkbox.isChecked() is False
    ), "Default repository checkbox should not be checked"

    # ---------------------
    # Check file
    # ---------------------

    # Read settings file and check if the setting were correctly changed
    # Creates config parser using Config to make code easier
    config_parser = Config()._create_config_parser()
    settings = config_parser[SETTINGS]

    # Check language setting
    assert (
        settings[SETTING_LANGUAGE] == new_language
    ), f"Language setting is {settings[SETTING_LANGUAGE]} but should be {new_language}"

    # Check archetype repository setting
    assert (
        settings[SETTING_CUSTOM_ARCHETYPE_REPOSITORY] == new_archetype_repository
    ), f"Archetype repository setting is {settings[SETTING_CUSTOM_ARCHETYPE_REPOSITORY]} but should be {new_archetype_repository}"
