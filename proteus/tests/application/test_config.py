# ==========================================================================
# File: test_config.py
# Description: pytest file for the PROTEUS config
# Date: 03/04/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Generator

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import pytest

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_APP_PATH
from proteus.tests import PROTEUS_SAMPLE_CONFIG_PATH
from proteus.application.configuration.app_settings import AppSettings
from proteus.application.configuration.config import Config
from proteus.application.configuration.profile_settings import ProfileSettings

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


@pytest.fixture()
def app_settings(mocker) -> Generator[AppSettings, None, None]:
    mocker.patch("pathlib.Path.cwd", return_value=PROTEUS_SAMPLE_CONFIG_PATH)
    app_settings = AppSettings.load(PROTEUS_APP_PATH)
    app_settings.profiles_directory = (
        PROTEUS_SAMPLE_CONFIG_PATH / "config_test_profiles"
    )
    yield app_settings

    # Clean up
    # This is necessary to avoid errors when running tests in a batch
    Config._instances.pop(Config, None)


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------


def test_config_singleton() -> None:
    config1 = Config()
    config2 = Config()
    assert config1 is config2


def test_config_load_settings_default_profile(mocker, app_settings: AppSettings):
    """
    Test that the config loads a basic setting pattern (default profile selected
    found and selected template is found in profile)
    """
    # ------------------
    # Arrange
    # ------------------
    mocker.patch.object(AppSettings, "load", return_value=app_settings)
    config = Config()

    # ------------------
    # Act
    # ------------------
    config._load_settings()

    # ------------------
    # Assert
    # ------------------
    assert (
        config.app_settings.selected_profile == "dummy_profile"
    ), f"Expected selected profile: 'dummy_profile', Actual: {config.app_settings.selected_profile}"
    assert (
        config.app_settings.default_view == "dummy_view"
    ), f"Expected default view: 'dummy_view', Actual: {config.app_settings.default_view}"
    assert (
        "dummy_profile" in config.listed_profiles.keys()
    ), f"Expected 'dummy_profile' in listed profiles, Actual: {config.listed_profiles}"
    assert (
        config.app_settings.using_default_profile
    ), "Expected using default profile to be True"


def test_config_load_settings_default_profile_default_view_not_found(
    mocker, app_settings: AppSettings
):
    """
    Test that if the default view is not found in the selected profile, the first
    view (xslt template) listed in the profile is selected.
    """
    # ------------------
    # Arrange
    # ------------------
    app_settings.default_view = "non_existent_view"
    mocker.patch.object(AppSettings, "load", return_value=app_settings)
    config = Config()

    # ------------------
    # Act
    # ------------------
    config._load_settings()

    # ------------------
    # Assert
    # ------------------
    assert (
        config.app_settings.selected_profile == "dummy_profile"
    ), f"Expected selected profile: 'dummy_profile', Actual: {config.app_settings.selected_profile}"
    assert (
        config.app_settings.default_view == config.profile_settings.listed_templates[0]
    ) and (
        config.app_settings.default_view != "non_existent_view"
    ), f"Expected default view: '{config.profile_settings.listed_templates[0]}', Actual: {config.app_settings.default_view}"


def test_config_load_settings_default_profile_selected_profile_not_found(
    mocker, app_settings: AppSettings
):
    """
    Test that if the selected profile is not found in the listed profiles, the first
    listed profile is selected.
    """
    # ------------------
    # Arrange
    # ------------------
    app_settings.selected_profile = "non_existent_profile"
    mocker.patch.object(AppSettings, "load", return_value=app_settings)
    config = Config()

    # ------------------
    # Act
    # ------------------
    config._load_settings()

    # ------------------
    # Assert
    # ------------------
    assert (config.app_settings.selected_profile != "non_existent_profile") and (
        config.app_settings.selected_profile == list(config.listed_profiles.keys())[0]
    ), f"Expected selected profile: 'profile_valid_min', Actual: {config.app_settings.selected_profile}"


def test_config_load_settings_custom_profile(mocker, app_settings: AppSettings):
    """
    Test that the config loads settings when a custom profile is selected.
    """
    # ------------------
    # Arrange
    # ------------------
    app_settings.using_default_profile = False
    app_settings.custom_profile_path = (
        PROTEUS_SAMPLE_CONFIG_PATH / "config_test_profiles" / "dummy_profile"
    )
    mocker.patch.object(AppSettings, "load", return_value=app_settings)
    config = Config()

    # ------------------
    # Act
    # ------------------
    config._load_settings()

    # ------------------
    # Assert
    # ------------------
    assert (
        not config.app_settings.using_default_profile
    ), "Expected using default profile to be False"

    assert (
        config.app_settings.custom_profile_path
        == PROTEUS_SAMPLE_CONFIG_PATH / "config_test_profiles" / "dummy_profile"
    ), f"Expected custom profile path: '{PROTEUS_SAMPLE_CONFIG_PATH / 'config_test_profiles' / 'dummy_profile'}', Actual: {config.app_settings.custom_profile_path}"


def test_config_load_settings_custom_profile_not_valid(
    mocker, app_settings: AppSettings
):
    """
    Test that the config loads settings when a custom profile is selected but it is invalid.
    It should fallback to the default profile.
    """
    # ------------------
    # Arrange
    # ------------------
    app_settings.using_default_profile = False
    app_settings.custom_profile_path = (
        PROTEUS_SAMPLE_CONFIG_PATH / "config_test_profiles" / "non_existent_profile"
    )
    mocker.patch.object(AppSettings, "load", return_value=app_settings)
    config = Config()

    # ------------------
    # Act
    # ------------------
    config._load_settings()

    # ------------------
    # Assert
    # ------------------
    assert (
        config.app_settings.using_default_profile
    ), "Expected using default profile to be True"


def test_config_load_settings_default_profile_not_valid(mocker):
    """
    Test that the config loads settings when the default profile is not valid.
    It should raise an exception.
    """
    # ------------------
    # Arrange
    # ------------------

    # Mock ProfileSettings load to raise an exception because if selected profile is not valid
    # load settings will select another one from the listed profiles before

    mocker.patch.object(ProfileSettings, "load", side_effect=AssertionError)

    # ------------------
    # Act/Assert
    # ------------------
    with pytest.raises(AssertionError):
        Config()
