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

from typing import Dict, List, Union
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QSizePolicy, QSplitter

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.views.utils.event_manager import Event, EventManager
from proteus.views.utils.state_manager import StateManager
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.document_render import DocumentRender
from proteus.controller.command_stack import Controller

# logging configuration
log = logging.getLogger(__name__)

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
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.

        Store the tabs for each document in a dictionary to access them
        later. Also store the children components of each tab in a
        dictionary to delete when the tab is closed.
        """
        super().__init__(parent, *args, **kwargs)

        # Tabs dictionary
        self.tabs: Dict[ProteusID, QWidget] = {}

        # Tab children
        # NOTE: Store children components of each tab in a dictionary to
        #       delete them later
        self.tab_children: Dict[ProteusID, List] = {}

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
        """
        Create the documents tab menu component. It gets the project
        structure from the controller and creates a tab for each
        document.
        """
        # Get project structure from project service
        project_structure: List[Object] = Controller.get_project_structure()

        # Add a document tab for each document in the project
        for document in project_structure:
            self.add_document(document)

        # Connect singal to handle document tab change
        self.currentChanged.connect(self.current_document_changed)
        # Call the current document changed method to update the document for the
        # first time
        self.current_document_changed(index=0)

        log.info("Document list tabs component created")

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
        render). Document tab consists of a widget that contains the document
        tree and render components separated by a splitter.
        """
        # Create document tab widget
        tab: QWidget = QWidget()
        tab_layout: QHBoxLayout = QHBoxLayout(tab)

        # Splitter
        splitter: QSplitter = QSplitter()
        splitter.setStyleSheet("QSplitter::handle { width: 4px; background-color: #666666; }")

        # Tree widget --------------------------------------------------------
        document_tree: DocumentTree = DocumentTree(self, document.id)
        document_tree.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred
        )
        document_tree.setMinimumWidth(200)

        # Render widget ------------------------------------------------------
        document_render: DocumentRender = DocumentRender(self, document.id)
        document_render.setStyleSheet("background-color: #FFFFFF;")
        document_render.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        document_render.setMinimumWidth(400)

        # Add tree and render to splitter
        splitter.addWidget(document_tree)
        splitter.addWidget(document_render)
        # NOTE: By default the splitter is 1200px wide when the application
        #       is launched. We set the initial sizes proportionally to the
        #       splitter size to avoid the render component to be too small
        splitter.setSizes([300, 900])

        # Add splitter with tree and render to tab layout
        tab_layout.addWidget(splitter)
        tab.setLayout(tab_layout)

        # Add tab to the dictionary
        self.tabs[document.id] = tab
        self.tab_children[document.id] = [document_tree, document_render]

        document_name: str = document.get_property("name").value
        self.addTab(tab, document_name)

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_on_add_document
    # Description: Update the documents tab menu component when a new
    #              document is added to the project.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_add_document(self, *args, **kwargs) -> None:
        """
        Update the documents tab menu component when a new document is added
        to the project. It creates a new tab for the document using the add
        document method.

        Triggered by: Event.ADD_DOCUMENT
        """
        new_document: Object = kwargs.get("document")

        # Check the document is instance of Object
        # Check the object is instance of Object
        assert isinstance(
            new_document, Object
        ), "Object is not instance of Object on ADD_DOCUMENT event"

        self.add_document(new_document)

    # ----------------------------------------------------------------------
    # Method     : update_on_delete_document
    # Description: Update the documents tab menu component when a document
    #              is deleted from the project.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_delete_document(self, *args, **kwargs) -> None:
        """
        Update the documents tab menu component when a document is deleted
        from the project. It deletes the tab from the tabs widget and
        deletes the child components.

        Triggered by: Event.DELETE_DOCUMENT
        """
        document_id: ProteusID = kwargs.get("element_id")

        # Check the element id is not None
        assert document_id is not None, "Element id is None on DELETE_OBJECT event"

        # Check there is a tab for the document
        assert (
            document_id in self.tabs
        ), f"Document tab not found for document {document_id} on DELETE_DOCUMENT event"

        # Delete tab from tabs widget
        document_tab: QWidget = self.tabs.get(document_id)
        self.removeTab(self.indexOf(document_tab))

        # Delete child components
        child_component: Union[DocumentTree, DocumentRender] = None
        for child_component in self.tab_children.get(document_id):
            child_component.delete_component()

        # Delete tab object
        document_tab.parent = None
        document_tab.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : update_on_modify_object
    # Description: Update the documents tab menu component when an object
    #              is modified.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_modify_object(self, *args, **kwargs) -> None:
        """
        Update the documents tab menu component when an object is modified.
        It changes the tab name with the new document name if the object
        modified is a document.
        """
        element_id: ProteusID = kwargs.get("element_id")

        # Check the element id is not None
        assert element_id is not None, "Element id is None on MODIFY_OBJECT event"

        # Check if exists a tab for the element
        if element_id in self.tabs:
            # Get document tab
            document_tab: QWidget = self.tabs.get(element_id)

            # Change tab name
            element: Object = Controller.get_element(element_id)
            document_name: str = element.get_property("name").value
            self.setTabText(self.indexOf(document_tab), document_name)

    # ======================================================================
    # Component slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : current_document_changed
    # Description: Slot triggered when the current document tab is changed.
    #              It updates the current document id in the controller.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def current_document_changed(self, index: int) -> None:
        """
        Slot triggered when the current document tab is changed. It updates
        the current document id in the state manager.
        """
        # Get document id
        document_id: ProteusID = None
        if index >= 0:
            document_tab: QWidget = self.widget(index)
            # Get the document id (key) from the tab (value)
            document_id: ProteusID = list(self.tabs.keys())[
                list(self.tabs.values()).index(document_tab)
            ]

        # Update current document in the state manager
        StateManager.set_current_document(document_id)