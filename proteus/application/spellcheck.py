# ==========================================================================
# File: spellcheck.py
# Description: Spellchecker utilities for the PROTEUS application.
# Date: 08/05/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import re
from typing import Iterator

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from spellchecker import SpellChecker
from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.utils.abstract_meta import SingletonMeta

# --------------------------------------------------------------------------
# Class: SpellCheckerWrapper
# Description: Spellchecker wrapper class.
# Date: 08/05/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class SpellCheckerWrapper(metaclass=SingletonMeta):
    """
    Spellchecker wrapper class. It is used to check the spelling of a text.

    Current implementation uses pyspellchecker library.
    """

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Constructor method.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self, language: str = "en"):
        """
        Constructor method.
        """

        assert language in SpellChecker.languages(), (
            f"Language '{language}' is not available for spellchecking. "
            f"Available languages are: {', '.join(SpellChecker.languages())}"
        )

        self._spellchecker = SpellChecker(language=language)

    # --------------------------------------------------------------------------
    # Method: list_available_languages
    # Description: List available languages for spellchecking.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def list_available_languages(self) -> list[str]:
        """
        List available languages for spellchecking.

        return: List of available languages dictionaries.
        """
        return list(SpellChecker.languages())
    
    # --------------------------------------------------------------------------
    # Method: check
    # Description: Check the spelling of a word.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def check(self, word: str) -> bool:
        """
        Check the spelling of a word. Returns True if the word is spelled correctly.

        param word: word to check.
        return: True if the word is spelled correctly, False otherwise.
        """
        return word in self._spellchecker
    
    # --------------------------------------------------------------------------
    # Method: suggest
    # Description: Get a list of suggested words for a misspelled word.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def suggest(self, word: str) -> list[str]:
        """
        Get a list of suggested words for a misspelled word.

        param text: Text to get suggestions.
        return: List of suggested words.
        """
        candidates = self._spellchecker.candidates(word)
        if candidates:
            return list(candidates)
        else:
            return list()
        
    
    # --------------------------------------------------------------------------
    # Method: tokenize (static)
    # Description: Tokenize a text into words.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    # TODO: Ommit email addresses and URLs
    # TODO: Improve code block handling
    @staticmethod
    def tokenize(text: str) -> Iterator[re.Match]:
        """
        Tokenize a text into words.

        param text: Text to tokenize.
        return: List of matches.
        """
        tokenize_pattern = re.compile(r"\b(?<!`)[A-Za-z]{2,}(?!`)(?!>)\b")

        return re.finditer(tokenize_pattern, text)
    

# --------------------------------------------------------------------------
# Class: SpellCheckHighlighter
# Description: Syntax highlighter for spellchecking.
# Date: 08/05/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class SpellCheckHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter for spellchecking. It is used to highlight
    misspelled words in the text.
    """        

    # --------------------------------------------------------------------------
    # Method: highlightBlock
    # Description: Highlight misspelled words in the text.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def highlightBlock(self, text: str) -> None:

        if not hasattr(self, "_spellchecker"):
            self._spellchecker = SpellCheckerWrapper()

        highlight_format = QTextCharFormat()
        highlight_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        highlight_format.setUnderlineColor(Qt.GlobalColor.red)
        
        for match in self._spellchecker.tokenize(text):
            word = match.group()
            if not self._spellchecker.check(word):
                self.setFormat(match.start(), match.end() - match.start(), highlight_format)