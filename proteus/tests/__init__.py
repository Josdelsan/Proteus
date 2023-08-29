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

PROTEUS_TEST_PATH = PROTEUS_APP_PATH / "proteus/tests"
PROTEUS_TEST_SAMPLE_DATA_PATH = PROTEUS_TEST_PATH / "sample_data"