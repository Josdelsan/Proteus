# ==========================================================================
# File: __init__.py
# Description: module initialization for the PROTEUS utils package
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# XSLT templates config file tags and attributes
TEMPLATE_TAG = "template"
ENTRY_POINTS_TAG = "entryPoints"
ENTRY_POINT_TAG = "entryPoint"
DEPENCENCIES_TAG = "dependencies"
PLUGIN_DEPENDENCY_TAG = "pluginDependency"

NAME_ATTRIBUTE = "name"
LANGUAGE_ATTRIBUTE = "language"
FILE_ATTRIBUTE = "file"
DEFAULT_ATTRIBUTE = "default"

# PyQt6 Search Paths
RESOURCES_SEARCH_PATH = "resources"
TEMPLATE_DUMMY_SEARCH_PATH = "templates"
ASSETS_DUMMY_SEARCH_PATH = "assets"

# Proteus Icons
from strenum import StrEnum

DEFAULT_ICON_KEY = ":Proteus-default-icon"

class ProteusIconType(StrEnum):
    App = "app"
    MainMenu = "main_menu"
    Archetype = "archetype"
    Repository = "repository"
    Document = "document"