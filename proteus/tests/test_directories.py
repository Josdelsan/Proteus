# ==========================================================================
# File: test_directories.py
# Description: pytest file for the PROTEUS application directories
# Date: 10/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------
from proteus.application.configuration.config import Config
# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

def test_application_directories():
    """
    It tests that essential PROTEUS directories exist.
    """
    app : Config = Config()
    assert app.app_settings.resources_directory.is_dir()
    assert app.app_settings.icons_directory.is_dir()
    assert app.app_settings.i18n_directory.is_dir()
    assert app.app_settings.default_profile_directory.is_dir()

    assert app.profile_settings.archetypes_directory.is_dir()
    assert app.profile_settings.xslt_directory.is_dir()
