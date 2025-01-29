# ==========================================================================
# File: autocompleter.py
# Description: Autocompleter module for TextEdit autocompletion plugins
# Date: 28/01/2025
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Class: AutocompleterInterface
# Date: 28/01/2025
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class AutocompleterInterface(ABC):
    """
    Interface for Autocompleter classes. Defines the methods that autocompleter
    components should implement in order to work with TextEdit widget.

    Autocompleter can be added as plugins and can be selected in the app config.
    """

    @abstractmethod
    def autocomplete(current_string: str, context: str = "") -> List[str]:
        """_summary_

        :param str current_string: Main context
        :param str context: Addtional context, defaults to ""
        :return List[str]: List of suggestions
        """
        pass