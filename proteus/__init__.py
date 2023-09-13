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
import datetime
from logging.handlers import TimedRotatingFileHandler

# --------------------------------------------------------------------------
# Application absolute path
# --------------------------------------------------------------------------

# NOTE: this is a workaround for the PyInstaller application. It is needed
#       for the application to work properly when it is packaged as one file.

PROTEUS_APP_PATH = Path(getattr(sys, '_MEIPASS', Path().parent.absolute()))

# --------------------------------------------------------------------------
# Constant declarations for PROTEUS logger name
# --------------------------------------------------------------------------

PROTEUS_LOGGER_NAME    = str('proteus')
PROTEUS_LOGGING_FORMAT = str('%(name)s:%(filename)s [%(levelname)s] -> %(message)s')
PROTEUS_LOGGING_DIR    = PROTEUS_APP_PATH / '.proteus'

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

# Create a logger
logger = logging.getLogger(PROTEUS_LOGGER_NAME)
logger.setLevel(logging.DEBUG)

# Create directory for log files
if not PROTEUS_LOGGING_DIR.exists():
    PROTEUS_LOGGING_DIR.mkdir()

# Define a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a TimedRotatingFileHandler to create log files based on date and time
log_filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
file_handler = TimedRotatingFileHandler(
    filename=f'{PROTEUS_LOGGING_DIR}/{log_filename}',
    when='midnight',
    interval=1,
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

