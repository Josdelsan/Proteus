# ==========================================================================
# File: document_interactions.py
# Description: PyQT6 document interactions class for the REMUS plugin
# Date: 03/01/2024
# Version: 0.2
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils import ProteusIconType
from proteus.utils.translator import Translator
from proteus.model import ProteusID, PROTEUS_DOCUMENT, PROTEUS_NAME
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.views.components.abstract_component import ProteusComponent
from proteus.views.components.dialogs.property_dialog import PropertyDialog

# Module configuration
log = logging.getLogger(__name__)  # Logger
_ = Translator().text  # Translator


# --------------------------------------------------------------------------
# Class: DocumentInteractions
# Description: Document interactions class for the REMUS plugin
# Date: 11/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DocumentInteractions(ProteusComponent):
    """
    Document interactions class for the REMUS plugin. Implements slots that
    are used by the document html view to handle user interactions.
    """

    @pyqtSlot(str)
    def open_properties_dialog(self, id: str) -> None:
        """
        Open the edit properties dialog for the given object id
        :param id: object id
        """
        if not id:
            log.error(
                f"Method 'open_edit_properties_dialog' called with empty id '{id}'"
            )
            return

        # Check if the id exists in the project
        proteus_id = ProteusID(id)

        # Raise an error if the id does not exist
        self._controller.get_element(proteus_id)

        log.debug(
            f"Object '{proteus_id}' was double clicked in the document html view, opening edit properties dialog"
        )

        # Create the dialog
        PropertyDialog.create_dialog(self._controller, proteus_id)

    @pyqtSlot(str)
    def select_and_navigate_to_object(self, id: str) -> None:
        """
        Select the object in the document tree and navigate to the document
        where the object is located if necessary.

        :param id: object id
        """
        if not id:
            log.error(f"Method 'navigate_to_object' called with empty id '{id}'")
            return

        # Check if the id exists in the project
        object_id = ProteusID(id)

        # Raise an error if the id does not exist
        object: Object = self._controller.get_element(object_id)

        log.debug(
            f"A reference to object '{object_id}' was clicked in the document html view, selecting object in document tree and navigating to document if necessary"
        )

        # Make sure the object is not a project
        if isinstance(object, Project):
            log.error(
                f"Method 'open_edit_properties_dialog' called with project id '{id}'"
            )
            return

        # Check if the object is in the current document ----------------------
        def find_object_document(object: Object) -> ProteusID:
            """Helper function to find the document of an object"""
            if PROTEUS_DOCUMENT in object.classes:
                return object.id
            else:
                return find_object_document(object.parent)

        current_document = self._state_manager.get_current_document()
        object_document = find_object_document(object)

        # If the object is in the current document, select object in state manager
        if current_document == object_document:
            # This triggers the SELECT_OBJECT event that will select the object
            # in the document tree and also call the scroll javascript function
            self._state_manager.set_current_object(object_id, object_document)
            return

        # If the object is not in the current document, show the user a message box
        # asking if he wants to navigate to the document where the object is
        else:
            object_name = object.get_property(PROTEUS_NAME).value
            document_name = (
                self._controller.get_element(object_document)
                .get_property(PROTEUS_NAME)
                .value
            )

            message_box = QMessageBox()

            # Set icon
            proteus_icon: Path = self._config.get_icon(
                ProteusIconType.App, "proteus_icon"
            )
            message_box.setWindowIcon(QIcon(proteus_icon.as_posix()))

            # Set title and text
            message_box.setWindowTitle(self.__("document.navigation.request.title"))
            message_box.setText(
                self.__("document.navigation.request.text", object_name, document_name)
            )

            # Set buttons
            message_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            message_box.setDefaultButton(QMessageBox.StandardButton.Yes)

            # If the user clicks yes, navigate to the document
            if message_box.exec() == QMessageBox.StandardButton.Yes:
                # Set the current object in the other document and do not navigate (will not
                # navigate because the document is not the current document)
                # Then set the current document, this will avoid update_on_select_object to
                # be called twice, also avoid update_on_select_object triggering before
                # new document is completely loaded
                self._state_manager.set_current_object(
                    object_id, object_document, False
                )
                self._state_manager.set_current_document(object_document)
            # If the user clicks no, do nothing
            else:
                return
