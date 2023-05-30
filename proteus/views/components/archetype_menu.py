# ==========================================================================
# File: archetype_menu.py
# Description: PyQT6 archetype menubar for the PROTEUS application
# Date: 29/05/2023
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

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QToolBar, \
                            QToolButton, QStyle, QApplication
from PyQt6.QtGui import QIcon

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.object import Object
from proteus.views.utils.decorators import subscribe_to
from proteus.controller.command_stack import Command


# --------------------------------------------------------------------------
# Class: ArchetypeMenu
# Description: PyQT6 archetype menu class for the PROTEUS application menu
# Date: 29/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@subscribe_to()
class ArchetypeMenu(QToolBar):
    """
    Archetype menu component for the PROTEUS application. It is used to
    display the object archetypes separated by classes in a tab menu.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.tab_widget = QTabWidget()

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the object archetype tab menu component
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the object archetype tab menu component. It creates a tab for
        each class of object archetypes.
        """

        object_archetypes_dict: Dict[
            str, List[Object]
        ] = Command.get_object_archetypes()
        for class_name in object_archetypes_dict.keys():
            self.add_tab(class_name, object_archetypes_dict[class_name])

        self.addWidget(self.tab_widget)

    def add_tab(self, class_name: str, object_archetypes: List[Object]) -> None:
        """ """
        archetypes_widget = QWidget()
        archetypes_layout = QHBoxLayout()

        for archetype in object_archetypes:
            archetype_widget = QToolButton(parent=archetypes_widget)
            archetype_widget.setToolTip(archetype.properties["name"].value)

            # TODO: Change the icon for the archetype icon
            icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
            archetype_widget.setIcon(QIcon(icon))

            archetype_widget.clicked.connect(
                lambda checked, arg=archetype.id: self.clone_archetype(arg)
            )

            archetypes_layout.addWidget(archetype_widget)

        archetypes_widget.setLayout(archetypes_layout)
        self.tab_widget.addTab(archetypes_widget, class_name)

    def clone_archetype(self, archetype_id: str) -> None:
        """ """
        print(archetype_id)
