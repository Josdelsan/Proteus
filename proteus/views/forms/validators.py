# ==========================================================================
# File: validators.py
# Description: Validators module for PROTEUS forms.
# Date: 23/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
import re

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

# ----------------------------------------------------------------------
# Function   : is_valid_folder_name
# Description: Check if a folder name is valid for the current operating
#              system.
# Date       : 05/06/2023
# Version    : 0.1
# Author     : José María Delgado Sánchez
# ----------------------------------------------------------------------
def is_valid_folder_name(folder_name) -> bool:
    """
    Check if a folder name is valid for the current operating system.
    """
    # Check for forbidden characters
    forbidden_characters = re.compile(r'[<>:"/\\|?*]')
    if forbidden_characters.search(folder_name):
        return False

    # Check for reserved names on Windows
    if os.name == 'nt':
        reserved_names = re.compile(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]|CON\..*|PRN\..*|AUX\..*|NUL\..*|COM[1-9]\..*|LPT[1-9]\..*)', re.IGNORECASE)
        if reserved_names.match(folder_name):
            return False

    # Check for reserved names on Linux and macOS (reserved characters are allowed on Unix-like systems)
    if os.name == 'posix':
        reserved_names = {'/dev', '/proc', '/sys', '/tmp', '/run', '/var'}
        if folder_name in reserved_names or folder_name.startswith('/'):
            return False

    return True
