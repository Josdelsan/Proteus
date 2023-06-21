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
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
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
        EventManager.attach(Event.CURRENT_DOCUMENT_CHANGED, self.update_component, self)

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

        self.html_textedit = QTextEdit(self)
        self.html_textedit.setReadOnly(True)
        self.html_textedit.setVisible(False)
        layout.addWidget(self.html_textedit)

        html: str = Controller().get_document_html(self.element_id)
        self.browser.setHtml(html)
        self.html_textedit.setPlainText(html)

        # Add the button to switch between HTML and browser view
        self.switch_button = QPushButton("Switch View", self)
        self.switch_button.clicked.connect(self.switch_view)
        layout.addWidget(self.switch_button)

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
        Update the document render component when there is by an event. Just
        update the component if it is the current document displayed.

        Triggered by: Event.MODIFY_OBJECT, Event.ADD_OBJECT, Event.DELETE_OBJECT
        Event.CURRENT_DOCUMENT_CHANGED
        """

        current_document_id: ProteusID = Controller.get_current_document_id()   

        # If the current document is the same as the document render
        # element id, do not update the component
        if current_document_id == self.element_id:
            html: str = Controller().get_document_html(self.element_id)
            self.browser.setHtml(html)
            self.html_textedit.setPlainText(html)

    # ======================================================================
    # Component methods
    # ======================================================================

    def switch_view(self) -> None:
        """
        Switch between HTML and browser view.
        """
        is_browser_visible = self.browser.isVisible()
        if is_browser_visible:
            self.browser.setVisible(False)
            self.html_textedit.setVisible(True)
            self.switch_button.setText("Switch View: HTML")
        else:
            self.browser.setVisible(True)
            self.html_textedit.setVisible(False)
            self.switch_button.setText("Switch View: Browser")
