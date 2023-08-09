# ==========================================================================
# File: views_container.py
# Description: PyQT6 views container component for the PROTEUS application
# Date: 04/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt, QByteArray, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTabWidget,
    QStyle,
    QMessageBox,
    QTabBar,
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

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: ViewsContainer
# Description: PyQT6 views container class for the PROTEUS application
# Date: 04/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ViewsContainer(QTabWidget):
    """
    Views container component for the PROTEUS application. It contains
    a browser for each project view. Displays the current document
    representation for each view.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self, parent=None, controller: Controller = None, *args, **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.
        """
        super().__init__(parent, *args, **kwargs)
        # Controller instance
        assert isinstance(
            controller, Controller
        ), "Must provide a controller instance to the views container component"
        self._controller: Controller = controller

        # Translator instance
        self.translator = Translator()

        # Dict of stored browsers for each view. The way the dict is updated
        # the index of the browser is the same as the index of the tab.
        # NOTE: Dictionaries are ordered since Python 3.7. We can parse the
        #       dict to a list to get the browsers in the same order as the
        #       tabs.
        # NOTE: QWebEngineView is used instead QTextBrowser because it supports
        #       javascript, external resources and other features that are
        #       needed to render the document.
        # TODO: Find an alternative to avoid using multiple browsers. It
        #       has an impact on memory usage but is faster than setHtml.
        #       Multiple browsers are a solution to QTabWidget since a
        #       QWebEngineView cannot be added to multiple parents.
        self.browsers: Dict[str, QWebEngineView] = {}
        self.tabs: Dict[str, QWidget] = {}

        # Create the component
        self.create_component()

        # Connect tab close signal to the close_tab method
        self.tabCloseRequested.connect(self.close_tab)

        # Connect update methods to the events
        EventManager.attach(Event.MODIFY_OBJECT, self.update_component, self)
        EventManager.attach(Event.ADD_OBJECT, self.update_component, self)
        EventManager.attach(Event.DELETE_OBJECT, self.update_component, self)
        EventManager.attach(Event.CURRENT_DOCUMENT_CHANGED, self.update_component, self)
        EventManager.attach(Event.CURRENT_VIEW_CHANGED, self.update_component, self)
        EventManager.attach(Event.ADD_VIEW, self.update_on_add_view, self)
        EventManager.attach(Event.DELETE_VIEW, self.update_on_delete_view, self)
        EventManager.attach(Event.SELECT_OBJECT, self.update_on_select_object, self)

        # Call the current view changed method to update the document for the
        # first time if there are views
        if len(self.tabs) > 0:
            self.current_view_changed(index=0)

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the views container component.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the views container component.
        """
        # Allow to close tabs
        self.setTabsClosable(True)

        xsl_templates: list[str] = self._controller.get_project_templates()
        for xsl_template in xsl_templates:
            self.add_view(xsl_template)

        # Create a button to add new views
        add_view_button: QPushButton = QPushButton()
        add_view_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        )

        # Connect to new view dialog
        add_view_button.clicked.connect(
            lambda: NewViewDialog.create_dialog(self._controller)
        )
        self.setCornerWidget(add_view_button, Qt.Corner.TopRightCorner)

        # Hide the close button on the main view tab
        tabbutton: QWidget = (
            self.tabBar().tabButton(0, QTabBar.ButtonPosition.RightSide).hide()
        )

        # Connect singal to handle view tab change
        self.currentChanged.connect(self.current_view_changed)

        log.info("Views container component created")

    # ----------------------------------------------------------------------
    # Method     : add_view
    # Description: Add a new view to the views container component.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_view(self, xslt_name: str) -> None:
        """
        Add a new view to the views container component.
        """
        main_tab: QWidget = QWidget()
        layout = QVBoxLayout()

        # Create browser
        browser: QWebEngineView = QWebEngineView(self)
        browser.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        layout.addWidget(browser)

        # Create document page using subclass
        # NOTE: This subclass is needed for external links handling
        document_page: DocumentPage = DocumentPage(
            parent=browser, translator=self.translator
        )

        browser.setPage(document_page)

        # Build the tab code name
        # NOTE: The tab code name is used to access the tab name internationalization
        tab_code_name: str = f"document_render.view.{xslt_name}"

        # Set layout, add tab
        # NOTE: Tabs are added in the same order as the browsers are stored,
        #       always at the end.
        main_tab.setLayout(layout)
        self.addTab(main_tab, self.translator.text(tab_code_name))

        # Store the browser and the tab
        self.browsers[xslt_name] = browser
        self.tabs[xslt_name] = main_tab

    # ----------------------------------------------------------------------
    # Method     : delete_component
    # Description: Delete the component and its children components.
    # Date       : 09/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_component(self) -> None:
        """
        Delete the component and its children components.
        Handle the detachment from the event manager.
        """
        # Detach from the event manager
        EventManager.detach(self)

        # Delete the component
        self.setParent(None)
        self.deleteLater()

        log.info("Views container component deleted")

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_component
    # Description: Update the views container component.
    # Date       : 04/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self, *args, **kwargs) -> None:
        """
        Update the views container component. Update the current view browser
        with the content of the current document. If the current view is not
        in the browsers dict, ignore the update.

        Triggered by: Event.MODIFY_OBJECT, Event.ADD_OBJECT, Event.DELETE_OBJECT
        Event.CURRENT_DOCUMENT_CHANGED, Event.CURRENT_VIEW_CHANGED
        """

        current_document_id: ProteusID = StateManager.get_current_document()
        current_view: str = StateManager.get_current_view()

        # If the current view is not in the browsers dict, ignore the update
        if current_view not in self.browsers:
            log.warning(
                f"View {current_view} not found in the views container component"
            )
            return

        # If there is no current document, clear the browser
        if current_document_id is None:
            browser: QWebEngineView = self.browsers[current_view]
            browser.page().setContent(QByteArray(), "text/html")
            return

        # Update the current view browser with the content of the current document
        if current_view in self.browsers and current_document_id is not None:
            browser: QWebEngineView = self.browsers[current_view]

            # Get html from controller
            html_str: str = self._controller.get_document_view(
                document_id=current_document_id, xslt_name=current_view
            )

            # Convert html to QByteArray
            # NOTE: This is done to avoid 2mb limit on setHtml method
            # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwebenginewidgets/qwebengineview.html#setHtml
            html_array: QByteArray = QByteArray(html_str.encode(encoding="utf-8"))
            browser.page().setContent(html_array, "text/html")

            # Connect to load finished signal to update the object list
            # NOTE: This is necessary to run the script after the page is loaded
            # https://stackoverflow.com/questions/74257725/qwebengineview-page-runjavascript-does-not-run-a-javascript-code-correctly
            browser.page().loadFinished.connect(lambda: self.update_on_select_object())

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
        Update the views container component when an object is selected.
        Navigate to the object in the document given the object id.

        Triggered by: Event.SELECT_OBJECT
        """
        # Get the selected object id
        selected_object_id: ProteusID = StateManager.get_current_object()
        current_view: str = StateManager.get_current_view()

        # If there is no selected object or the document is not the current
        # document, do nothing
        if selected_object_id is None:
            return

        # Create the javascript code to navigate to the object
        # NOTE: Must use getElementById instead of querySelector because
        #       object id may start with a number.
        # https://stackoverflow.com/questions/37270787/uncaught-syntaxerror-failed-to-execute-queryselector-on-document
        script: str = (
            f"document.getElementById('{selected_object_id}').scrollIntoView();"
        )

        # Iterate over the browsers and navigate to the url
        browser: QWebEngineView = self.browsers[current_view]
        browser.page().runJavaScript(script)

    # ----------------------------------------------------------------------
    # Method     : update_on_delete_view
    # Description: Update the views container component when a view is
    #              deleted from the document.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_delete_view(self, *args, **kwargs) -> None:
        """
        Update the views container component when a view is deleted from
        the project documents. Delete the tab from each document.

        Triggered by: Event.DELETE_VIEW
        """
        xslt_name: str = kwargs["xslt_name"]

        # Get the index of the tab to delete
        tab: int = self.tabs[xslt_name]
        tab_index: int = self.indexOf(tab)

        # Delete the tab
        self.removeTab(tab_index)
        self.update()

        self.tabs.pop(xslt_name)

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
        self._controller.delete_project_template(xslt_name)

    # ----------------------------------------------------------------------
    # Method     : current_view_changed
    # Description: Slot triggered when the current view tab is changed.
    #              It updates the current view in the state manager.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def current_view_changed(self, index: int) -> None:
        """
        Slot triggered when the current document tab is changed. It updates
        the current view in the state manager.
        """
        # Get view name from the tab index
        view_name: str = None
        if index >= 0:
            view_tab: QWidget = self.widget(index)
            # Get the document id (key) from the tab (value)
            view_name = list(self.tabs.keys())[list(self.tabs.values()).index(view_tab)]

        # Update current document in the state manager
        StateManager.set_current_view(view_name)
    

