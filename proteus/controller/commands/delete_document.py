# ==========================================================================
# File: delete_document.py
# Description: Controller to delete an document.
# Date: 03/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoCommand

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.views.utils.event_manager import EventManager, Event


# --------------------------------------------------------------------------
# Class: DeletedocumentCommand
# Description: Controller class delete an document.
# Date: 03/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DeleteDocumentCommand(QUndoCommand):
    """
    Controller class to delete an document.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, document_id: ProteusID):
        super(DeleteDocumentCommand, self).__init__()

        self.before_clone_parent_state: ProteusState = None
        self.document: Object = ProjectService._get_element_by_id(document_id)
        self.old_document_state: ProteusState = self.document.state

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the command, deleting the document.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo the command, deleting the document.
        """
        # Set redo text
        self.setText(f"Mark as DEAD document {self.document.id}")

        # Change the state of the cloned document and his children to FRESH
        ProjectService.change_state(self.document.id, ProteusState.DEAD)

        # Modify the parent state depending on its current state
        self.before_clone_parent_state: ProteusState = self.document.parent.state

        if self.before_clone_parent_state is ProteusState.CLEAN:
            after_clone_parent_state: ProteusState = ProteusState.DIRTY
        else:
            after_clone_parent_state: ProteusState = self.before_clone_parent_state

        self.document.parent.state: ProteusState = after_clone_parent_state

        # Emit the event to update the view
        EventManager.notify(Event.DELETE_DOCUMENT, element_id=self.document.id)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, marking the document with its previous
    #              state.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo the command, marking the document with its previous state.
        """
        # Set undo text
        self.setText(f"Revert delete document {self.document.id}")

        # Change the state of the cloned document and his children to the old state
        ProjectService.change_state(self.document.id, self.old_document_state)

        # Set the parent state to the old state
        self.document.parent.state: ProteusState = self.before_clone_parent_state

        # Emit the event to update the view
        EventManager.notify(Event.ADD_DOCUMENT, document=self.document)
