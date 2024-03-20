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
PREFERENCE_DEFAULT_ARCHETYPE_REPOSITORY: str = "selected_archetype_repository"


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
    preferred_archetype_repository: str = None

    # Found templates/archetypes repositories
    listed_templates: List[str] = None
    listed_archetype_repositories: List[str] = None

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

        profile_settings = ProfileSettings(
            profile_path=profile_path,
            settings_file_path=settings_file_path,
            config_parser=config_parser,
        )

        profile_settings._load_directories()
        profile_settings._list_templates_and_archetype_repositories()
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
        elif not self.plugins_directory.exists():
            log.warning(
                f"Plugins directory {self.plugins_directory} does not exist in profile {self.profile_path}!"
            )

        if not directories[ICONS_DIRECTORY]:
            log.warning(
                f"Icons directory is not set in profile config {self.profile_path}!"
            )
        elif not self.icons_directory.exists():
            log.warning(
                f"Icons directory {self.icons_directory} does not exist in profile {self.profile_path}!"
            )

        if not directories[I18N_DIRECTORY]:
            log.warning(
                f"i18n directory is not set in profile config {self.profile_path}!"
            )
        elif not self.i18n_directory.exists():
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

        # Default archetype repository -----------------------
        preferred_archetype_repository = settings[PREFERENCE_DEFAULT_ARCHETYPE_REPOSITORY]

        assert (
            preferred_archetype_repository is not None
            and preferred_archetype_repository != ""
        ), f"Default archetype repository setting is not defined in {self.settings_file_path}!"

        if preferred_archetype_repository not in self.listed_archetype_repositories:
            log.error(
                f"Default archetype repository {preferred_archetype_repository} was not found in the archetypes directory. Using first archetype repository found instead."
            )
            preferred_archetype_repository = self.listed_archetype_repositories[0]

        self.preferred_archetype_repository = preferred_archetype_repository


    # --------------------------------------------------------------------------
    # Method: _list_templates_and_archetype_repositories
    # Description: List templates and archetype repositories found in the profile
    # Date: 18/03/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _list_templates_and_archetype_repositories(self) -> None:
        """
        List templates and archetype repositories found in the profile.

        It validates that the templates and archetypes repositories are valid
        by loading them using their corresponding classes. They listed items
        are not stored, just their names.
        """

        # Templates
        self.listed_templates = []

        for template_dir in self.xslt_directory.iterdir():
            try:
                Template.load(template_dir)
                self.listed_templates.append(template_dir.name)
            except Exception as e:
                log.error(f"Could not load template from {template_dir}. It will be ignored in profile settings. Error: {e}")

        assert (
            len(self.listed_templates) > 0
        ), f"No valid templates found in the XSLT directory {self.xslt_directory}!"

        # Archetype repositories
        self.listed_archetype_repositories = []

        for archetype_repository_dir in self.archetypes_directory.iterdir():
            try:
                ArchetypeRepository.load_object_archetypes(archetype_repository_dir)
                ArchetypeRepository.load_document_archetypes(archetype_repository_dir)
                ArchetypeRepository.load_project_archetypes(archetype_repository_dir)
                self.listed_archetype_repositories.append(archetype_repository_dir.name)
            except Exception as e:
                log.error(f"Could not load archetype repository from {archetype_repository_dir}. It will be ignored in profile settings. Error: {e}")

        assert (
            len(self.listed_archetype_repositories) > 0
        ), f"No valid archetype repositories found in the archetypes directory {self.archetypes_directory}!"

        log.info(f"Listed templates: {self.listed_templates}")
        log.info(f"Listed archetype repositories: {self.listed_archetype_repositories}")