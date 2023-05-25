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

from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QSizePolicy, QSplitter

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.utils.decorators import component
from proteus.views.utils.event_manager import Event
from proteus.views.components.document_tree import DocumentTree


# --------------------------------------------------------------------------
# Class: DocumentList
# Description: PyQT6 documents tab menu component for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@component(QTabWidget, [Event.OPEN_PROJECT])
class DocumentList():
    """
    Documents tab menu component for the PROTEUS application. It is used to
    display the documents of the project in a tab menu. It also manages the
    creation of the document tree component and render for each document.
    """

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the documents tab menu component
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> QTabWidget:
        """ """
        pass

    # ----------------------------------------------------------------------
    # Method     : update_component
    # Description: Update the documents tab menu component
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self, *args, **kwargs) -> None:
        """
        Update the documents tab menu component.
        """
        # Get project structure from project service
        project_structure = self.project_service.get_project_structure()

        # Add a document tab for each document in the project
        for tab_name in project_structure:
            self.add_document(tab_name)


    # ----------------------------------------------------------------------
    # Method     : add_document
    # Description: Add a document to the tab menu creating its child
    #              components (tree and render).
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_document(self, tab_name):
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
        document_tree = DocumentTree(tab_name, self)
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


        tab_layout.addWidget(splitter)
        tab.setLayout(tab_layout)

        self.addTab(tab, tab_name)