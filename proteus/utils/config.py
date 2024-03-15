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

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
import datetime
from typing import Dict, List, Tuple
from pathlib import Path
from configparser import ConfigParser
import shutil
from dataclasses import dataclass
import logging
from logging.handlers import TimedRotatingFileHandler

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from lxml import etree as ET
from PyQt6 import QtCore

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.utils.abstract_meta import SingletonMeta
from proteus import PROTEUS_LOGGER_NAME, PROTEUS_LOGGING_DIR, PROTEUS_MAX_LOG_FILES
from proteus.utils import (
    RESOURCES_SEARCH_PATH,
    TEMPLATE_DUMMY_SEARCH_PATH,
    ASSETS_DUMMY_SEARCH_PATH,
)

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Constant declarations for PROTEUS configuration file keys
# --------------------------------------------------------------------------

CONFIG_FILE: str = "proteus.ini"

# Settings
SETTINGS: str = "settings"
SETTING_LANGUAGE: str = "language"
SETTING_DEFAULT_VIEW: str = "default_view"
SETTING_CUSTOM_ARCHETYPE_REPOSITORY: str = "custom_archetype_repository"
SETTING_DEFAULT_ARCHETYPE_REPOSITORY: str = "default_archetype_repository"
SETTING_USING_CUSTOM_REPOSITORY: str = "using_custom_archetype_repository"

# Directories
DIRECTORIES: str = "directories"
BASE_DIRECTORY: str = "base_directory"
ARCHETYPES_DIRECTORY: str = "archetypes_directory"
RESOURCES_DIRECTORY: str = "resources_directory"
PLUGINS_DIRECTORY: str = "plugins_directory"
ICONS_DIRECTORY: str = "icons_directory"
XSLT_DIRECTORY: str = "xslt_directory"
I18N_DIRECTORY: str = "i18n_directory"

# --------------------------------------------------------------------------
# Class: Config
# Description: Class for the Configuration PROTEUS application
# Date: 11/10/2022
# Version: 0.2
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
#         José María Delgado Sánchez
# --------------------------------------------------------------------------


