# ==========================================================================
# File: copilot.py
# Description: This is a simple mockup of how an autocompleter could be implemented
# Date: 28/01/2025
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import random
import time

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Plugin imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Proteus imports
# --------------------------------------------------------------------------

from proteus.application.utils.autocompleter import AutocompleterInterface


class CopilotExample(AutocompleterInterface):

    MOCK_STRING = "this is an example suggestion"

    def autocomplete(self, current_string: str, context: str = ""):
        random_num = random.randint(0, 100)
        sug = current_string + self.MOCK_STRING + " " + str(random_num)
        # time.sleep(3)
        return [sug]
