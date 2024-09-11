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
from typing import List, Dict
from pathlib import Path
from dataclasses import dataclass
from configparser import ConfigParser

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.resources.icons import Icons, ProteusIconType
from proteus.model.template import Template
from proteus.model.archetype_repository import ArchetypeRepository

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
PREFERENCES: str = "preferences"
PREFERENCE_DEFAULT_VIEW: str = "default_view"

# Information
INFORMATION: str = "information"
NAME: str = "name"
DESCRIPTION: str = "description"
IMAGE: str = "image"


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

    # Directory settings
    plugins_directory: Path = None
    archetypes_directory: Path = None
    xslt_directory: Path = None
    icons_directory: Path = None
    i18n_directory: Path = None

    # Profile preferences settings
    preferred_default_view: str = None

    # Found templates
    listed_templates: List[str] = None


    # --------------------------------------------------------------------------
    # Method: load
    # Description: Load profile settings from the configuration file
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
        config_parser.read(config_file_path, encoding="utf-8")

        settings_file_path: Path = config_file_path

        log.info(f"Loading settings from {settings_file_path}...")

        profile_settings = ProfileSettings(
            profile_path=profile_path,
            settings_file_path=settings_file_path,
            config_parser=config_parser,
        )

        profile_settings._load_directories()
        profile_settings._validate_profile_basic_content()
        profile_settings._load_preference_settings()

        return profile_settings


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

        # Archetypes and XSLT directories are mandatory
        assert (
            self.archetypes_directory.exists()
        ), f"Archetypes directory {self.archetypes_directory} does not exist in profile {self.profile_path}!"
        assert (
            self.xslt_directory.exists()
        ), f"XSLT directory {self.xslt_directory} does not exist in profile {self.profile_path}!"

        # Plugins, icons and i18n directories are optional
        if not directories[PLUGINS_DIRECTORY]:
            log.warning(
                f"Plugins directory is not set in profile config {self.profile_path}!"
            )
            self.plugins_directory = None
        elif not self.plugins_directory.exists():
            log.warning(
                f"Plugins directory {self.plugins_directory} does not exist in profile {self.profile_path}!"
            )
            self.plugins_directory = None

        if not directories[ICONS_DIRECTORY]:
            log.warning(
                f"Icons directory is not set in profile config {self.profile_path}!"
            )
            self.icons_directory = None
        elif not self.icons_directory.exists():
            log.warning(
                f"Icons directory {self.icons_directory} does not exist in profile {self.profile_path}!"
            )
            self.icons_directory = None

        if not directories[I18N_DIRECTORY]:
            log.warning(
                f"i18n directory is not set in profile config {self.profile_path}!"
            )
            self.i18n_directory = None
        elif not self.i18n_directory.exists():
            log.warning(
                f"i18n directory {self.i18n_directory} does not exist in profile {self.profile_path}!"
            )
            self.i18n_directory = None

        log.info(f"Directories loaded from {self.settings_file_path}.")
        log.info(f"{self.archetypes_directory = }")
        log.info(f"{self.xslt_directory = }")
        log.info(f"{self.plugins_directory = }")
        log.info(f"{self.icons_directory = }")
        log.info(f"{self.i18n_directory = }")

    # --------------------------------------------------------------------------
    # Method: _load_preference_settings
    # Description: Load profile preference settings from the configuration file
    # Date: 15/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_preference_settings(self) -> None:
        """
        Load user settings from the configuration file.
        """
        # Settings section
        settings = self.config_parser[PREFERENCES]

        # Default view -----------------------
        preferred_default_view = settings[PREFERENCE_DEFAULT_VIEW]

        assert (
            preferred_default_view is not None and preferred_default_view != ""
        ), f"Selected view setting is not defined in {self.settings_file_path}!"

        if preferred_default_view not in self.listed_templates:
            log.error(
                f"Selected view {preferred_default_view} was not found in the XSLT directory. Using first view found instead."
            )
            preferred_default_view = self.listed_templates[0]

        self.preferred_default_view = preferred_default_view


    # --------------------------------------------------------------------------
    # Method: _validate_profile_basic_content
    # Description: Validate the basic content of the profile
    # Date: 18/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _validate_profile_basic_content(self) -> None:
        """
        Validate the basic content of the profile (templates and archetype repositories).
        Loads all the templates and the archetype repository in order to check if they are valid.
        List the templates found.
        """

        # Templates --------------------------
        self.listed_templates = []

        for template_dir in self.xslt_directory.iterdir():
            try:
                template = Template.load(template_dir)
                self.listed_templates.append(template.name)
            except Exception as e:
                log.error(f"Could not load template from {template_dir}. It will be ignored in profile settings. Error: {e}")

        assert (
            len(self.listed_templates) > 0
        ), f"No valid templates found in the XSLT directory {self.xslt_directory}!"

        log.info(f"Listed templates: {self.listed_templates}")

        # Archetype repository ----------------
        try:
            ArchetypeRepository.load_object_archetypes(self.archetypes_directory)
            ArchetypeRepository.load_document_archetypes(self.archetypes_directory)
            ArchetypeRepository.load_project_archetypes(self.archetypes_directory)
        except Exception as e:
            log.error(f"Could not load archetype repository from {self.archetypes_directory}. It will be ignored in profile settings. Error: {e}")
            raise e


