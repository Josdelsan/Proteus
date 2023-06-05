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

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QLabel, \
                            QComboBox, QLineEdit, QPushButton, QFrame, \
                            QSizePolicy, QDialogButtonBox


# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.model.object import Object
from proteus.controller.command_stack import Controller

# --------------------------------------------------------------------------
# Class: Newdocument
# Description: PyQT6 new document component for the PROTEUS application
# Date: 28/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class NewDocumentDialog(QDialog):
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
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Properties for creating a new document
        self._archetype_id = None

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
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a separator widget
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Get document archetypes
        document_archetypes : List[Object] = Controller.get_document_archetypes()
        # Create a combo box with the document archetypes
        archetype_label = QLabel("Select document Archetype:")
        archetype_combo = QComboBox()
        for archetype in document_archetypes:
            archetype_combo.addItem(archetype.properties["name"].value)
        

        # Show the archetype description
        description_label = QLabel("Document Description:")
        description_output = QLabel()


        # Create Save and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.save_button_clicked)
        button_box.rejected.connect(self.cancel_button_clicked)

        # Error message label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        # Add the widgets to the layout
        layout.addWidget(archetype_label)
        layout.addWidget(archetype_combo)
        layout.addWidget(separator)
        layout.addWidget(description_label)
        layout.addWidget(description_output)
        
        layout.addWidget(button_box)

        # Set fixed width for the window
        self.setFixedWidth(400)
        # Allow vertical expansion for the description
        description_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # ---------------------------------------------
        # Actions
        # ---------------------------------------------

        # Update the description when the user selects an archetype
        def update_description():
            index = archetype_combo.currentIndex()
            if index >= 0:
                archetype = document_archetypes[index]
                self._archetype_id = archetype.id
                description_output.setText(archetype.properties["description"].value)

        # Update the description when the user selects an archetype
        archetype_combo.currentIndexChanged.connect(update_description)
        # Update the description for the first archetype
        update_description()
        

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Save button clicked event handler
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_button_clicked(self):
        
        if self._archetype_id is None:
            self.error_label.setText("Please select a valid document archetype")
            return
        
        # Create the document
        Controller.create_document(self._archetype_id)

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


    # ----------------------------------------------------------------------
    # Method     : create_dialog
    # Description: Create a new document dialog and show it
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog() -> None:
        """
        Create a new document dialog and show it
        """
        dialog = NewDocumentDialog()
        dialog.exec()
