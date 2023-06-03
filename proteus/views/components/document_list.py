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

from typing import Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QSizePolicy, QSplitter

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.views.utils.decorators import subscribe_to
from proteus.views.utils.event_manager import Event
from proteus.views.components.document_tree import DocumentTree
from proteus.controller.command_stack import Controller


# --------------------------------------------------------------------------
# Class: DocumentList
# Description: PyQT6 documents tab menu component for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@subscribe_to([Event.CLONE_DOCUMENT, Event.DELETE_DOCUMENT])
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

        # Create the component
        self.create_component()

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

    # ----------------------------------------------------------------------
    # Method     : update_component
    # Description: Update the documents tab menu component
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self, event, *args, **kwargs) -> None:
        """
        Update the documents tab menu component.
        """
        # Handle events
        match event:
            # ------------------------------------------------
            # Event: STACK_CHANGED
            # Description: Disable or enable main menu buttons
            # ------------------------------------------------
            case Event.CLONE_DOCUMENT:
                new_document = kwargs.get("cloned_document")
                self.add_document(new_document)

            case Event.DELETE_DOCUMENT:
                document_id = kwargs.get("element_id")
                self.removeTab(self.indexOf(self.tabs[document_id]))
                self.tabs[document_id].deleteLater()
        

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

        container2 = QWidget()
        container2.setStyleSheet("background-color: #FFFFFF;")
        container2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        splitter.addWidget(container2)

        # Add splitter with tree and render to tab layout
        tab_layout.addWidget(splitter)
        tab.setLayout(tab_layout)

        # Add tab to the dictionary
        self.tabs[document.id] = tab

        document_name = document.get_property("name").value
        self.addTab(tab, document_name)
