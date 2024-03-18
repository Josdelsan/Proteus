# ==========================================================================
# File: app_settings.py
# Description: PROTEUS app settings module
# Date: 15/03/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
import shutil
from pathlib import Path
from dataclasses import dataclass, replace
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

CONFIG_FILE: str = "proteus.ini"

# Directories
DIRECTORIES: str = "directories"
BASE_DIRECTORY: str = "base_directory"
RESOURCES_DIRECTORY: str = "resources_directory"
ICONS_DIRECTORY: str = "icons_directory"
I18N_DIRECTORY: str = "i18n_directory"
DEFAULT_PROFILE_DIRECTORY: str = "default_profile_directory"

# User editable settings
SETTINGS: str = "settings"
SETTING_LANGUAGE: str = "language"
SETTING_DEFAULT_VIEW: str = "default_view"
SETTING_DEFAULT_ARCHETYPE_REPOSITORY: str = "selected_archetype_repository"
SETTING_USING_DEFAULT_PROFILE: str = "using_default_profile"
SETTING_CUSTOM_PROFILE_PATH: str = "custom_profile_path"


# logging configuration
log = logging.getLogger(__name__)


@dataclass
class AppSettings:
    """
    Store app settings located in the app configuration file.
    """

    # General purpose variables
    app_path: Path = None
    settings_file_path: Path = None
    config_parser: ConfigParser = None

    # Directory settings (not editable by the user)
    base_directory: Path = None
    resources_directory: Path = None
    icons_directory: Path = None
    i18n_directory: Path = None
    default_profile_directory: Path = None

    # Application settings (User editable settings)
    language: str = None
    default_view: str = None
    default_archetype_repository: str = None
    using_default_profile: bool = None
    custom_profile_path: Path = None

    # --------------------------------------------------------------------------
    # Method: load
    # Description: Load user settings from the configuration file
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @staticmethod
    def load(app_path: Path) -> "AppSettings":
        """
        Loads the user/app settings from the configuration file located in the
        app directory. If the cwd is different from the app directory, creates
        a copy of the configuration file in the cwd and loads the settings from
        it.
        """
        config_file_path: Path = app_path / CONFIG_FILE

        assert (
            config_file_path.exists()
        ), f"PROTEUS configuration file {CONFIG_FILE} does not exist in {app_path}!"

        # Check for proteus.ini file where the application is executed
        # NOTE: This allows to change config in single executable app version
        config_file_exec_path: Path = Path.cwd() / CONFIG_FILE
        if not config_file_exec_path.exists():
            log.warning(
                f"PROTEUS configuration file {CONFIG_FILE} does not exist in the execution path. Copying configuration file to execution path..."
            )

            # Copy proteus.ini file to execution path
            shutil.copy(config_file_path, config_file_exec_path)

        config_parser: ConfigParser = ConfigParser()
        config_parser.read(config_file_exec_path)

        # Variable to store init file path
        # This is required to avoid loosing track if cwd changes
        settings_file_path: Path = config_file_exec_path

        log.info(f"Loading settings from {settings_file_path}...")

        app_settings = AppSettings(
            app_path=app_path,
            settings_file_path=settings_file_path,
            config_parser=config_parser,
        )

        app_settings._load_directories()
        app_settings._load_user_settings()

        return app_settings

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

        self.base_directory = self.app_path / directories[BASE_DIRECTORY]
        self.resources_directory = self.app_path / directories[RESOURCES_DIRECTORY]
        self.icons_directory = self.resources_directory / directories[ICONS_DIRECTORY]
        self.i18n_directory = self.resources_directory / directories[I18N_DIRECTORY]
        self.default_profile_directory = (
            self.app_path / directories[DEFAULT_PROFILE_DIRECTORY]
        )

        assert (
            self.base_directory.exists()
        ), f"PROTEUS base directory {self.base_directory} does not exist!"
        assert (
            self.resources_directory.exists()
        ), f"PROTEUS resources directory {self.resources_directory} does not exist!"
        assert (
            self.icons_directory.exists()
        ), f"PROTEUS icons directory {self.icons_directory} does not exist!"
        assert (
            self.i18n_directory.exists()
        ), f"PROTEUS i18n directory {self.i18n_directory} does not exist!"
        assert (
            self.default_profile_directory.exists()
        ), f"PROTEUS default profile directory {self.default_profile_directory} does not exist!"

        log.info(f"Directories loaded from {self.settings_file_path}.")
        log.info(f"{self.base_directory = }")
        log.info(f"{self.resources_directory = }")
        log.info(f"{self.icons_directory = }")
        log.info(f"{self.i18n_directory = }")
        log.info(f"{self.default_profile_directory = }")

    # --------------------------------------------------------------------------
    # Method: _load_user_settings
    # Description: Load user editable settings from the configuration file
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_user_settings(self) -> None:
        """
        Load user editable settings from the configuration file.
        """
        # Settings section
        settings = self.config_parser[SETTINGS]

        # Language -----------------------
        self.language = settings[SETTING_LANGUAGE]

        log.info(f"Config file {self.settings_file_path} | Language: {self.language}")

        # Default view -------------------
        self.default_view = settings[SETTING_DEFAULT_VIEW]

        log.info(
            f"Config file {self.settings_file_path} | Default view: {self.default_view}"
        )

        # Default archetype repository -------------------
        self.default_archetype_repository = settings[
            SETTING_DEFAULT_ARCHETYPE_REPOSITORY
        ]

        log.info(
            f"Config file {self.settings_file_path} | Default archetype repository: {self.default_archetype_repository}"
        )

        # Profile ------------------------
        using_default_profile_str: str = settings[SETTING_USING_DEFAULT_PROFILE]
        using_default_profile: bool = using_default_profile_str.lower() == "true"
        self.using_default_profile = using_default_profile

        custom_profile_path_str: str = settings[SETTING_CUSTOM_PROFILE_PATH]
        if custom_profile_path_str and not using_default_profile:
            custom_profile_path = Path(custom_profile_path_str)

            if custom_profile_path.exists():
                self.custom_profile_path = custom_profile_path
            else:
                log.warning(
                    f"Custom profile path {custom_profile_path} does not exist. Using default profile..."
                )
                self.using_default_profile = True

        log.info(
            f"Loaded app user settings from {self.settings_file_path}."
        )
        log.info(f"{self.language = }")
        log.info(f"{self.default_archetype_repository = }")
        log.info(f"{self.default_view = }")
        log.info(f"{self.using_default_profile = }")
        log.info(f"{self.custom_profile_path = }")


    # --------------------------------------------------------------------------
    # Method: clone
    # Description: Clone the current object with the new user settings (if any)
    # Date: 18/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def clone(
        self,
        language: str = None,
        default_view: str = None,
        default_archetype_repository: str = None,
        using_default_profile: bool = None,
        custom_profile_path: Path = None,
    ) -> "AppSettings":
        """
        Clone the current object with the new user settings (if any).
        """
        if language is None:
            language = self.language

        if default_view is None:
            default_view = self.default_view

        if default_archetype_repository is None:
            default_archetype_repository = self.default_archetype_repository

        if using_default_profile is None:
            using_default_profile = self.using_default_profile

        if custom_profile_path is None:
            custom_profile_path = self.custom_profile_path

        return replace(
            self,
            language=language,
            default_view=default_view,
            default_archetype_repository=default_archetype_repository,
            using_default_profile=using_default_profile,
            custom_profile_path=custom_profile_path,
        )

    # --------------------------------------------------------------------------
    # Method: save
    # Description: Save the current settings to the configuration file
    # Date: 18/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def save(self) -> None:
        """
        Save the current settings to the configuration file.
        """
        # Settings section
        self.config_parser[SETTINGS][SETTING_LANGUAGE] = self.language
        self.config_parser[SETTINGS][SETTING_DEFAULT_VIEW] = self.default_view
        self.config_parser[SETTINGS][
            SETTING_DEFAULT_ARCHETYPE_REPOSITORY
        ] = self.default_archetype_repository
        self.config_parser[SETTINGS][SETTING_USING_DEFAULT_PROFILE] = str(
            self.using_default_profile
        )
        self.config_parser[SETTINGS][SETTING_CUSTOM_PROFILE_PATH] = str(
            self.custom_profile_path
        )

        with open(self.settings_file_path, "w") as config_file:
            self.config_parser.write(config_file)

        log.info(f"Settings saved to {self.settings_file_path}.")
        log.info(f"{self.language = }")
        log.info(f"{self.default_view = }")
        log.info(f"{self.default_archetype_repository = }")
        log.info(f"{self.using_default_profile = }")
        log.info(f"{self.custom_profile_path = }")
        
