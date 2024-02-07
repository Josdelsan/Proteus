# ==========================================================================
# File: new_document_dialog.py
# Description: PyQT6 new document component for the PROTEUS application
# Date: 28/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QFrame,
    QDialogButtonBox,
)


# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.object import Object
from proteus.controller.command_stack import Controller
from proteus.utils import ProteusIconType
from proteus.utils.translator import Translator
from proteus.views.components.abstract_component import ProteusComponent

# Module configuration
_ = Translator().text  # Translator


# --------------------------------------------------------------------------
# Class: Newdocument
# Description: PyQT6 new document component for the PROTEUS application
# Date: 28/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class NewDocumentDialog(QDialog, ProteusComponent):
    """
    New document component class for the PROTEUS application. It provides a
    dialog form to create new documents from document archetypes.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Create properties to store the new document data.
        """
        super(NewDocumentDialog, self).__init__(*args, **kwargs)

        # Properties for creating a new document
        self._archetype_id: ProteusID = None

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        # Set the window title
        self.setWindowTitle(_("new_document_dialog.title"))

        # Set window icon
        proteus_icon: Path = self._config.get_icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(QIcon(proteus_icon.as_posix()))

        # Create a separator widget
        separator: QFrame = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Get document archetypes
        document_archetypes: List[Object] = self._controller.get_document_archetypes()
        # Create a combo box with the document archetypes
        archetype_label: QLabel = QLabel(_("new_document_dialog.combobox.label"))
        archetype_combo: QComboBox = QComboBox()

        archetype: Object = None
        for archetype in document_archetypes:
            archetype_combo.addItem(archetype.get_property(PROTEUS_NAME).value)

        # Show the archetype description
        description_label: QLabel = QLabel(
            _("new_document_dialog.archetype.description")
        )
        description_output: QLabel = QLabel()
        description_output.setWordWrap(True)

        # Create Save and Cancel buttons
        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)

        # Error message label
        self.error_label: QLabel = QLabel()
        self.error_label.setObjectName("error_label")
        self.error_label.setWordWrap(True)

        # Add the widgets to the layout
        layout.addWidget(archetype_label)
        layout.addWidget(archetype_combo)
        layout.addWidget(separator)
        layout.addWidget(description_label)
        layout.addWidget(description_output)
        layout.addWidget(self.error_label)

        layout.addWidget(self.button_box)

        # ---------------------------------------------
        # Actions
        # ---------------------------------------------

        # Update the description when the user selects an archetype
        def update_description():
            index = archetype_combo.currentIndex()
            if index >= 0:
                archetype: Object = document_archetypes[index]
                self._archetype_id = archetype.id
                description_output.setText(archetype.properties["description"].value)

        # Update the description when the user selects an archetype
        archetype_combo.currentIndexChanged.connect(update_description)
        # Update the description for the first archetype
        update_description()

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Save button clicked event handler
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_button_clicked(self):
        """
        Manage the save button clicked event. It creates a new document from
        the selected archetype.
        """
        if self._archetype_id is None:
            self.error_label.setText(
                _("new_document_dialog.error.no_archetype_selected")
            )
            return

        # Create the document
        self._controller.create_document(self._archetype_id)

        # Close the form window
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Cancel button clicked event handler
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def cancel_button_clicked(self):
        """
        Manage the cancel button clicked event. It closes the form window
        without creating any document.
        """
        # Close the form window without saving any changes
        self.close()
        self.deleteLater()

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog
    # Description: Create a new document dialog and show it
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(controller: Controller) -> "NewDocumentDialog":
        """
        Create a new document dialog and show it
        """
        dialog = NewDocumentDialog(controller=controller)
        dialog.exec()
        return dialog
