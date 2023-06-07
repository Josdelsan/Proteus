# ==========================================================================
# File: document_render.py
# Description: PyQT6 document render for the PROTEUS application
# Date: 04/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.views.utils.event_manager import Event, EventManager
from proteus.controller.command_stack import Controller


# --------------------------------------------------------------------------
# Class: DocumentRender
# Description: PyQT6 document render for the PROTEUS application
# Date: 04/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DocumentRender(QWidget):
    """
    Document render component for the PROTEUS application. It is used to
    display the document render.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent=None, element_id=None, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.

        Store the document id reference.
        """
        super().__init__(parent, *args, **kwargs)
        self.element_id: ProteusID = element_id
        self.browser: QWebEngineView = None

        self.create_component()

        EventManager.attach(Event.MODIFY_OBJECT, self.update_component, self)
        EventManager.attach(Event.ADD_OBJECT, self.update_component, self)
        EventManager.attach(Event.DELETE_OBJECT, self.update_component, self)

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the document render component.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the document render component.
        """
        layout = QVBoxLayout()

        # Create the web view using the web engine profile
        self.browser = QWebEngineView(self)
        layout.addWidget(self.browser)

        html: str = Controller().get_document_html(self.element_id)
        self.browser.setHtml(html)

        self.setLayout(layout)

    # ----------------------------------------------------------------------
    # Method     : delete_component
    # Description: Delete the document render component.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_component(self, *args, **kwargs) -> None:
        """
        Manage the deletion of the document render component. Detach from
        events and delete the component.

        This method must be called by the parent component in order to
        delete the document render before deleting the parent (document tab)
        """
        # Detach the component from the event manager
        EventManager.detach(self)

        # Delete the component
        self.parent = None
        self.deleteLater()

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_component
    # Description: Update the document render component.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self, *args, **kwargs) -> None:
        """
        Update the document render component.

        Triggered by: Event.MODIFY_OBJECT, Event.ADD_OBJECT, Event.DELETE_OBJECT
        """
        html: str = Controller().get_document_html(self.element_id)
        self.browser.setHtml(html)
