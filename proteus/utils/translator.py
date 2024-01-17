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

from typing import Dict
from pathlib import Path
import yaml
import logging
import threading

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils.config import Config

# logging configuration
log = logging.getLogger(__name__)

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
    file with yaml format.
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

        # Load translations
        self.load_translations()

    # --------------------------------------------------------------------------
    # Method: load_translations
    # Description: Loads the translations for the current language.
    # Date: 26/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def load_translations(self):
        """
        Loads the translations for the current language. Reads the yaml file
        for the given language and returns a dictionary with the translations.
        """
        log.info(f"Loading translations for {self.current_language}")

        # Build the path to the translations file
        translation_file: Path = (
            self.config.i18n_directory / f"{self.current_language}.yaml"
        )

        # Check if the translations file exists
        assert (
            translation_file.exists()
        ), f"Translations file for '{self.current_language}' not found: {translation_file}"

        # Read the translations file
        with open(translation_file, "r", encoding="utf-8") as file:
            self._translations: Dict[str, str] = yaml.full_load(file)

    # --------------------------------------------------------------------------
    # Method: text
    # Description: Returns the translation for the given key.
    # Date: 26/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def text(self, key: str, *args) -> str:
        """
        Returns the text for the given key. Text is already translated. If the
        key is not found in the translations file, it returns the key itself.

        Key is preprocessed, it is converted to lower case and spaces are
        replaced by underscores.

        If there are arguments, they are formatted in the translation.
        """
        # Check type of key
        assert isinstance(key, str), f"Language code key must be string type '{key}'"

        # Preprocess the key
        text_code: str = key.lower().replace(" ", "_")

        # Get the translation for the given key
        translation: str = ""
        try:
            translation = self._translations[text_code]
        except KeyError:
            # If translation not found return the key itself
            translation = key
            log.warning(f"Text not found for code '{text_code}' in '{self.current_language}' file.")

        # Check if there are arguments to format the translation
        if args:
            translation = translation.format(*args)
        
        return translation
