# ==========================================================================
# File: document_list.py
# Description: PyQT6 documents tab menu component for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict, List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QSizePolicy, QSplitter, QLabel

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.views.utils.decorators import subscribe_to, trigger_on
from proteus.views.utils.event_manager import Event, EventManager
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.document_render import DocumentRender
from proteus.controller.command_stack import Controller


# --------------------------------------------------------------------------
# Class: DocumentList
# Description: PyQT6 documents tab menu component for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DocumentList(QTabWidget):
    """
    Documents tab menu component for the PROTEUS application. It is used to
    display the documents of the project in a tab menu. It also manages the
    creation of the document tree component and render for each document.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        
        # Tabs dictionary
        self.tabs : Dict[ProteusID, QWidget] = {}

        # Tab children
        # NOTE: Store children components of each tab in a dictionary to
        #       delete them later
        self.tab_children : Dict[ProteusID, List] = {}

        # Create the component
        self.create_component()

        # Subscribe to events
        EventManager.attach(Event.ADD_DOCUMENT, self.update_on_add_document, self)
        EventManager.attach(Event.DELETE_DOCUMENT, self.update_on_delete_document, self)
        EventManager.attach(Event.MODIFY_OBJECT, self.update_on_modify_object, self)

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the documents tab menu component
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """ """
        # Get project structure from project service
        project_structure = Controller.get_project_structure()

        # Add a document tab for each document in the project
        for document in project_structure:
            self.add_document(document)

        proteus.logger.info("Document list tabs component created")

        
    # ----------------------------------------------------------------------
    def update_on_add_document(self, *args, **kwargs) -> None:
        new_document = kwargs.get("document")
        self.add_document(new_document)

    # ----------------------------------------------------------------------
    def update_on_delete_document(self, *args, **kwargs) -> None:
        document_id = kwargs.get("element_id")

        # Delete tab from tabs widget
        document_tab = self.tabs.get(document_id)
        self.removeTab(self.indexOf(document_tab))

        # Delete child components
        for child_component in self.tab_children.get(document_id):
            child_component.delete_component()

        # Delete tab object
        document_tab.parent = None
        document_tab.deleteLater()

    # ----------------------------------------------------------------------
    def update_on_modify_object(self, *args, **kwargs) -> None:
        element_id = kwargs.get("element_id")

        # Check if exists a tab for the element
        if element_id in self.tabs:
            # Get document tab
            document_tab = self.tabs.get(element_id)

            # Change tab name
            element: Object = Controller.get_element(element_id)
            document_name: str = element.get_property("name").value
            self.setTabText(self.indexOf(document_tab), document_name)

    
    # ----------------------------------------------------------------------
    # Method     : add_document
    # Description: Add a document to the tab menu creating its child
    #              components (tree and render).
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_document(self, document: Object):
        """
        Add a document to the tab menu creating its child components (tree and
        render).
        """
        # Create document tab widget
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        # Splitter
        splitter = QSplitter()
        splitter.setStyleSheet("QSplitter::handle { background-color: #666666; }")

        # Tree widget
        document_tree = DocumentTree(self, document.id)
        document_tree.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        splitter.addWidget(document_tree)

        document_render = DocumentRender(self, document.id)
        document_render.setStyleSheet("background-color: #FFFFFF;")
        document_render.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        splitter.addWidget(document_render)

        # Add splitter with tree and render to tab layout
        tab_layout.addWidget(splitter)
        tab.setLayout(tab_layout)

        # Add tab to the dictionary
        self.tabs[document.id] = tab
        self.tab_children[document.id] = [document_tree, document_render]

        document_name = document.get_property("name").value
        self.addTab(tab, document_name)
