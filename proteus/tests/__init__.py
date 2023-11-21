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

import yaml

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_APP_PATH

# --------------------------------------------------------------------------

PROTEUS_TEST_PATH = PROTEUS_APP_PATH / "proteus/tests"
PROTEUS_SAMPLE_DATA_PATH = PROTEUS_TEST_PATH / "sample_data"

# Sample data mapping file
PROTEUS_SAMPLE_DATA_FILE = PROTEUS_SAMPLE_DATA_PATH / "sample_data_map.yaml"
sample_data: dict = None
with open(PROTEUS_SAMPLE_DATA_FILE, "r") as f:
    sample_data = yaml.safe_load(f)