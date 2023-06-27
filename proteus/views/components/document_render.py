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

from typing import Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTabWidget,
    QStyle,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.views.utils.event_manager import Event, EventManager
from proteus.views.utils.state_manager import StateManager
from proteus.views.utils.translator import Translator
from proteus.views.components.dialogs.new_view_dialog import NewViewDialog
from proteus.controller.command_stack import Controller


# --------------------------------------------------------------------------
# Class: DocumentRender
# Description: PyQT6 document render for the PROTEUS application
# Date: 04/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DocumentRender(QTabWidget):
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

        self.translator = Translator()

        # Store the document id reference
        self.element_id: ProteusID = element_id

        # Dict of stored browsers for each view. The way the dict is updated
        # the index of the browser is the same as the index of the tab.
        # NOTE: Dictionaries are ordered since Python 3.7. We can parse the
        #       dict to a list to get the browsers in the same order as the
        #       tabs.
        # TODO: Find an alternative to avoid using multiple browsers. It
        #       has an impact on memory usage but is faster than setHtml.
        #       Multiple browsers are a solution to QTabWidget since a
        #       QWebEngineView cannot be added to multiple parents.
        self.browsers: Dict[str, QWebEngineView] = {}

        # Create the component
        self.create_component()

        # Connect tab close signal to the close_tab method
        self.tabCloseRequested.connect(self.close_tab)

        # Connect update methods to the events
        EventManager.attach(Event.MODIFY_OBJECT, self.update_component, self)
        EventManager.attach(Event.ADD_OBJECT, self.update_component, self)
        EventManager.attach(Event.DELETE_OBJECT, self.update_component, self)
        EventManager.attach(Event.CURRENT_DOCUMENT_CHANGED, self.update_component, self)
        EventManager.attach(Event.ADD_VIEW, self.update_on_add_view, self)
        EventManager.attach(Event.DELETE_VIEW, self.update_on_delete_view, self)
        EventManager.attach(Event.SELECT_OBJECT, self.update_on_select_object, self)

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
        # Allow to close tabs
        self.setTabsClosable(True)

        xsl_templates: list[str] = Controller().get_project_templates()
        for xsl_template in xsl_templates:
            self.add_view(xsl_template)

        # Create a button to add new views
        add_view_button: QPushButton = QPushButton()

        # Set the button icon
        add_view_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        )

        # Connect to new view dialog
        add_view_button.clicked.connect(NewViewDialog.create_dialog)

        self.setCornerWidget(add_view_button, Qt.Corner.TopRightCorner)

    # ----------------------------------------------------------------------
    # Method     : add_view
    # Description: Add a new view to the document render component.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_view(self, xslt_name: str) -> None:
        """
        Add a new view to the document render component.
        """
        main_tab: QWidget = QWidget()
        layout = QVBoxLayout()

        # Create browser
        browser: QWebEngineView = QWebEngineView(self)
        layout.addWidget(browser)

        # Get html from controller
        html_str: str = Controller().get_document_view(self.element_id, xslt_name)

        # Convert html to QByteArray
        # NOTE: This is done to avoid 2mb limit on setHtml method
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwebenginewidgets/qwebengineview.html#setHtml
        html_array: QByteArray = QByteArray(html_str.encode(encoding="utf-8"))
        browser.setContent(html_array, "text/html")

        # Build the tab code name
        # NOTE: The tab code name is used to access the tab name internationalized
        tab_code_name: str = f"document_render.view.{xslt_name}"

        # Set layout, add tab and store browser
        # NOTE: Tabs are added in the same order as the browsers are stored,
        #       always at the end.
        main_tab.setLayout(layout)
        self.addTab(main_tab, self.translator.text(tab_code_name))
        self.browsers[xslt_name] = browser

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

        current_document_id: ProteusID = StateManager.get_current_document()

        # If the current document is the same as the document render
        # element id, do not update the component
        if current_document_id == self.element_id:
            # Iterate over the browsers and update them with the corresponding
            # html
            for xslt_name, browser in self.browsers.items():
                # Get html from controller
                html_str: str = Controller().get_document_view(
                    self.element_id, xslt_name
                )

                # Convert html to QByteArray
                # NOTE: This is done to avoid 2mb limit on setHtml method
                # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwebenginewidgets/qwebengineview.html#setHtml
                html_array: QByteArray = QByteArray(html_str.encode(encoding="utf-8"))
                browser.setContent(html_array, "text/html")

    # ----------------------------------------------------------------------
    # Method     : update_on_add_view
    # Description: Update the document render component when a new view is
    #              added to the project.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_add_view(self, *args, **kwargs) -> None:
        """
        Update the document render component when a new view is added to
        the project documents. Add a new tab to each document. If the
        view already exists, do nothing.

        Triggered by: Event.ADD_VIEW
        """
        xslt_name: str = kwargs["xslt_name"]

        # If the view already exists, do nothing
        if xslt_name in self.browsers.keys():
            return

        self.add_view(xslt_name)

    # ----------------------------------------------------------------------
    # Method     : update_on_select_object
    # Description: Update the document render component when an object is
    #              selected.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_select_object(self, *args, **kwargs) -> None:
        """
        Update the document render component when an object is selected.
        Navigate to the object in the document given the object id.

        Triggered by: Event.SELECT_OBJECT
        """
        # Get the selected object id
        selected_object_id: ProteusID = StateManager.get_current_object()

        # Get document id
        document_id: ProteusID = StateManager.get_current_document()

        # If there is no selected object or the document is not the current
        # document, do nothing
        if selected_object_id is None or document_id != self.element_id:
            return

        # Create the javascript code to navigate to the object
        # NOTE: Must use getElementById instead of querySelector because
        #       object id may start with a number.
        # https://stackoverflow.com/questions/37270787/uncaught-syntaxerror-failed-to-execute-queryselector-on-document
        script: str = (
            f"document.getElementById('{selected_object_id}').scrollIntoView();"
        )

        # Iterate over the browsers and navigate to the url
        for browser in self.browsers.values():
            browser.page().runJavaScript(script)

    # ----------------------------------------------------------------------
    # Method     : update_on_delete_view
    # Description: Update the document render component when a view is
    #              deleted from the document.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_delete_view(self, *args, **kwargs) -> None:
        """
        Update the document render component when a view is deleted from
        the project documents. Delete the tab from each document.

        Triggered by: Event.DELETE_VIEW
        """
        xslt_name: str = kwargs["xslt_name"]

        # Get the index of the tab to delete
        tab_index: int = self.indexOf(self.browsers[xslt_name].parentWidget())

        # Delete the tab
        self.removeTab(tab_index)
        self.update()

        # Delete the browser
        browser: QWebEngineView = self.browsers.pop(xslt_name)
        browser.parent = None
        browser.deleteLater()

    # ======================================================================
    # Component methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : close_tab
    # Description: Close the tab with the given index.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def close_tab(self, index) -> None:
        """
        Triggered when the user closes a tab. Get the xslt name and call
        the controller to delete the view and delete template from project
        file.
        """
        # Get the key corresponding to the tab index
        xslt_name: str = list(self.browsers.keys())[index]

        # Delete the view
        Controller().delete_project_template(xslt_name)