@dataclass
class ProfileBasicMetadata:
    """
    Profile basic metadata class. Do not load any information apart from the name, description and image.
    """

    # General purpose variables
    profile_path: Path = None
    settings_file_path: Path = None
    config_parser: ConfigParser = None

    # Profile metadata
    name: str = None
    description: str = None
    image: Path = None

    # --------------------------------------------------------------------------
    # Method: load
    # Description: Load profile basic metadata from the configuration file
    # Date: 11/09/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @staticmethod
    def load(profile_path: Path) -> "ProfileBasicMetadata":
        """
        Loads the profile basic metadata from the configuration file located in the
        profile directory. If the file does not exist, error is raised.

        :param profile_path: Path to the profile directory.
        """
        config_file_path: Path = profile_path / CONFIG_FILE

        assert (
            config_file_path.exists()
        ), f"PROTEUS profile configuration file {CONFIG_FILE} does not exist in {profile_path}!"

        config_parser: ConfigParser = ConfigParser()
        config_parser.read(config_file_path, encoding="utf-8")

        settings_file_path: Path = config_file_path

        log.info(f"Loading basic metadata from {settings_file_path}...")

        profile_metadata = ProfileBasicMetadata(
            profile_path=profile_path,
            settings_file_path=settings_file_path,
            config_parser=config_parser,
        )

        profile_metadata._load_information()

        return profile_metadata
    
    # --------------------------------------------------------------------------
    # Method: _load_information
    # Description: Load profile information from the configuration file
    # Date: 11/09/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_information(self) -> None:
        """
        Load profile information from the configuration file.
        """
        # information section
        information = self.config_parser[INFORMATION]

        self.name = information[NAME]
        self.description = information[DESCRIPTION]
        image_relative_path = information[IMAGE]

        assert (
            self.name is not None and self.name != ""
        ), f"Profile name is not defined in '{self.settings_file_path}'!"

        assert (
            image_relative_path is not None and image_relative_path != ""
        ), f"Profile image is not defined in '{self.settings_file_path}'!"
        
        if self.description is None or self.description == "":
            log.warning(f"Profile description is not defined in '{self.settings_file_path}'!")
            self.description = ""

        self.image = self.profile_path / image_relative_path

        assert (
            self.image.exists()
        ), f"Profile image '{image_relative_path}' does not exist in profile '{self.profile_path}'!"


        log.info(f"Profile information loaded from {self.settings_file_path}.")
        log.info(f"{self.name = }")
        log.info(f"{self.description = }")
        log.info(f"{self.image = }")


    # --------------------------------------------------------------------------
    # Method: list_profiles
    # Description: List the profiles available in the profiles directory
    # Date: 11/09/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @staticmethod
    def list_profiles(profiles_directory: Path) -> Dict[str, "ProfileBasicMetadata"]:
        """
        List the profiles available in the profiles directory. If profile metadata
        cannot be loaded correctly, it is ignored.

        :param profiles_directory: Path to the profiles directory.
        :return: Dictionary with the profile name as key and the profile metadata as value.
        """
        
        assert (
            profiles_directory.exists()
        ), f"PROTEUS profiles directory {profiles_directory} does not exist!"

        listed_profiles = dict()

        for profile_dir in profiles_directory.iterdir():
            try:
                profile_metadata = ProfileBasicMetadata.load(profile_dir)
                listed_profiles[profile_dir.name] = profile_metadata
            except Exception as e:
                log.error(f"Could not load profile metadata from {profile_dir}. It will be ignored. Error: {e}")

        return listed_profiles