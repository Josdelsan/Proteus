# ==========================================================================
# File: __init__.py
# Description: module initialization for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging

# --------------------------------------------------------------------------
# Constant declarations for PROTEUS logger name
# --------------------------------------------------------------------------

PROTEUS_LOGGER_NAME    = str('proteus')
PROTEUS_LOGGING_FORMAT = str('%(name)s:%(filename)s [%(levelname)s] -> %(message)s')

# --------------------------------------------------------------------------
# Logger configuration
# --------------------------------------------------------------------------

logging.basicConfig(
    level=logging.DEBUG, 
    format=PROTEUS_LOGGING_FORMAT)

logger = logging.getLogger(PROTEUS_LOGGER_NAME)

