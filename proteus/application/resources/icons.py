# ==========================================================================
# File: dynamic_icons.py
# Description: Manage the icons for PROTEUS application.
# Date: 12/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict
from pathlib import Path
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from strenum import StrEnum
from lxml import etree as ET
from PyQt6.QtGui import QIcon

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.utils.abstract_meta import SingletonMeta

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

ICONS_FILE: str = "icons.xml"
DEFAULT_ICON_KEY = ":Proteus-default-icon"


# --------------------------------------------------------------------------
# Class: ProteusIconType
# Description: Enum for PROTEUS icon types
# Date: 15/03/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ProteusIconType(StrEnum):
    App = "app"
    MainMenu = "main_menu"
    Archetype = "archetype"
    Profile = "profile"
    Document = "document"


# --------------------------------------------------------------------------
# Class: Icons
# Description: Manage the icons for PROTEUS application
# Date: 12/02/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class Icons(metaclass=SingletonMeta):
    """
    Handle PROTEUS icons. It can load icons from directories that contain
    an icons configuration file 'icons.xml'. The icons configuration file
    must contain the following structure:

    <icons>
        <type name="type_name" default="default_icon">
            <icon key="icon_key" file="icon_file"/>
            ...
        </type>
        ...
    </icons>

    Where:
    - type_name: Icon type name. It must be a valid ProteusIconType.
    - default_icon: Default icon for the type. It is optional.
    - icon_key: Icon key.
    - icon_file: Icon file path.

    The icons configuration file must be located in the icons directory.

    All the repeated values (included default) defined in the icons file inside
    the profile will override the values defined in the resources
    directory. This allows maintaining default values in the application while
    it is possible to override them.

    This class uses memoization to store the icons already instantiated as
    QIcon objects.
    """

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Constructor for Icons class.
    # Date: 26/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initializes the Icons class.
        """
        # Icons variable
        self._icons_paths: Dict[ProteusIconType, Dict[str, Path]] = {}

        # Icons memo
        self._icons_memo: Dict[ProteusIconType, Dict[str, QIcon]] = {}
        for icon_type in ProteusIconType:
            self._icons_memo[icon_type] = {}

    # ==========================================================================
    # Helper methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: _load_icons
    # Description: Loads the icons from the given directory
    # Date: 12/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _load_icons(self, icons_path: Path) -> None:
        """
        Loads the icons configuration file 'icons.xml' from the given directory.
        Stores the icons paths found in the configuration file. 

        :param icons_path: Path to the icons directory.
        """

        # Parse icons file
        icons_file: Path = icons_path / ICONS_FILE
        resources_icons_tree: ET._ElementTree = ET.parse(icons_file)
        resources_icons_root: ET._Element = resources_icons_tree.getroot()

        # Iterate over icons tag children (type tag) to create each type dictionary
        for type_tag in resources_icons_root.iterchildren():
            # Get name attribute to check if it is a valid icon type
            type_name: str = type_tag.attrib.get("name", None)

            # Check if type name is a valid ProteusIconType
            assert (
                type_name in ProteusIconType._member_map_.values()
            ), f"Icon type '{type_name}' is not a valid ProteusIconType, check {icons_file.as_posix()} file."

            # Initialize type dictionary
            type_dictionary: Dict[str, Path] = {}

            # Get the default icon and store if it exists
            default_icon: str = type_tag.attrib.get("default", None)
            if default_icon is not None:
                type_dictionary[DEFAULT_ICON_KEY] = icons_path / default_icon
                log.warning(
                    f"Default icon not found for icon type '{type_name}'. This could crash the application. Check {icons_path.as_posix()} file."
                )

            # Iterate over icons tag children icon
            for icon in type_tag.iterchildren():
                # Get key and file attributes for the icon tag
                key = icon.attrib.get("key", None)
                file = icon.attrib.get("file", None)

                if key is None or key == "" or file is None or file == "":
                    log.error(
                        f"Icon key or file are not correctly defined for icon type '{type_name}'. Check {icons_path.as_posix()} file. Key value: {key}, File value: {file}"
                    )
                    continue

                # Check if icon file exists
                file_path: Path = icons_path / file
                if not file_path.exists():
                    log.error(
                        f"Icon file '{file_path}' does not exist. Check {icons_path.as_posix()} file."
                    )
                    continue

                # Add icon to type dictionary
                type_dictionary[key] = file_path

            # Update icons paths dictionary
            if type_name in self._icons_paths:
                self._icons_paths[type_name].update(type_dictionary)
            else:
                self._icons_paths[type_name] = type_dictionary

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: load_icons
    # Description: Load the system icons
    # Date: 12/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def load_icons(self, icons_directory: Path) -> bool:
        """
        Loads the icons from the given directory. Returns True if the icons
        were loaded successfully, False otherwise.

        :param icons_directory: Path to the icons directory.

        :return: True if the icons were loaded successfully, False otherwise.
        """

        if icons_directory is None:
            log.error("Icons directory is None.")
            return False

        if icons_directory.exists() and icons_directory.is_dir():
            try:
                self._load_icons(icons_directory)
                return True
            except Exception as e:
                log.error(f"Error loading icons: {e}")
                return False
        else:
            log.error(f"Icons directory '{icons_directory}' does not exist.")
            return False

    # --------------------------------------------------------------------------
    # Method: icon_path
    # Description: Returns the icon path for the given key and type
    # Date: 12/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def icon_path(
        self, type: ProteusIconType, key: str = DEFAULT_ICON_KEY
    ) -> Path | None:
        """
        It returns the icon path for the given type and key.

        :param type: Icon type.
        :param key: Icon key.
        """
        try:
            # Check if key exists
            if key not in self._icons_paths[type]:
                log.warning(
                    f"Icon key '{key}' not found for type '{type}', using default icon"
                )
                key = DEFAULT_ICON_KEY

            # Default icon may not exist, log a critical message
            icon_path = self._icons_paths[type].get(key, None)
            if icon_path is None:
                log.critical(
                    f"Icon path not found for type '{type}' and key '{key}', check default icons."
                )

            return icon_path

        except KeyError:
            log.critical(f"Type {type} not found in dynamic icons dictionary.")
            return None

    # --------------------------------------------------------------------------
    # Method: icon
    # Description: Returns the icon for the given key and type
    # Date: 12/02/2024
    # Version: 0.2
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def icon(self, type: ProteusIconType, key: str = DEFAULT_ICON_KEY) -> QIcon:
        """
        It returns the icon (QIcon) for the given type and key.

        :param type: Icon type.
        :param key: Icon key.
        """
        # Check if icon is already in memo
        if key in self._icons_memo[type]:
            return self._icons_memo[type][key]
        
        icon_path = self.icon_path(type, key)
        icon = QIcon(icon_path.as_posix()) if icon_path else QIcon()
        self._icons_memo[type][key] = icon
        return icon
