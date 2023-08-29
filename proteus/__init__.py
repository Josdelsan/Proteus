# ==========================================================================
# File: __init__.py
# Description: module initialization for the PROTEUS application
# Date: 18/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from pathlib import Path
import sys

# --------------------------------------------------------------------------
# Constant declarations for PROTEUS logger name
# --------------------------------------------------------------------------

PROTEUS_LOGGER_NAME    = str('proteus')
PROTEUS_LOGGING_FORMAT = str('%(name)s:%(filename)s [%(levelname)s] -> %(message)s')

# --------------------------------------------------------------------------
# Logger configuration
# --------------------------------------------------------------------------

# logging levels =     
#   NOTSET=0
#   DEBUG=10
#   INFO=20
#   WARN=30
#   ERROR=40
#   CRITICAL=50

logging.basicConfig(
    #filename=PROTEUS_LOGGER_NAME+'.log',
    #filemode='a',    
    level=logging.DEBUG, 
    format=PROTEUS_LOGGING_FORMAT
)

logger = logging.getLogger(PROTEUS_LOGGER_NAME)

# --------------------------------------------------------------------------
# Application absolute path
# --------------------------------------------------------------------------

# NOTE: this is a workaround for the PyInstaller application. It is needed
#       for the application to work properly when it is packaged as one file.

PROTEUS_APP_PATH = Path(getattr(sys, '_MEIPASS', Path().parent.absolute()))
