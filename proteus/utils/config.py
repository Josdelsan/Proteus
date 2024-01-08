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
from typing import Dict, List
from pathlib import Path
from configparser import ConfigParser
import shutil
import logging
import threading
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
from proteus import PROTEUS_LOGGER_NAME, PROTEUS_LOGGING_DIR, PROTEUS_MAX_LOG_FILES
from proteus.utils import (
    ENTRY_POINTS_TAG,
    ENTRY_POINT_TAG,
    DEPENCENCIES_TAG,
    PLUGIN_DEPENDENCY_TAG,
    NAME_ATTRIBUTE,
    LANGUAGE_ATTRIBUTE,
    FILE_ATTRIBUTE,
    DEFAULT_ATTRIBUTE,
)

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Constant declarations for PROTEUS configuration file keys
# --------------------------------------------------------------------------

CONFIG_FILE: str = "proteus.ini"
TEMPLATE_FILE: str = "template.xml"
ICONS_FILE: str = "icons.xml"

# Settings
SETTINGS: str = "settings"
LANGUAGE: str = "language"

# Directories
DIRECTORIES: str = "directories"
BASE_DIRECTORY: str = "base_directory"
ARCHETYPES_DIRECTORY: str = "archetypes_directory"
RESOURCES_DIRECTORY: str = "resources_directory"
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


