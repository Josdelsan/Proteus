# ==========================================================================
# File: profile_settings.py
# Description: PROTEUS profile settings module
# Date: 15/03/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import List
from pathlib import Path
from dataclasses import dataclass
from configparser import ConfigParser

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

CONFIG_FILE: str = "profile.ini"

# Directories
DIRECTORIES: str = "directories"
PLUGINS_DIRECTORY: str = "plugins_directory"
ARCHETYPES_DIRECTORY: str = "archetypes_directory"
XSLT_DIRECTORY: str = "xslt_directory"
ICONS_DIRECTORY: str = "icons_directory"
I18N_DIRECTORY: str = "i18n_directory"

# User editable settings
SETTINGS: str = "settings"
SETTING_DEFAULT_VIEW: str = "default_view"
SETTING_DEFAULT_ARCHETYPE_REPOSITORY: str = "selected_archetype_repository"


# logging configuration
log = logging.getLogger(__name__)


@dataclass
class ProfileSettings:
    """
    Store app settings located in the app configuration file.
    """

    # General purpose variables
    profile_path: Path = None
    settings_file_path: Path = None
    config_parser: ConfigParser = None

    # Directory settings (not editable by the user)
    plugins_directory: Path = None
    archetypes_directory: Path = None
    xslt_directory: Path = None
    icons_directory: Path = None
    i18n_directory: Path = None

    # Profile settings
    default_view: str = None
    selected_archetype_repository: str = None

    # Archetype repository path
    # NOTE: This is stored to avoid building the path every time it is needed
    selected_archetype_repository_path: Path = None

    # --------------------------------------------------------------------------
    # Method: load
    # Description: Load user settings from the configuration file
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @staticmethod
    def load(profile_path: Path) -> "ProfileSettings":
        """
        Loads the profile settings from the configuration file located in the
        profile directory. If the file does not exist, error is raised.
        """
        config_file_path: Path = profile_path / CONFIG_FILE

        assert (
            config_file_path.exists()
        ), f"PROTEUS profile configuration file {CONFIG_FILE} does not exist in {profile_path}!"

        config_parser: ConfigParser = ConfigParser()
        config_parser.read(config_file_path)

        settings_file_path: Path = config_file_path

        log.info(f"Loading settings from {settings_file_path}...")

        return ProfileSettings(
            profile_path=profile_path,
            settings_file_path=settings_file_path,
            config_parser=config_parser,
        )

    # --------------------------------------------------------------------------
    # Method: __post_init__
    # Description: Post initialization method
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __post_init__(self) -> None:
        """
        Post initialization method.
        """
        self._load_directories()
        self._load_user_settings()

    # --------------------------------------------------------------------------
    # Method: _load_directories
    # Description: Load directory settings from the configuration file
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_directories(self) -> None:
        """
        Load directory settings from the configuration file.
        """
        # Directories section
        directories = self.config_parser[DIRECTORIES]

        self.archetypes_directory = (
            self.profile_path / directories[ARCHETYPES_DIRECTORY]
        )
        self.xslt_directory = self.profile_path / directories[XSLT_DIRECTORY]
        self.plugins_directory = self.profile_path / directories[PLUGINS_DIRECTORY]
        self.icons_directory = self.profile_path / directories[ICONS_DIRECTORY]
        self.i18n_directory = self.profile_path / directories[I18N_DIRECTORY]

        assert (
            self.archetypes_directory.exists()
        ), f"Archetypes directory {self.archetypes_directory} does not exist in profile {self.profile_path}!"
        assert (
            self.xslt_directory.exists()
        ), f"XSLT directory {self.xslt_directory} does not exist in profile {self.profile_path}!"

        if not directories[PLUGINS_DIRECTORY]:
            log.warning(
                f"Plugins directory {self.plugins_directory} does not exist in profile {self.profile_path}!"
            )

        if not directories[ICONS_DIRECTORY]:
            log.warning(
                f"Icons directory {self.icons_directory} does not exist in profile {self.profile_path}!"
            )

        if not directories[I18N_DIRECTORY]:
            log.warning(
                f"i18n directory {self.i18n_directory} does not exist in profile {self.profile_path}!"
            )

        log.info(f"Directories loaded from {self.settings_file_path}.")
        log.info(f"{self.archetypes_directory = }")
        log.info(f"{self.xslt_directory = }")
        log.info(f"{self.plugins_directory = }")
        log.info(f"{self.icons_directory = }")
        log.info(f"{self.i18n_directory = }")

    # --------------------------------------------------------------------------
    # Method: _load_user_settings
    # Description: Load user editable settings from the configuration file
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    # TODO: Implement archetype repository and XSLT template validation?
    def _load_user_settings(self) -> None:
        """
        Load user editable settings from the configuration file.
        """
        # Settings section
        settings = self.config_parser[SETTINGS]

        # Default view -----------------------
        default_view = settings[SETTING_DEFAULT_VIEW]

        assert (
            default_view is not None and default_view != ""
        ), f"Selected view setting is not defined in {self.settings_file_path}!"

        listed_views: List[str] = [
            e.name for e in self.xslt_directory.iterdir() if e.is_dir()
        ]

        if default_view not in listed_views:
            log.error(
                f"Selected view {default_view} was not found in the XSLT directory. Using first view found instead."
            )
            default_view = listed_views[0]

        self.default_view = default_view

        # Default archetype repository -----------------------
        selected_archetype_repository = settings[SETTING_DEFAULT_ARCHETYPE_REPOSITORY]

        assert (
            selected_archetype_repository is not None
            and selected_archetype_repository != ""
        ), f"Default archetype repository setting is not defined in {self.settings_file_path}!"

        listed_archetype_repositories: List[str] = [
            e.name for e in self.archetypes_directory.iterdir() if e.is_dir()
        ]

        if selected_archetype_repository not in listed_archetype_repositories:
            log.error(
                f"Default archetype repository {selected_archetype_repository} was not found in the archetypes directory. Using first archetype repository found instead."
            )
            selected_archetype_repository = listed_archetype_repositories[0]

        self.selected_archetype_repository = selected_archetype_repository
        self.selected_archetype_repository_path = self.archetypes_directory / selected_archetype_repository
