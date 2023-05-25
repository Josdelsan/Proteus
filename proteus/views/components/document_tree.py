# ==========================================================================
# File: document_tree.py
# Description: PyQT6 document structure tree component for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.utils.decorators import component
from proteus.views.utils.event_manager import Event


# --------------------------------------------------------------------------
# Class: DocumentTree
# Description: PyQT6 document structure tree component class for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@component(QWidget)
class DocumentTree():
    """
    Document structure tree component for the PROTEUS application. It is used
    to manage the creation of the document structure tree and its actions.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Constructor for the document structure tree component, it
    #              adds the document id to the component.
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, document_id : str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.document_id = document_id

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the document tree for each document in the project
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the document tree for each document in the project.
        """
        layout = QVBoxLayout(self)

        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabels([self.document_id])

        structure : Dict = self.project_service.get_object_structure(self.document_id)
        top_level_items = structure[self.document_id]

        for item in top_level_items:
            item_id = list(item.keys())[0]
            item_widget = QTreeWidgetItem([item_id])
            self.populate_tree(item_widget, item[item_id])
            tree_widget.addTopLevelItem(item_widget)

        layout.addWidget(tree_widget)
        self.setLayout(layout)


    # ----------------------------------------------------------------------
    # Method     : update_component
    # Description: Update the document tree for each document in the project
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self, *args, **kwargs) -> None:
        """ """
        pass

    # ----------------------------------------------------------------------
    # Method     : populate_tree
    # Description: Populate document tree given the document structure
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def populate_tree(self, parent_item, children):
        for child in children:
            child_id = list(child.keys())[0]
            child_item = QTreeWidgetItem(parent_item, [child_id])
            self.populate_tree(
                child_item, child[child_id]
            ) 

        