class Config:
    # Singleton instance
    _instance = None
    __lock = threading.Lock()  # Ensure thread safety

    def __new__(cls, *args, **kwargs):
        """
        It creates a singleton instance for Config class.
        """
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        It initializes the config paths for PROTEUS application.
        """
        # Check if the instance has been initialized
        with self.__class__.__lock:
            if self._initialized:
                return
            self._initialized = True

        # Logger configuration
        self._logger_configuration()

        # Application configuration
        self.config: ConfigParser = self._create_config_parser()

        # Application directories ------------------------------------------
        self.directories = self.config[DIRECTORIES]
        self.base_directory: Path = (
            proteus.PROTEUS_APP_PATH / self.directories[BASE_DIRECTORY]
        )
        self.resources_directory: Path = (
            proteus.PROTEUS_APP_PATH / self.directories[RESOURCES_DIRECTORY]
        )
        self.archetypes_directory: Path = (
            proteus.PROTEUS_APP_PATH / self.directories[ARCHETYPES_DIRECTORY]
        )
        self.icons_directory: Path = (
            self.resources_directory / self.directories[ICONS_DIRECTORY]
        )
        self.xslt_directory: Path = (
            self.resources_directory / self.directories[XSLT_DIRECTORY]
        )
        self.i18n_directory: Path = (
            self.resources_directory / self.directories[I18N_DIRECTORY]
        )

        # Configure PyQt search paths --------------------------------------
        QtCore.QDir.addSearchPath("resources", self.resources_directory.as_posix())

        # Application settings ---------------------------------------------
        self.settings = self.config[SETTINGS]
        self.language: str = self.settings[LANGUAGE]

        # Icons dictionary -------------------------------------------------
        # NOTE: Use get_icon method to access icons to ensure default icon is
        # used if icon is not found.
        self._icons_dictionary: Dict[
            str, Dict[str, Path]
        ] = self._create_icons_dictionary()

        # XSL template routes ----------------------------------------------
        self.xslt_routes: Dict[str, Path] = {}
        self.xslt_dependencies: Dict[str, List[str]] = {}
        self.xslt_routes, self.xslt_dependencies = self._load_xslt_templates()

        # Current project --------------------------------------------------
        # TODO: This is set in the project service. Current project information
        # may be stored in a separate class. This is a workarround to access
        # assets folder.
        self.current_project_path: str = None

        # Check application directories
        self.check_application_directories()

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

    def get_icon(self, type: str, name: str) -> Path:
        """
        It returns the icon path for the given type and name.
        """
        assert (
            type in self._icons_dictionary
        ), f"Icon type {type} not found, check icons.xml file"

        # Check if name exists
        if name not in self._icons_dictionary[type]:
            log.warning(
                f"Icon name {name} not found for type {type}, using default icon"
            )
            name = "default"

        return self._icons_dictionary[type][name]

    def _create_icons_dictionary(self) -> Dict[str, Dict[str, Path]]:
        """
        Private method that reads the icons.xml file and creates a nested
        dictionary structure to access icons by type and name.
        """
        # Initialize dictionary
        icons_dictionary: Dict[str, Dict[str, Path]] = {}

        # Parse icons file
        icons_tree: ET._ElementTree = ET.parse(self.icons_directory / ICONS_FILE)
        icons_root: ET._Element = icons_tree.getroot()

        # Iterate over icons tag children type to create each type dictionary
        for type in icons_root:
            # Initialize type dictionary
            type_dictionary: Dict[str, Path] = {}

            # Store default icon
            type_dictionary["default"] = self.icons_directory / type.attrib["default"]

            # Iterate over icons tag children icon
            for icon in type:
                # Add icon to type dictionary
                type_dictionary[icon.attrib["key"]] = (
                    self.icons_directory / icon.attrib["file"]
                )

            # Add type dictionary to icons dictionary
            icons_dictionary[type.attrib["name"]] = type_dictionary

        return icons_dictionary

    def _load_xslt_templates(self) -> (Dict[str, Path], Dict[str, List[str]]):
        """
        Private method that creates a dictionary with the XSLT routes.

        Returns:
            xslt_routes (Dict[str,Path]): Dictionary with the XSLT Paths for each template to
                the entry point file.
            xslt_dependencies (Dict[str, List[str]]): Dictionary with the XSLT plugin dependencies
                for each template.
        """
        # Initialize dictionaries
        xslt_routes: Dict[str, Path] = {}
        xslt_dependencies: Dict[str, List[str]] = {}

        # Iterate over XSLT directory folders
        for xslt_folder in self.xslt_directory.iterdir():
            # Check if folder is a directory
            if xslt_folder.is_file():
                log.warning(
                    f"Unexpected item in XSLT directory: {xslt_folder}. It will be ignored."
                )
                continue

            # Look for the template.xml file inside the folder
            template_file: Path = xslt_folder / TEMPLATE_FILE
            if not template_file.exists():
                log.error(
                    f"XSLT template configuration file {template_file} does not exist! Check your XSLT directory."
                )
                continue

            # Parse template file
            template_tree: ET._ElementTree = ET.parse(template_file)
            template_root: ET._Element = template_tree.getroot()

            # Get the template name
            template_name: str = template_root.get(NAME_ATTRIBUTE)

            # Check name attribute is not empty
            assert (
                template_name is not None and template_name != ""
            ), f"Name attribute not found in template tag for template {template_file}"

            # ----------------------------
            # Entry point file handling
            # ----------------------------

            # Set default entry point in case there is no entryPoints tag
            entry_points: ET._Element = template_root.find(ENTRY_POINTS_TAG)

            # Check entryPoints tag exists
            assert (
                entry_points is not None
            ), f"'entryPoints' tag not found in template {template_name}"

            entry_point_file: str = entry_points.get(DEFAULT_ATTRIBUTE)

            # Iterate over entryPoints tag children to get the entryPoint for the current language or the default one
            for entry_point in entry_points.findall(ENTRY_POINT_TAG):
                # Get language and file attributes for the entryPoint tag
                lang = entry_point.get(LANGUAGE_ATTRIBUTE)
                file = entry_point.get(FILE_ATTRIBUTE)

                # Check xml is well formed
                assert (
                    lang is not None and file is not None
                ), f"Language or file attribute not found in entryPoint tag for template {template_name}"

                # Add the template file to the dictionary if the language is the same as the application language
                # Otherwise, add the default template file
                if lang == self.language:
                    entry_point_file = file

            # Form the entry point file path
            entry_point_file_path: Path = (
                self.xslt_directory / xslt_folder / entry_point_file
            )

            # Check if the template entry point file exists
            assert (
                entry_point_file_path.exists()
            ), f"XSLT template entry point file {entry_point_file} does not exist in {xslt_folder}!"

            # Set the entry point file path
            xslt_routes[template_name] = entry_point_file_path

            # ----------------------------
            # Template dependencies handling
            # ----------------------------
            # Initialize template dependencies list
            template_dependencies: List[str] = []

            # Get the dependencies tag
            dependencies: ET._Element = template_root.find(DEPENCENCIES_TAG)

            # Check dependencies tag exists
            assert (
                dependencies is not None
            ), f"'dependencies' tag not found in template {template_name}"

            # Iterate over dependencies tag children to get the pluginDependency
            for dependency in dependencies.findall(PLUGIN_DEPENDENCY_TAG):
                # Get name attribute for the pluginDependency tag
                name = dependency.get(NAME_ATTRIBUTE)

                # Check xml is well formed
                assert (
                    name is not None and name != ""
                ), f"Name attribute not found in pluginDependency tag for template {template_name}"

                # Add the template dependency to the list
                template_dependencies.append(name)

            # Add the template dependencies list to the dictionary
            xslt_dependencies[template_name] = template_dependencies

        return xslt_routes, xslt_dependencies

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

    def check_application_directories(self) -> None:
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

        # Check if projects archetypes exists
        assert (
            self.archetypes_directory / "projects"
        ).is_dir(), f"PROTEUS archetypes projects directory '{self.archetypes_directory / 'projects'}' does not exist!"

        log.info("  Archetypes projects directory OK")

        # Check if documents archetypes exists
        assert (
            self.archetypes_directory / "documents"
        ).is_dir(), f"PROTEUS archetypes document directory '{self.archetypes_directory / 'documents'}' does not exist!"

        log.info("  Archetypes documents directory OK")

        # Check if objects archetypes exists
        assert (
            self.archetypes_directory / "objects"
        ).is_dir(), f"PROTEUS archetypes objects directory '{self.archetypes_directory / 'objects'}' does not exist!"

        log.info("  Archetypes objects directory OK")

        # Check if xslt directory exists
        assert (
            self.xslt_directory.is_dir()
        ), f"PROTEUS xslt directory '{self.xslt_directory}' does not exist!"

        log.info("  XSLT directory OK")

        # Check if default xsl templates exists in xslt dictionary
        assert (
            "default" in self.xslt_routes
        ), f"PROTEUS xslt default template does not exist!"

        log.info("  XSLT default template OK")

        # Check xsl templates loaded
        for template in self.xslt_routes:
            assert self.xslt_routes[
                template
            ].exists(), (
                f"PROTEUS xslt template '{self.xslt_routes[template]}' does not exist!"
            )

        log.info("  XSLT templates directories OK")
