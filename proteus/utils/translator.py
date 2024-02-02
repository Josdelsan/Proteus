# ==========================================================================
# File: translator.py
# Description: Manage the language translations for PROTEUS application
# Date: 26/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict, List
from pathlib import Path
import yaml
import logging
import threading

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from lxml import etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils.config import Config

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

LANGUAGE_CONFIG_FILE = "languages.xml"


# --------------------------------------------------------------------------
# Class: Translator
# Description: Manage the language translations for PROTEUS application
# Date: 26/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class Translator:
    """
    Manage the language translations for PROTEUS application. It stores the
    current language translations. It can be only one instance of this class.
    Provides methods to get the current translation for a given key.

    Translations are stored in i18n directory. Each language has its own
    directory with the translations files. The translations files are yaml files.

    Translations are stored in nested dictionaries. When the yaml file contains
    multiple levels, they are treated as 'context' for the defined translations.
    Contexts are not returned if they are defined in the yaml file but the
    translation is not found.

    Example without indentation(context):
    - (YAML file content | archetype.class.paragraph: "paragraph")
    - Translator().text("archetype.class.paragraph") -> "paragraph"
    - Translator().text("archetype.class.section") -> "archetype.class.section"

    Example with indentation(context), the context are defined in the yaml file:
    - (YAML file content | archetype: class: paragraph: "paragraph")
    - Translator().text("archetype.class.paragraph") -> "paragraph"
    - Translator().text("archetype.class.section") -> "section"
    """

    # Singleton instance
    __instance = None
    __lock = threading.Lock()  # Ensure thread safety

    # --------------------------------------------------------------------------
    # Method: __new__
    # Description: Singleton constructor for Translator class.
    # Date: 26/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        It creates a singleton instance for Translator class.
        """
        if not cls.__instance:
            log.info("Creating Translator instance")
            cls.__instance = super(Translator, cls).__new__(cls)
            cls.__instance._initialized = False
        return cls.__instance

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Constructor for Translator class.
    # Date: 26/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        It initializes the Translator class. It loads the translations for the
        current language.
        """
        # Check if the instance has been initialized
        with self.__class__.__lock:
            if self._initialized:
                return
            self._initialized = True

        # Proteus configuration
        self.config: Config = Config()
        self.current_language: str = self.config.language

        # Properties
        self._available_languages = None

        # Translations variable
        self._translations: Dict[str, dict] = {}

        # Load system translations ------------------------------
        system_lang_file: Path = self.config.i18n_directory / LANGUAGE_CONFIG_FILE
        system_translations_directory: Path = self._read_config_file(system_lang_file)

        assert (
            system_translations_directory is not None
        ), f"There was an error reading the language configuration file: {system_lang_file}. Could not find a valid language directory."

        self._load_translations(system_translations_directory)

        # Load archetype repository translations ----------------
        archetype_lang_file: Path = (
            self.config.archetypes_directory / 'i18n' / LANGUAGE_CONFIG_FILE
        )
        archetype_translations_directory: Path = self._read_config_file(
            archetype_lang_file
        )
        if archetype_translations_directory is not None:
            self._load_translations(archetype_translations_directory)

    # ==========================================================================
    # Properties
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: get_available_languages
    # Description: Returns the available languages for the application.
    # Date: 01/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @property
    def available_languages(self) -> List[str]:
        """
        Read the application configuration file located in the resources directory
        and returns the available languages for the application.

        Check if the language directory exists before adding it to the list of
        available languages.

        :return: List of available languages for the application. Empty list if
                    no languages are found.
        """
        if self._available_languages:
            return self._available_languages
        else:
            # Build the path to the language configuration file
            language_config_file: Path = (
                self.config.i18n_directory / LANGUAGE_CONFIG_FILE
            )

            # Read the language configuration file
            languages_tree: ET._ElementTree = ET.parse(language_config_file)
            languages_root: ET._Element = languages_tree.getroot()

            # List of available languages
            available_languages: List[str] = []

            # Iterate over the language tags
            for language in languages_root:
                # Get the language code
                language_code: str = language.get("key")

                # Get the language directory
                language_directory: str = language.get("path")

                # Check if the language path exists
                if language_directory is not None:
                    language_directory_path: Path = (
                        self.config.i18n_directory / language_directory
                    )
                    if language_directory_path.exists():
                        available_languages.append(language_code)

            # Store the available languages
            self._available_languages = available_languages
            return self._available_languages

    # ==========================================================================
    # Helper methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: _read_config_file
    # Description: Reads the language configuration file and returns the path
    #              to the translations directory.
    # Date: 01/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _read_config_file(self, language_config_file: Path) -> Path:
        """
        Reads the language configuration file and return the path to the lagnuage
        directory or file.

        Check if the language configuration file has the language entry for the
        current application language. If not, it returns the default language if
        it exists. If there is no default language or current language is not
        found, it returns None.

        :return: Path to the translations directory/file or None if not found any.
        """
        # Check if the language configuration file exists
        if not language_config_file.exists():
            log.error(f"Language configuration file not found: {language_config_file}")
            return None

        # Read the language configuration file
        languages_tree: ET._ElementTree = ET.parse(language_config_file)
        languages_root: ET._Element = languages_tree.getroot()

        # Get the default language directory if exists
        default_language_directory: str = languages_root.get("default")

        # Iterate over the language tags
        for language in languages_root:
            # If the key if the current language
            if language.get("key") == self.current_language:
                log.debug(
                    f"Configuration for language '{self.current_language}' found in file '{language_config_file}'"
                )

                # Get the language directory
                language_directory: str = language.get("path")

                # Check if the language directory exists
                if language_directory is not None:
                    language_directory_path: Path = (
                        language_config_file.parent / language_directory
                    )
                    if language_directory_path.exists():
                        return language_directory_path

        # If the current language is not found, return the default language if exists
        if default_language_directory is not None:
            default_language_directory_path: Path = Path(default_language_directory)
            if default_language_directory_path.exists():
                return default_language_directory_path
        else:
            return None

    # --------------------------------------------------------------------------
    # Method: _load_translations
    # Description: Loads the translations found in the given directory
    # Date: 26/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_translations(self, translations_path: Path) -> None:
        """
        Loads the translations files found in the given directory/file. It reads
        the yaml files and stores the translations in the _translations variable.
        Loads both .yaml and .yml files.

        Updates the _translations variable dictionary with the new translations.
        This means it overwrites the translations for the same key if repeated.

        :param translations_path: Path to the translations directory or file.
        """
        log.info(
            f"Loading translations from: {translations_path.as_posix()}"
        )

        # Check if the translations_path is a directory or a file
        if translations_path.is_dir():
            # Get all the yaml files in the directory
            translations_yaml_files: List[Path] = list(
                translations_path.rglob("*.yaml")
            )
            translations_yml_files: List[Path] = list(translations_path.rglob("*.yml"))
            translations_files: List[Path] = (
                translations_yaml_files + translations_yml_files
            )
        else:
            translations_files = [translations_path]

        # Iterate over the yaml files
        for file in translations_files:
            log.debug(f"Loading translations from file: {file.as_posix()}")

            # Read the yaml file
            with open(file, "r", encoding="utf-8") as f:
                translations: dict = yaml.safe_load(f)

                # Update the translations dictionary
                self._translations = self._recursive_translation_update(
                    self._translations, translations
                )

    # --------------------------------------------------------------------------
    # Method: _recursive_translation_update
    # Description: Recursively updates the translations dictionary with the
    #              given translations.
    # Date: 02/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _recursive_translation_update(
        self,
        stored_translations: dict,
        new_translations: dict,
        previous_context: str = "",
    ) -> Dict:
        """
        Update the stored_translations dictionary with the new_translations
        dictionary. It uses recursion to update the nested dictionaries avoiding
        overwriting the whole dictionary.

        :param stored_translations: Dictionary with the stored translations.
        :param new_translations: Dictionary with the new translations to update.
        :return: Dictionary with the updated translations.
        """
        # Copy so the original dictionary is not modified
        updated_translations: dict = stored_translations.copy()

        context: str  # Dict key, translation context
        value: dict | str  # Dict value, translation value str or another context dict

        # Iterate over the new translations to check if they should be updated
        for context, value in new_translations.items():
            # If context is not in the stored_translations, it can be directly added and return
            if context in stored_translations:
                
                context_value: str | dict = stored_translations[context]
                # If the context value is None, it means that it is a leaf node and it can be updated
                if context_value is None:
                    updated_translations[context] = value

                # If the value type do not match, it means that there might be an error in the file.
                # Contexts must be dictionaries and translations must be strings.
                elif isinstance(value, type(context_value)):
                    # For nested dictionaries, call the function recursively
                    if isinstance(value, dict):
                        updated_value = self._recursive_translation_update(
                            context_value, value, f"{previous_context}.{context}"
                        )
                        updated_translations[context] = updated_value

                    # For strings(leaf node), update the value
                    else:
                        updated_translations[context] = value

                # Log type mismatch to check for inconsistencies in the translations files
                else:
                    log.warning(
                        f"Type mismatch for translation '{previous_context}.{context}'."
                        f"Data stored in the context '{context}' will not be overwritten with new value."
                        f"Context type: {type(stored_translations[context])}, new value type: {type(value)}"
                    )
            else:
                updated_translations[context] = value

        return updated_translations

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: text
    # Description: Returns the translation for the given key.
    # Date: 02/02/2024
    # Version: 0.2
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def text(self, key: str, *args) -> str:
        """
        Returns the translation found for the given key. If no translation is
        found, it returns the key without the contexts found in the key.

        If there are arguments, they are formatted in the translation.

        :param key: Key to find the translation.
        :param args: Arguments to format the translation.
        """
        final_translation: str = key

        current_context_dict: dict = self._translations

        # Preprocess the key
        proccesed_key: str = key.lower().replace(" ", "_")

        # Check if the key is in the translations dictionary
        if proccesed_key in self._translations:
            final_translation = self._translations[proccesed_key]
        else:
            # If the key is not found, iterate splitting the key by the dots
            # and check if the key is in the translations dictionary
            dots_number: int = key.count(".")
            acumulated_context: str = (
                ""  # Used to restore the original key if no translation is found
            )
            while range(0, dots_number):
                key_parts: List[str] = proccesed_key.split(".", 1)

                # If list len is 1, it means that there are no more contexts
                # (no dots)
                context: str = key_parts[0]
                if len(key_parts) == 1:
                    proccesed_key = context
                else:
                    proccesed_key = key_parts[1]

                if context in current_context_dict:
                    acumulated_context += f"{context}."
                    # If the context is a dictionary, update the current_context_dict
                    if isinstance(current_context_dict[context], dict):
                        current_context_dict = current_context_dict[context]
                    # If the content is not a dictionary, it is the final translation
                    else:
                        final_translation = current_context_dict[context]
                        break
                else:
                    # If the translation is not found, remove the found contexts
                    final_translation = key.removeprefix(acumulated_context)
                    break

        # Check if there are arguments to format the translation
        if args:
            final_translation = final_translation.format(*args)

        return final_translation
