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

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QSizePolicy,
    QSplitter,
    QLabel,
    QScrollArea,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.controller.command_stack import Controller
from proteus.views.utils.decorators import subscribe_to
from proteus.views.utils.event_manager import Event, EventManager

# --------------------------------------------------------------------------
# Class: DocumentRender
# Description: PyQT6 document render for the PROTEUS application
# Date: 04/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@subscribe_to([Event.ADD_OBJECT, Event.MODIFY_OBJECT])
class DocumentRender(QScrollArea):
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
    def __init__(self, parent=None, document_id=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.document_id = document_id
        self.label = QLabel("")

        self.create_component()

    
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
        self.setWidgetResizable(True)

        widget = QWidget()
        self.setWidget(widget)
        layout = QVBoxLayout()

        xml = Controller().get_document_xml(self.document_id)
        self.label = QLabel(f"{xml}")

        layout.addWidget(self.label)
        widget.setLayout(layout)

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
        """
        xml = Controller().get_document_xml(self.document_id)
        self.label.setText(f"{xml}")

    # ----------------------------------------------------------------------
    # Method     : delete_component
    # Description: Delete the document render component.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_component(self, *args, **kwargs) -> None:
        """
        Delete the document render component.
        """
        EventManager.detach(Event.MODIFY_OBJECT, self)
        EventManager.detach(Event.ADD_OBJECT, self)
        self.parent = None
        self.deleteLater()