# --------------------------------------------------------------------------
# Class: DocumentPage
# Description: Document Page class. Subclass of QWebEnginePage.
# Date: 30/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DocumentPage(QWebEnginePage):
    """
    Subclass of QWebEnginePage. Used to override the acceptNavigationRequest
    method to avoid opening external links in the browser.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Initialize the class.
    # Date       : 30/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent, translator: Translator, *args, **kargs) -> None:
        """
        Initialize the class.
        """
        super().__init__(parent, *args, **kargs)
        self.translator: Translator = translator

    # ----------------------------------------------------------------------
    # Method     : acceptNavigationRequest
    # Description: Override the acceptNavigationRequest method to avoid
    #              opening external links in the browser.
    # Date       : 30/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def acceptNavigationRequest(
        self, url: QUrl, _type: QWebEnginePage.NavigationType, isMainFrame: bool
    ) -> bool:
        """
        Override the acceptNavigationRequest method to avoid opening
        external links in the browser. If the link is a link to an
        external page, ask the user if he wants to open it in system
        default browser.
        """
        # If the link is a link to an external page, ask the user if he
        # wants to open it in system default browser.
        if (
            _type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked
            and not url.isLocalFile()
        ):
            # Ask the user if he wants to open the link in the system
            # default browser
            reply: QMessageBox.StandardButton = QMessageBox.question(
                None,
                self.translator.text("document_render.external_link"),
                self.translator.text(
                    "document_render.external_link.text", url.toString()
                ),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            # If the user wants to open the link in the system default
            # browser, open it
            if reply == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(url)
                return False
            else:
                return False

        return super().acceptNavigationRequest(url, _type, isMainFrame)
