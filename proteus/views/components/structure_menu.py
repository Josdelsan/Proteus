# ==========================================================================
# File: project_strcuture_manager.py
# Description: PyQT6 menu manager for the PROTEUS application project menu
# Date: 16/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass
from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QTabWidget

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.services.service_manager import ServiceManager
from proteus.views.utils.decorators import component

# --------------------------------------------------------------------------
# Class: MenuManager
# Description: PyQT6 menu manager class for the PROTEUS application menus
# Date: 16/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@component(QTabWidget)
@dataclass(init=False)
class StructureMenu():
    """ """

    def create_component(self) -> QTabWidget:
        """ """

        # TODO: This is a temporary solution for testing purposes
        if self.project_service.project is None:
            pass
        else:
            project_structure = self.project_service.get_project_structure()
            for tab_name in project_structure:
                self.add_tab(tab_name)
        
        
    def add_tab(self, tab_name):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabels(["Document"])

        # Document structure
        doc_structure = self.project_service.get_object_structure(tab_name)
        doc_children : List = doc_structure[tab_name]

        root_item = QTreeWidgetItem(tree_widget, [tab_name])
        self.populate_tree(root_item, doc_children)

        tab_layout.addWidget(tree_widget)
        tab.setLayout(tab_layout)

        self.addTab(tab, tab_name)

    def populate_tree(self, parent_item, children):
        for child in children:
            child_id = list(child.keys())[0]
            child_item = QTreeWidgetItem(parent_item, [child_id])
            self.populate_tree(
                child_item, child[child_id]
            ) 
