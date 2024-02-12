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
    ProteusIconType,
    DEFAULT_ICON_KEY,
    ENTRY_POINTS_TAG,
    ENTRY_POINT_TAG,
    DEPENCENCIES_TAG,
    PLUGIN_DEPENDENCY_TAG,
    NAME_ATTRIBUTE,
    LANGUAGE_ATTRIBUTE,
    FILE_ATTRIBUTE,
    DEFAULT_ATTRIBUTE,
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
TEMPLATE_FILE: str = "template.xml"
ICONS_FILE: str = "icons.xml"

# Settings
SETTINGS: str = "settings"
SETTING_LANGUAGE: str = "language"
SETTING_ARCHETYPE_REPOSITORY: str = "archetype_repository"

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


class Config(metaclass=SingletonMeta):

    def __init__(self):
        """
        It initializes the config paths for PROTEUS application.
        """
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
        QtCore.QDir.addSearchPath(
            RESOURCES_SEARCH_PATH, self.resources_directory.as_posix()
        )  # Used in PyQt stylesheets

        # Configure dummy search paths -------------------------------------
        # NOTE: This is used by the XSLT templates to access local files
        # This allows to use search path syntax so it can be handled as a
        # request by the request interceptor. It will build the path to the
        # file and return it as an http response.
        QtCore.QDir.addSearchPath(TEMPLATE_DUMMY_SEARCH_PATH, "")
        QtCore.QDir.addSearchPath(ASSETS_DUMMY_SEARCH_PATH, "")

        # Application settings ---------------------------------------------
        self.settings = self.config[SETTINGS]

        # Language
        self.language: str = self.settings[SETTING_LANGUAGE]

        # Archetype repository
        self.default_repository: bool = True
        archetype_repository: str = self.settings[SETTING_ARCHETYPE_REPOSITORY]
        if archetype_repository != "":
            archetype_repository_path: Path = (
                self.base_directory / archetype_repository
            ).resolve()
            if archetype_repository_path.exists():
                self.archetypes_directory = archetype_repository_path
                self.default_repository = False
            else:
                log.warning(
                    f"Archetype repository '{archetype_repository_path}' does not exist. Using default repository."
                )

        # Store settings to keep track of user changes
        # TODO: This is a workaround to preserve user settings changes until
        # the application is restarted. This is required because the config
        # setting dialog do not access the config file directly but this class
        # instance to check settings values. This class cannot modify most of
        # its variables during runtime because it will
        self.current_config_file_user_settings: Dict[str, str] = {}
        self.current_config_file_user_settings[SETTING_LANGUAGE] = self.language
        self.current_config_file_user_settings[SETTING_ARCHETYPE_REPOSITORY] = (
            archetype_repository
        )

        # Icons dictionary -------------------------------------------------
        # NOTE: Use get_icon method to access icons to ensure default icon is
        # used if icon is not found.
        self._icons_dictionary: Dict[str, Dict[str, Path]] = (
            self._create_icons_dictionary()
        )

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

        # Update current config file user settings
        self.current_config_file_user_settings.update(settings)

    def get_icon(self, type: ProteusIconType, name: str) -> Path:
        """
        It returns the icon path for the given type and name.

        :param type: Icon type.
        :param name: Icon code name.
        """
        assert (
            type in self._icons_dictionary
        ), f"Icon type {type} not found, check icons.xml file"

        # Check if name exists
        if name not in self._icons_dictionary[type]:
            log.warning(
                f"Icon name '{name}' not found for type '{type}', using default icon"
            )
            name = DEFAULT_ICON_KEY

        return self._icons_dictionary[type][name]

    # TODO: Refactor this method to improve readability
    def _create_icons_dictionary(self) -> Dict[ProteusIconType, Dict[str, Path]]:
        """
        Private method that reads the icons.xml file and creates a nested
        dictionary structure to access icons by type and name.

        It reads the icons file from the resources directory and the archetype
        repository.

        Archetype repository icons can only add values for archetypes and acronyms.
        Other types found will be ignored.

        All the repeated values (included default) defined in the icons file inside
        archetype repository will override the values defined in the resources
        directory. This allows mantaining default values in the application while
        it is possible to override them in the archetype repository specific
        implementation.
        """
        # ----------------------------
        # Initialize dictionary
        # ----------------------------
        icons_dictionary: Dict[ProteusIconType, Dict[str, Path]] = {}

        # ----------------------------
        # Resources icons file handling
        # ----------------------------

        # Parse icons file
        resource_icon_file: Path = self.icons_directory / ICONS_FILE
        resources_icons_tree: ET._ElementTree = ET.parse(resource_icon_file)
        resources_icons_root: ET._Element = resources_icons_tree.getroot()

        # Iterate over icons tag children (type tag) to create each type dictionary
        for type_tag in resources_icons_root.iterchildren():
            # Get name attribute to check if it is a valid icon type
            type_name: str = type_tag.attrib.get("name", None)
            assert (
                type_name in ProteusIconType._member_map_.values()
            ), f"Icon type '{type_name}' is not a valid ProteusIconType, check {resource_icon_file.as_posix()} file."

            # Initialize type dictionary
            type_dictionary: Dict[str, Path] = {}

            # Get the default icon and store if it exists
            default_icon: str = type_tag.attrib.get("default", None)
            if default_icon is not None:
                type_dictionary[DEFAULT_ICON_KEY] = self.icons_directory / default_icon
            else:
                log.error(
                    f"Default icon not found for icon type '{type_name}'. This could crash the application. Check {resource_icon_file.as_posix()} file."
                )

            # Iterate over icons tag children icon
            for icon in type_tag.iterchildren():
                # Get key and file attributes for the icon tag
                key = icon.attrib.get("key", None)
                file = icon.attrib.get("file", None)

                if key is None or key == "" or file is None or file == "":
                    log.error(
                        f"Icon key or file are not correctly defined for icon type '{type_name}'. Check {resource_icon_file.as_posix()} file. Key value: {key}, File value: {file}"
                    )

                # Check if icon file exists
                file_path: Path = self.icons_directory / file
                if not file_path.exists():
                    log.error(
                        f"Icon file '{file_path}' does not exist. Check {resource_icon_file.as_posix()} file."
                    )

                # Add icon to type dictionary
                type_dictionary[key] = file_path

            # Add type dictionary to icons dictionary
            icons_dictionary[type_name] = type_dictionary

        # ----------------------------
        # Archetypes icons file handling
        # ----------------------------

        # Parse icons file
        archetypes_icon_file: Path = self.archetypes_directory / "icons" / ICONS_FILE

        # If no icons file is found, return the current icons dictionary
        if not archetypes_icon_file.exists():
            log.info(
                f"Icons file not found in archetype repository. Using default icons."
            )
            return icons_dictionary

        archetypes_icons_tree: ET._ElementTree = ET.parse(archetypes_icon_file)
        archetypes_icons_root: ET._Element = archetypes_icons_tree.getroot()

        # Iterate over icons tag children (type tag) to create each type dictionary
        # NOTE: This will override the values defined in the resources directory
        for type_tag in archetypes_icons_root.iterchildren():
            # Get name attribute to check if it is a valid icon type
            type_name: str = type_tag.attrib.get("name", None)

            accepted_types: List[ProteusIconType] = [
                ProteusIconType.Archetype,
                ProteusIconType.Document,
            ]

            # Check if type is valid
            if type_name not in accepted_types:
                log.warning(
                    f"Icon type '{type_name}' cannot be defined in archetype repository, check {archetypes_icon_file.as_posix()} file."
                )
                continue

            # Retrieve type dictionary if it exists
            type_dictionary: Dict[str, Path] = icons_dictionary.get(type_name, {})

            # Get the default icon and store if it exists
            default_icon: str = type_tag.attrib.get("default", None)
            if default_icon is not None:
                log.info(
                    f"Default icon found for icon type '{type_name}'. This will override the default icon defined in the resources directory."
                )
                type_dictionary[DEFAULT_ICON_KEY] = (
                    self.archetypes_directory / "icons" / default_icon
                )

            # Iterate over icons tag children icon
            for icon in type_tag.iterchildren():
                # Get key and file attributes for the icon tag
                key = icon.attrib.get("key", None)
                file = icon.attrib.get("file", None)

                if key is None or key == "" or file is None or file == "":
                    log.error(
                        f"Icon key or file are not correctly defined for icon type '{type_name}'. Check {archetypes_icon_file.as_posix()} file. Key value: {key}, File value: {file}"
                    )

                # Check if icon file exists
                file_path: Path = self.archetypes_directory / "icons" / file
                if not file_path.exists():
                    log.error(
                        f"Icon file '{file_path}' does not exist. Check {archetypes_icon_file.as_posix()} file."
                    )

                # Add icon to type dictionary
                type_dictionary[key] = file_path

            # Add type dictionary to icons dictionary
            icons_dictionary[type_name] = type_dictionary

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
