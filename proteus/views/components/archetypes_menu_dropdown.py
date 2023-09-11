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
    QApplication,
    QTreeWidget,
    QTreeWidgetItem,
    QStyle,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.views import ARCHETYPE_MENU_ICON_TYPE
from proteus.config import Config
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.controller.command_stack import Controller
from proteus.views.utils.translator import Translator
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.views.utils.state_manager import StateManager


# --------------------------------------------------------------------------
# Class: ArchetypesMenuDropdown
# Description: Class for the PROTEUS application context menu.
# Date: 01/09/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ArchetypesMenuDropdown(QMenu):
    """
    Class for the PROTEUS application context menu.
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
        self, controller: Controller, archetype_list: List[Object], *args, **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the page object and the controller instance.
        """
        super().__init__(*args, **kwargs)

        assert controller is not None, "Controller cannot be None"

        # Dependencies
        self._controller = controller
        self._archetype_list = archetype_list
        self.translator = Translator()

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
        Create the component.
        """
        for archetype in self._archetype_list:
            arch_class = archetype.classes[-1]
            clone_action = QAction(
                self.translator.text(archetype.get_property("name").value)
            )
            icon: QIcon = QIcon(Config().get_icon(ARCHETYPE_MENU_ICON_TYPE, arch_class).as_posix())
            clone_action.setIcon(icon)
            clone_action.triggered.connect(
                lambda checked, arg=archetype.id: self._controller.create_object(
                    archetype_id=arg, parent_id=StateManager.get_current_object()
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



