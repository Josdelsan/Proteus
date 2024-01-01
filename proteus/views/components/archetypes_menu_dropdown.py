# ==========================================================================
# File: archetypes_menu_dropdown.py
# Description: PyQT6 menu dropdown component.
# Date: 01/09/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QMenu,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.views import ARCHETYPE_MENU_ICON_TYPE
from proteus.model.object import Object
from proteus.views.components.abstract_component import ProteusComponent


# --------------------------------------------------------------------------
# Class: ArchetypesMenuDropdown
# Description: Class for the PROTEUS application context menu.
# Date: 01/09/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ArchetypesMenuDropdown(QMenu, ProteusComponent):
    """
    Class for the PROTEUS archetypes dropdown menu. It is used to create
    a dropdown menu given a list of archetypes. The dropdown menus will
    be shown in the main menu. Each archetype will be shown as an action.

    Clone action is connected to each archetype in the list. They will
    be cloned in the current selected object.

    This class is only responsible for the dropdown menu, the button that
    will show the dropdown menu is created in the MainMenu component.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 01/09/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self, archetype_list: List[Object], *args, **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component.

        :param archetype_list: List of archetypes to be shown in the dropdown menu.
        """
        super(ArchetypesMenuDropdown, self).__init__(*args, **kwargs)

        # Store the archetype list
        self._archetype_list = archetype_list

        # Store actions by archetype id
        self.actions: Dict[ProteusID, QAction] = {}

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component.
    # Date       : 01/09/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the component. Using the provided archetype list, create
        a dropdown menu with each archetype as an action.

        Each action is connected to the clone_object method of the controller.
        The cloned object parent will be the current selected object. By
        default, every object will use class icon as the action icon.
        """
        for archetype in self._archetype_list:
            arch_class = archetype.classes[-1]
            clone_action = QAction(
                # Name translation might not be needed for archetypes
                archetype.get_property(PROTEUS_NAME).value,
            )
            icon: QIcon = QIcon(
                self._config.get_icon(ARCHETYPE_MENU_ICON_TYPE, arch_class).as_posix()
            )
            clone_action.setIcon(icon)
            clone_action.triggered.connect(
                lambda checked, arg=archetype.id: self._controller.create_object(
                    archetype_id=arg, parent_id=self._state_manager.get_current_object()
                )
            )
            self.addAction(clone_action)
            self.actions[archetype.id] = clone_action

    # ======================================================================
    # Component slots methods (connected to the component signals and helpers)
    # ======================================================================

    # ======================================================================
    # Component static methods (create and show the form window)
    # ======================================================================
