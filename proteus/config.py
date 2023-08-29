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

from typing import Dict
from pathlib import Path
from configparser import ConfigParser
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from lxml import etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus

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
        if self._initialized:
            return
        self._initialized = True

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
        self.xslt_routes: Dict[str, Path] = self._create_xslt_routes()

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
        with open(proteus.PROTEUS_APP_PATH / CONFIG_FILE, "w") as configfile:
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
        icons_tree: ET.ElementTree = ET.parse(self.icons_directory / ICONS_FILE)
        icons_root: ET.Element = icons_tree.getroot()

        # Iterate over icons tag children type to create each type dictionary
        for type in icons_root:
            # Initialize type dictionary
            type_dictionary: Dict[str, Path] = {}

            # Store default icon
            type_dictionary["default"] = (
                self.icons_directory / type.attrib["default"]
            )

            # Iterate over icons tag children icon
            for icon in type:
                # Add icon to type dictionary
                type_dictionary[icon.attrib["key"]] = (
                    self.icons_directory / icon.attrib["file"]
                )

            # Add type dictionary to icons dictionary
            icons_dictionary[type.attrib["name"]] = type_dictionary

        return icons_dictionary

    def _create_xslt_routes(self) -> Dict[str, Path]:
        """
        Private method that creates a dictionary with the XSLT routes.
        """
        # Initialize dictionary
        xslt_routes: Dict[str, Path] = {}

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
            template_tree: ET.ElementTree = ET.parse(template_file)
            template_root: ET.Element = template_tree.getroot()

            # Get the template name
            template_name: str = template_root.attrib["name"]

            # Iterate over templates tag children to get the item with attribute language = self.language
            for template in template_root:
                # Add the template file to the dictionary if the language is the same as the application language
                # Otherwise, add the default template file
                if template.attrib["language"] == self.language or (
                    template.attrib["language"] == "default"
                    and template_name not in xslt_routes
                ):
                    # Get the template xsl file path
                    xsl_file_path: Path = (
                        self.xslt_directory / xslt_folder / template.attrib["file"]
                    )
                    # Add the template file to the dictionary
                    xslt_routes[template_name] = xsl_file_path

        return xslt_routes

    def _create_config_parser(self) -> ConfigParser:
        """
        Private method that creates configuration parser and loads config file.
        """

        CONFIG_FILE_PATH: Path = proteus.PROTEUS_APP_PATH / CONFIG_FILE

        assert (
            CONFIG_FILE_PATH.exists()
        ), f"PROTEUS configuration file {CONFIG_FILE} does not exist!"

        config_parser: ConfigParser = ConfigParser()
        config_parser.read(CONFIG_FILE_PATH)

        return config_parser

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
