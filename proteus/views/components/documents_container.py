# ==========================================================================
# File: project_container.py
# Description: PyQT6 documents container component for the PROTEUS application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict, List
import logging
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QTabWidget, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.controller.command_stack import Controller
from proteus.views import ACRONYM_ICON_TYPE
from proteus.utils.event_manager import Event
from proteus.views.components.abstract_component import ProteusComponent
from proteus.views.components.document_tree import DocumentTree

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: DocumentsContainer
# Description: PyQT6 documents container class for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DocumentsContainer(QTabWidget, ProteusComponent):
    """
    Documents tab menu component for the PROTEUS application. It is used to
    display the documents of the project in a tab menu. It manages the
    creation of the document tree component for each document.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self, parent: QWidget, *args, **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.

        Store the tabs for each document in a dictionary to access them
        later. Also store the children components of each tab in a
        dictionary to delete when the tab is closed.

        :param parent: Parent widget.
        """
        super(DocumentsContainer, self).__init__(parent, *args, **kwargs)

        # Tabs dictionary
        self.tabs: Dict[ProteusID, DocumentTree] = {}

        # Create the component
        self.create_component()

        # Subscribe to events
        self.subscribe()

        # Call the current document changed method to update the document for the
        # first time
        if len(self.tabs) > 0:
            self.current_document_changed(index=0)

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
        self.setObjectName("documents_container")
        self.setIconSize(QSize(28, 28))
        self.tabBar().setExpanding(True)

        # Handle tab reordering
        self.setMovable(True)
        self.tabBar().tabMoved.connect(self.tab_moved)

        # Get project structure from project service
        project_structure: List[Object] = self._controller.get_project_structure()

        # Add a document tab for each document in the project
        for document in project_structure:
            self.add_document(document)

        # Connect singal to handle document tab change
        self.currentChanged.connect(self.current_document_changed)

        log.info("Documents container tab component created")

    # ----------------------------------------------------------------------
    # Method     : add_document
    # Description: Add a document to the tab menu creating its child
    #              components (tree and render).
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_document(self, document: Object, position: int = None) -> None:
        """
        Add a document to the tab menu creating its child component (document
        tree).
        """
        # Tree widget --------------------------------------------------------
        tab: DocumentTree = DocumentTree(
            element_id=document.id, parent=self
        )

        # Add tab to the dictionary with the document id as key
        self.tabs[document.id] = tab

        # Get acronym, add the tab and store the index given by the addTab method
        document_acronym: str = document.get_property("acronym").value
        if position is not None:
            tab_index = self.insertTab(position, tab, document_acronym)
        else:
            tab_index = self.addTab(tab, document_acronym)

        # Set the tab icon
        icon_path: Path = self._config.get_icon(ACRONYM_ICON_TYPE, document_acronym)
        self.setTabIcon(tab_index, QIcon(icon_path.as_posix()))

        # Drop configuration to allow objects moves between tabs
        tabbar = self.tabBar()
        tabbar.setChangeCurrentOnDrag(True)
        tabbar.setAcceptDrops(True)

    # ----------------------------------------------------------------------
    # Method     : subscribe
    # Description: Subscribe the component to the events.
    # Date       : 15/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def subscribe(self) -> None:
        """
        Subscribe the component to the events.

        DocumentsContainer component subscribes to the following events:
            - Event.ADD_DOCUMENT    | update_on_add_document
            - Event.DELETE_DOCUMENT | update_on_delete_document
            - Event.MODIFY_OBJECT   | update_on_modify_object
            - Event.CURRENT_DOCUMENT_CHANGED | update_on_current_document_changed
        """
        self._event_manager.attach(
            Event.ADD_DOCUMENT, self.update_on_add_document, self
        )
        self._event_manager.attach(
            Event.DELETE_DOCUMENT, self.update_on_delete_document, self
        )
        self._event_manager.attach(
            Event.MODIFY_OBJECT, self.update_on_modify_object, self
        )
        self._event_manager.attach(
            Event.CURRENT_DOCUMENT_CHANGED,
            self.update_on_current_document_changed,
            self,
        )

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

        position: int = kwargs.get("position", None)

        # Check the document is instance of Object
        # Check the object is instance of Object
        assert isinstance(
            new_document, Object
        ), "Object is not instance of Object on ADD_DOCUMENT event"

        self.add_document(new_document, position=position)

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

        # Delete tab from tabs widget and delete it
        document_tab: DocumentTree = self.tabs.pop(document_id)
        self.removeTab(self.indexOf(document_tab))
        document_tab.delete_component()

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

        Triggered by: Event.MODIFY_OBJECT
        """
        element_id: ProteusID = kwargs.get("element_id")

        # Check the element id is not None
        assert element_id is not None, "Element id is None on MODIFY_OBJECT event"

        # Check if exists a tab for the element
        if element_id in self.tabs:
            # Get document tab
            document_tab: DocumentTree = self.tabs.get(element_id)
            tab_index: int = self.indexOf(document_tab)

            # Get new acronym
            element: Object = self._controller.get_element(element_id)
            document_acronym: str = element.get_property("acronym").value
            self.setTabText(tab_index, document_acronym)

            # Get new icon
            icon_path: Path = self._config.get_icon(ACRONYM_ICON_TYPE, document_acronym)
            self.setTabIcon(tab_index, QIcon(icon_path.as_posix()))

    # ----------------------------------------------------------------------
    # Method     : update_on_current_document_changed
    # Description: Update the documents tab menu component when the current
    #              document is changed.
    # Date       : 20/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_current_document_changed(self, *args, **kwargs) -> None:
        """
        Update the documents tab menu component when the current document
        is changed. It changes the current tab to the document tab with
        the current document id if the new current document is different
        from old current document.

        Triggered by: Event.CURRENT_DOCUMENT_CHANGED
        """
        new_document_id: ProteusID = self._state_manager.get_current_document()

        # Check if exists a tab for the element
        if new_document_id in self.tabs:
            # Get document tab
            document_tab: DocumentTree = self.tabs.get(new_document_id)
            tab_index: int = self.indexOf(document_tab)

            if tab_index != self.currentIndex():
                # Set current tab
                self.setCurrentIndex(tab_index)

    # ======================================================================
    # Component slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : current_document_changed
    # Description: Slot triggered when the current document tab is changed.
    #              It updates the current document id in the state manager.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def current_document_changed(self, index: int) -> None:
        """
        Slot triggered when the current document tab is changed. It updates
        the current document id in the state manager if the index is different
        from the current index.
        """
        # Get document id
        document_id: ProteusID = None
        if index >= 0:
            # Access tab from the index
            document_tab: DocumentTree = self.widget(index)

            # Access document id (key) from the tab (value)
            document_id = list(self.tabs.keys())[
                list(self.tabs.values()).index(document_tab)
            ]

        # Avoid updating the state manager if the document is the same
        # This can happen when the tab is selected by current_document_changed
        # event
        if document_id == self._state_manager.get_current_document():
            return

        # Update current document in the state manager
        self._state_manager.set_current_document(document_id)

    def tab_moved(self, new_index: int, old_index: int) -> None:
        # Get the current document id
        document_id: ProteusID = self._state_manager.get_current_document()

        # Get the project
        project = self._controller.get_current_project()

        log.debug(f"Moving document {document_id} from {old_index} to {new_index}")

        # Index adjusting to allow pop and insert without problems
        if new_index > old_index:
            new_index += 1

        self._controller.change_document_position(document_id, new_index)