@dataclass
class Config(metaclass=SingletonMeta):

    # --------------------------------
    # Variables
    # --------------------------------

    # App directories ----------------
    base_directory: Path = None
    resources_directory: Path = None
    archetypes_directory: Path = None
    plugins_directory: Path = None
    icons_directory: Path = None
    xslt_directory: Path = None
    i18n_directory: Path = None

    # Archetype repositories ----------
    archetypes_repositories: Dict[str, Path] = None
    current_archetype_repository: Path = None
    using_custom_repository: bool = False

    # XSLT templates ------------------
    xslt_default_view: str = None

    # Language ------------------------
    language: str = None

    # Other settings ------------------
    config: ConfigParser = None

    settings: Dict[str, str] = None

    # TODO: This is set in the project service. Current project information
    # may be stored in a separate class. This is a workarround to access
    # assets folder.
    current_project_path: str = None

    # TODO: This is a workaround to preserve user settings changes until
    # the application is restarted. This is required because the config
    # setting dialog do not access the config file directly but this class
    # instance to check settings values.
    current_config_file_user_settings: Dict[str, str] = None

    def __post_init__(self):
        """
        It initializes the config paths for PROTEUS application.
        """
        # NOTE: Methods order is important. They have dependencies between them.

        # Application configuration
        self.config: ConfigParser = self._create_config_parser()

        # Logger configuration
        self._logger_configuration()

        # Application directories
        self._setup_directories()

        # Qt search paths
        self._setup_qt_search_paths()

        # Load system archetypes repositories
        self.archetypes_repositories: Dict[str, Path] = (
            self._load_archetypes_repositories()
        )

        # Application settings
        self._setup_app_settings()

        # Check application directories
        self._check_application_directories()

    # ==========================================================================
    # Private methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: _setup_directories
    # Description: Private method that sets up the directories for the application.
    # Date: 20/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _setup_directories(self) -> None:
        """
        Private method that sets up the directories for the application.
        """
        # Application directories
        directories = self.config[DIRECTORIES]
        self.base_directory: Path = (
            proteus.PROTEUS_APP_PATH / directories[BASE_DIRECTORY]
        )
        self.resources_directory: Path = (
            proteus.PROTEUS_APP_PATH / directories[RESOURCES_DIRECTORY]
        )

        # -------
        self.archetypes_directory: Path = (
            proteus.PROTEUS_APP_PATH / directories[ARCHETYPES_DIRECTORY]
        )
        self.plugins_directory: Path = (
            proteus.PROTEUS_APP_PATH / directories[PLUGINS_DIRECTORY]
        )
        self.icons_directory: Path = (
            self.resources_directory / directories[ICONS_DIRECTORY]
        )
        self.xslt_directory: Path = (
            self.resources_directory / directories[XSLT_DIRECTORY]
        )
        self.i18n_directory: Path = (
            self.resources_directory / directories[I18N_DIRECTORY]
        )

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
            RESOURCES_SEARCH_PATH, self.resources_directory.as_posix()
        )  # Used in PyQt stylesheets

        # Configure dummy search paths
        # NOTE: This is used by the XSLT templates to access local files
        # This allows to use search path syntax so it can be handled as a
        # request by the request interceptor. It will build the path to the
        # file and return it as an http response.
        QtCore.QDir.addSearchPath(TEMPLATE_DUMMY_SEARCH_PATH, "")
        QtCore.QDir.addSearchPath(ASSETS_DUMMY_SEARCH_PATH, "")

    # --------------------------------------------------------------------------
    # Method: _setup_app_settings
    # Description: Private method that sets up the application settings.
    # Date: 20/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _setup_app_settings(self) -> None:
        """
        Private method that sets up the application settings.
        """
        self.settings = self.config[SETTINGS]

        # Language --------------------------------
        self.language: str = self.settings[SETTING_LANGUAGE]
        log.info(f"Using language '{self.language}'")

        # Default view -----------------------------
        self.xslt_default_view: str = self.settings[SETTING_DEFAULT_VIEW]
        log.info(f"Using default view '{self.xslt_default_view}'")

        # Default Archetype repository -------------
        default_archetype_repository: str = self.settings[
            SETTING_DEFAULT_ARCHETYPE_REPOSITORY
        ]
        if default_archetype_repository in self.archetypes_repositories:
            self.current_archetype_repository = self.archetypes_repositories[
                default_archetype_repository
            ]
        else:
            log.error(
                f"Default archetype repository '{default_archetype_repository}' does not exist. Using first repository found."
            )
            self.current_archetype_repository = list(
                self.archetypes_repositories.values()
            )[0]

        # Custom Archetype repository --------------
        is_valid_repository: bool = False
        custom_archetype_repository: str = self.settings[
            SETTING_CUSTOM_ARCHETYPE_REPOSITORY
        ]

        custom_archetype_repository_path: Path = Path(
            custom_archetype_repository
        ).resolve()
        if custom_archetype_repository_path.exists():
            is_valid_repository = True
        else:
            log.warning(
                f"Custom archetype repository '{custom_archetype_repository}' does not exist. Using default repository."
            )

        # Using custom Archetype repository ---------
        using_custom_archetype_repository: str = self.settings[
            SETTING_USING_CUSTOM_REPOSITORY
        ]

        self.using_custom_repository = using_custom_archetype_repository == "True"

        if self.using_custom_repository and is_valid_repository:
            log.info(
                f"Using custom archetype repository '{custom_archetype_repository}'"
            )
            self.current_archetype_repository = custom_archetype_repository_path
        else:
            log.info(
                f"Using default archetype repository '{default_archetype_repository}'"
            )


        # Store settings to keep track of user changes --------------------------------
        self.current_config_file_user_settings: Dict[str, str] = {}
        self.current_config_file_user_settings[SETTING_LANGUAGE] = self.language
        self.current_config_file_user_settings[SETTING_DEFAULT_ARCHETYPE_REPOSITORY] = (
            default_archetype_repository
        )
        self.current_config_file_user_settings[SETTING_CUSTOM_ARCHETYPE_REPOSITORY] = (
            custom_archetype_repository
        )
        self.current_config_file_user_settings[SETTING_USING_CUSTOM_REPOSITORY] = (
            using_custom_archetype_repository
        )


    # --------------------------------------------------------------------------
    # Method: _load_archetypes_repositories
    # Description: Private method that loads archetypes repositories from the
    #              archetypes directory.
    # Date: 20/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_archetypes_repositories(self) -> Dict[str, Path]:
        """
        Load archetypes repositories from the arhcetypes directory. Returns a dictionary
        with the repository name (folder name) and the repository path.

        It use ArchetypeRepository to check if the repository is valid loading the archetypes
        from the repository.
        """
        # Initialize dictionary
        archetypes_repositories: Dict[str, Path] = {}

        # Iterate over archetypes directory folders
        for archetype_folder in self.archetypes_directory.iterdir():
            # Check if folder is a directory
            if archetype_folder.is_file():
                log.warning(
                    f"Unexpected item in archetypes directory: {archetype_folder}. It will be ignored."
                )
                continue

            # Add the repository to the dictionary
            archetypes_repositories[archetype_folder.name] = archetype_folder

        return archetypes_repositories

    # --------------------------------------------------------------------------
    # Method: _create_config_parser
    # Description: Private method that creates configuration parser and loads config file.
    # Date: 10/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _create_config_parser(self) -> ConfigParser:
        """
        Private method that creates configuration parser and loads config file.
        """

        CONFIG_FILE_PATH: Path = proteus.PROTEUS_APP_PATH / CONFIG_FILE

        assert (
            CONFIG_FILE_PATH.exists()
        ), f"PROTEUS configuration file {CONFIG_FILE} does not exist!"

        # Check for proteus.ini file where the application is executed
        # NOTE: This allows to change config in single executable app version
        CONFIG_FILE_EXEC_PATH: Path = Path.cwd() / CONFIG_FILE
        if not CONFIG_FILE_EXEC_PATH.exists():
            log.warning(
                f"PROTEUS configuration file {CONFIG_FILE} does not exist in the execution path. Copying configuration file to execution path..."
            )

            # Copy proteus.ini file to execution path
            shutil.copy(CONFIG_FILE_PATH, CONFIG_FILE_EXEC_PATH)

        config_parser: ConfigParser = ConfigParser()
        config_parser.read(CONFIG_FILE_EXEC_PATH)

        # Variable to store init file path
        # This is required to avoid loosing track if cwd changes
        self.config_file_path: Path = CONFIG_FILE_EXEC_PATH

        return config_parser

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

    # Initial checks ----------------------------------------------------------
    def _check_application_directories(self) -> None:
        """
        It checks that essential PROTEUS directories exist.
        """
        log.info("Checking PROTEUS directories...")

        # Check if resources directory exists
        assert (
            self.resources_directory.is_dir()
        ), f"PROTEUS resources directory '{self.resources_directory}' does not exist!"

        log.info("  Resources directory OK")

        # Check if icons directory exists
        assert (
            self.icons_directory.is_dir()
        ), f"PROTEUS icons directory '{self.icons_directory}' does not exist!"

        log.info("  Icons directory OK")

        # Check if archetypes directory exists
        assert (
            self.archetypes_directory.is_dir()
        ), f"PROTEUS archetypes directory '{self.archetypes_directory}' does not exist!"

        log.info("  Archetypes directory OK")

        # Check if xslt directory exists
        assert (
            self.xslt_directory.is_dir()
        ), f"PROTEUS xslt directory '{self.xslt_directory}' does not exist!"

        log.info("  XSLT directory OK")

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: save_user_settings
    # Description: It saves the user settings in the configuration file.
    # Date: 10/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def save_user_settings(self, settings: Dict[str, str]) -> None:
        """
        It saves the user settings in the configuration file. The settings
        will apply the next time the application is started.
        """
        # Update settings
        for setting in settings:
            log.info(f"Setting {setting} updated to {settings[setting]}")
            self.config.set(SETTINGS, setting, settings[setting])

        # Save settings
        with open(self.config_file_path, "w") as configfile:
            self.config.write(configfile)

        # Update current config file user settings
        self.current_config_file_user_settings.update(settings)
