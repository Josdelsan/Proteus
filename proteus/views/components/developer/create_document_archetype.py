# ==========================================================================
# File: create_document_archetype.py
# Description: module for the PROTEUS create document archetype dialog
# Date: 29/10/2024
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
    QLabel,
    QFormLayout,
    QLineEdit,
)

# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.views.components.developer import XML_PROBLEMATIC_CHARS, create_error_label
from proteus.application.resources.translator import translate as _
from proteus.views.components.dialogs.base_dialogs import ProteusDialog
from proteus.controller.command_stack import Controller
from proteus.application.configuration.config import Config
from proteus.model.archetype_repository import ArchetypesType


# --------------------------------------------------------------------------
# Class: CreateDocumentArchetypeDialog
# Description: PyQT6 dialog component for the PROTEUS edit property dialog
# Date: 29/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class CreateDocumentArchetypeDialog(ProteusDialog):
    """
    CreateDocumentArchetypeDialog provides a dialog for creating a new object
    archetype from the selected object. It allows the user to set the ProteusID
    and the group/category where the new archetype will be stored. It also

    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 29/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component.
        """
        super(CreateDocumentArchetypeDialog, self).__init__(*args, **kwargs)

        self.object = self._controller.get_element(
            self._state_manager.get_current_document()
        )

        # Inputs
        self.input_id: QLineEdit
        self.directory_name: QLineEdit

        # Error labels
        self.error_label: QLabel = create_error_label()

        # Create the dialog
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component
    # Date       : 17/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the component
        """
        # Set the dialog title
        self.setWindowTitle(_("create_document_archetype_dialog.title"))

        # Create the main layout
        form_layout: QFormLayout = QFormLayout()

        # ProteusID input
        self.input_id = QLineEdit()

        # Directory name input
        self.directory_name = QLineEdit()


        # Add the inputs to the form layout
        form_layout.addRow(
            _("create_document_archetype_dialog.proteus_id"), self.input_id
        )
        form_layout.addRow(_("create_document_archetype_dialog.directory_name"), self.directory_name)

        # Add the error label
        form_layout.addRow(self.error_label)

        # Set the main layout
        self.set_content_layout(form_layout)

        # Connect the buttons to the slots
        self.accept_button.setText(_("dialog.create_button"))
        self.accept_button.clicked.connect(self.accept_button_clicked)

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : accept_button_clicked
    # Description: Slot method to accept the dialog
    # Date       : 29/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def accept_button_clicked(self) -> None:
        """
        Slot method to accept the dialog
        """
        # Inputs
        proteus_id = self.input_id.text().strip()
        directory_name = self.directory_name.text().strip()

        # Validate the ProteusID
        if not proteus_id or proteus_id == "":
            self.error_label.setText(
                _("create_document_archetype_dialog.proteus_id_missing")
            )
            self.error_label.show()
            return

        # Check if the ProteusID contains problematic characters
        if (
            any(char in proteus_id for char in XML_PROBLEMATIC_CHARS)
            or " " in proteus_id
        ):
            self.error_label.setText(
                _("create_document_archetype_dialog.proteus_id_invalid")
            )
            self.error_label.show()
            return
        
        # Force archetypes loading so lazy loading does not interfere with the check
        self._controller._archetype_service.get_project_archetypes()
        self._controller._archetype_service.get_document_archetypes()
        self._controller._archetype_service.get_object_archetypes()

        # Check if the ProteusID is already in use
        try:
            self._controller.get_archetype_by_id(proteus_id)
            self.error_label.setText(
                _("create_document_archetype_dialog.proteus_id_in_use")
            )
            self.error_label.show()
            return
        except AssertionError:
            self.error_label.hide()

        # Check if the directory name is empty
        if not directory_name or directory_name == "":
            self.error_label.setText(
                _("create_document_archetype_dialog.directory_name_missing")
            )
            self.error_label.show()
            return
        else:
            self.error_label.hide()

        # Check directory does not exist
        document_archetypes_dir = Config().profile_settings.archetypes_directory / ArchetypesType.DOCUMENTS
        if (document_archetypes_dir / directory_name).exists():
            self.error_label.setText(
                _("create_document_archetype_dialog.directory_name_in_use")
            )
            self.error_label.show()
            return
        else:
            self.error_label.hide()

        # Create the new archetype
        self._controller._archetype_service.store_document_as_archetype(
            self.object, proteus_id, directory_name
        )

        # Close the form window
        self.close()
        self.deleteLater()

    # ======================================================================
    # Dialog static methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog
    # Description: Create the dialog
    # Date       : 29/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(
        controller: Controller,
    ) -> "CreateDocumentArchetypeDialog":

        dialog: CreateDocumentArchetypeDialog = CreateDocumentArchetypeDialog(
            controller=controller
        )
        dialog.exec()
        return dialog
