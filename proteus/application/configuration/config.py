# ==========================================================================
# File: config.py
# Description: the config paths for PROTEUS application
# Date: 11/10/2022
# Version: 0.2
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
#         José María Delgado Sánchez
# ==========================================================================
# Update: 22/06/2023 (José María Delgado Sánchez)
# Description:
# - Convert the Config class into a singleton class.
# ==========================================================================
# Update: 20/03/2024 (José María Delgado Sánchez)
# Description:
# - Moved configuration file handling to separate class and reduced class
#   responsibilities.
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
import datetime
from pathlib import Path
from dataclasses import dataclass, replace
import logging
from logging.handlers import TimedRotatingFileHandler

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6 import QtCore

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.application.configuration.app_settings import AppSettings
from proteus.application.configuration.profile_settings import ProfileSettings
from proteus.application.utils.abstract_meta import SingletonMeta
from proteus import PROTEUS_LOGGER_NAME, PROTEUS_LOGGING_DIR, PROTEUS_MAX_LOG_FILES
from proteus.application import (
    RESOURCES_SEARCH_PATH,
    TEMPLATE_DUMMY_SEARCH_PATH,
    ASSETS_DUMMY_SEARCH_PATH,
)

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: Config
# Description: Class for the Configuration PROTEUS application
# Date: 11/10/2022
# Version: 0.3
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
#         José María Delgado Sánchez
# --------------------------------------------------------------------------


@dataclass
class Config(metaclass=SingletonMeta):

    # Settings
    app_settings: AppSettings = None
    profile_settings: ProfileSettings = None

    # App settings copy (store user changes)
    app_settings_copy: AppSettings = None

    # Listed profiles
    # NOTE: They are stored as lowercase strings. Validation is not
    # performed to avoid loading all the profiles. We assume built-in
    # profiles must be valid.
    listed_profiles: list[str] = None

    def __post_init__(self):
        """
        It initializes the config paths for PROTEUS application.
        """
        # NOTE: Methods order is important. They have dependencies between them.

        # Logger configuration
        self._logger_configuration()

        # Load settings
        self._load_settings()

        # Qt search paths
        self._setup_qt_search_paths()

    # ==========================================================================
    # Private methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: _load_settings
    # Description: Private method that loads the settings from the configuration
    #              files.
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_settings(self) -> None:
        """
        Private method that loads the settings from the configuration files.
        """
        # Load app settings
        self.app_settings = AppSettings.load(proteus.PROTEUS_APP_PATH)

        # List profiles directories available
        self.listed_profiles = [
            path.name
            for path in self.app_settings.profiles_directory.glob("*")
            if path.is_dir()
        ]

        # If the selected profile is not available, use the first listed profile
        if not self.app_settings.selected_profile in self.listed_profiles:
            log.error(
                f"Selected profile '{self.app_settings.selected_profile}' is not available in the profiles directory. Using listed profiles instead."
            )
            self.app_settings.selected_profile = self.listed_profiles[0]

        # Select correct profile path (custom or default)
        profile_path: Path = (
            self.app_settings.profiles_directory / self.app_settings.selected_profile
        )
        if not self.app_settings.using_default_profile:
            profile_path = self.app_settings.custom_profile_path

        # Try to load the profile settings
        try:
            self.profile_settings = ProfileSettings.load(profile_path)
        except Exception as e:
            log.error(f"Error loading profile settings from {profile_path}. Error: {e}")

            if self.app_settings.using_default_profile:
                log.critical(
                    "Default profile must be valid to run the application. Exiting..."
                )
                raise e
            else:
                log.warning(
                    "Custom profile is not valid. Using default profile instead."
                )
                self.profile_settings = ProfileSettings.load(
                    self.app_settings.profiles_directory
                    / self.app_settings.selected_profile
                )
                self.app_settings.using_default_profile = True

        # Validate settings using profile information
        if self.app_settings.default_view not in self.profile_settings.listed_templates:
            log.warning(
                f"Selected default view '{self.app_settings.default_view}' is not available in the profile. Using profile preferred view instead."
            )

            self.app_settings.default_view = (
                self.profile_settings.preferred_default_view
            )

        # Create a copy of the app settings to store user changes
        self.app_settings_copy = replace(self.app_settings)

    # --------------------------------------------------------------------------
    # Method: _setup_qt_search_paths
    # Description: Private method that sets up the search paths for the application.
    # Date: 20/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _setup_qt_search_paths(self) -> None:
        """
        Private method that sets up the search paths for the application.
        """
        # Configure Qt search paths
        QtCore.QDir.addSearchPath(
            RESOURCES_SEARCH_PATH, self.app_settings.resources_directory.as_posix()
        )  # Used in PyQt stylesheets

        # Configure dummy search paths
        # NOTE: This is used by the XSLT templates to access local files
        # This allows to use search path syntax so it can be handled as a
        # request by the request interceptor. It will build the path to the
        # file and return it as an http response.
        QtCore.QDir.addSearchPath(TEMPLATE_DUMMY_SEARCH_PATH, "")
        QtCore.QDir.addSearchPath(ASSETS_DUMMY_SEARCH_PATH, "")

    # --------------------------------------------------------------------------
    # Method: _logger_configuration
    # Description: Private method that configures the logger for the application.
    # Date: 10/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _logger_configuration(self) -> None:
        # Create a logger
        logger = logging.getLogger(PROTEUS_LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        # Create directory for log files
        if not PROTEUS_LOGGING_DIR.exists():
            PROTEUS_LOGGING_DIR.mkdir()

        # Define a formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create a TimedRotatingFileHandler to create log files based on date and time
        log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
        file_handler = TimedRotatingFileHandler(
            filename=f"{PROTEUS_LOGGING_DIR}/{log_filename}",
            when="midnight",
            interval=1,
            backupCount=PROTEUS_MAX_LOG_FILES,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        # Clean logs
        # This is required because TimedRotatingFileHandler does not delete old log files
        log_files = [str(log_file) for log_file in PROTEUS_LOGGING_DIR.glob("*.log")]
        log_files.sort(key=os.path.getmtime, reverse=True)

        for old_log_file in log_files[PROTEUS_MAX_LOG_FILES:]:
            os.remove(old_log_file)
