# ==========================================================================
# File: project_container.py
# Description: PyQT6 project container component for the PROTEUS application
# Date: 03/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QSplitter

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.controller.command_stack import Controller
from proteus.views.utils.event_manager import EventManager
from proteus.views.components.documents_container import DocumentsContainer
from proteus.views.components.views_container import ViewsContainer

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: ProjectContainer
# Description: PyQT6 project container class for the PROTEUS application
# Date: 03/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ProjectContainer(QWidget):
    """
    Container for the project information. It contains a tab widget with the
    documents of the project and a tab widget with the project views.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 03/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self, parent=None, controller: Controller = None, *args, **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.

        Store the tabs for each document in a dictionary to access them
        later. Also store the children components of each tab in a
        dictionary to delete when the tab is closed.
        """
        super().__init__(parent, *args, **kwargs)
        # Controller instance
        assert isinstance(
            controller, Controller
        ), "Must provide a controller instance to the project container component"
        self._controller: Controller = controller

        # Children components
        self.documents_container: DocumentsContainer = None
        self.views_container: ViewsContainer = None

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the documents tab menu component
    # Date       : 03/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the project container component. Initialize its children
        (DocumentsContainer and ViewsContainer) and add them to an splitter
        widget.
        """
        # Create project container layout
        tab_layout: QHBoxLayout = QHBoxLayout(self)

        # Splitter
        splitter: QSplitter = QSplitter()

        # DocumentsContainer -------------------------------------------------
        self.documents_container: DocumentsContainer = DocumentsContainer(self, self._controller)
        self.documents_container.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred
        )
        self.documents_container.setMinimumWidth(200)

        # ViewsContainer -----------------------------------------------------
        self.views_container: ViewsContainer = ViewsContainer(self, self._controller)
        self.views_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.views_container.setMinimumWidth(400)

        # Add tree and render to splitter
        splitter.addWidget(self.documents_container)
        splitter.addWidget(self.views_container)
        # NOTE: By default the splitter is 1200px wide when the application
        #       is launched. We set the initial sizes proportionally to the
        #       splitter size to avoid the render component to be too small
        splitter.setSizes([300, 900])

        # Add splitter with tree and render to tab layout
        tab_layout.addWidget(splitter)
        self.setLayout(tab_layout)

        log.info("Project container component created")

    # ----------------------------------------------------------------------
    # Method     : delete_component
    # Description: Delete the project container component and its children
    #              components.
    # Date       : 09/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_component(self) -> None:
        """
        Delete the project container component and its children components.
        Handle the detachment from the event manager.
        """
        # Detach from the event manager
        EventManager.detach(self)

        # Delete children components
        self.documents_container.delete_component()
        self.views_container.delete_component()

        # Delete component
        self.setParent(None)
        self.deleteLater()

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ======================================================================
    # Component slots methods (connected to the component signals)
    # ======================================================================
