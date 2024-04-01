# ==========================================================================
# File: __init__.py
# Description: module initialization for the tests of the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
#         José María Delgado Sánchez 
# ==========================================================================
# Update: 12/04/2023 (José María)
# Description:
# - Created constants for the test directory path and the sample
#   data directory path.
# ==========================================================================

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_APP_PATH

# --------------------------------------------------------------------------

PROTEUS_SAMPLE_PROJECTS_PATH = PROTEUS_APP_PATH / "proteus/tests/sample_data" # Sample data directory

# Icons
PROTEUS_SAMPLE_ICONS_PATH = PROTEUS_SAMPLE_PROJECTS_PATH / "icons"

# Projects
PROTEUS_SAMPLE_PROJECTS_PATH = PROTEUS_SAMPLE_PROJECTS_PATH / "projects"
PROTEUS_PROJECT_DATA_FILE = PROTEUS_SAMPLE_PROJECTS_PATH / "sample_data_map.yaml" # Sample data mapping file
