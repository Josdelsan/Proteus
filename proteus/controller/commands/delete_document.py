# ==========================================================================
# File: delete_document.py
# Description: Controller to delete an document.
# Date: 03/06/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# ==========================================================================
# update: 30/10/2023 (José María)
# - Added support for traces management
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoCommand

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.model.trace import Trace
from proteus.model.abstract_object import ProteusState
from proteus.services.project_service import ProjectService
from proteus.application.events import (
    ModifyObjectEvent,
    DeleteDocumentEvent,
    AddDocumentEvent,
)


# --------------------------------------------------------------------------
# Class: DeletedocumentCommand
# Description: Controller class delete an document.
# Date: 03/06/2023
# Version: 0.2
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
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, document_id: ProteusID, project_service: ProjectService):
        super(DeleteDocumentCommand, self).__init__()

        # Dependency injection
        assert isinstance(
            project_service, ProjectService
        ), "Must provide a project service instance to the command"
        self.project_service = project_service

        # Command attributes
        self.before_clone_parent_state: ProteusState = None
        self.document: Object = self.project_service._get_element_by_id(document_id)
        self.old_document_state: ProteusState = self.document.state
        self.old_position: int = self.document.parent.get_descendants().index(
            self.document
        )

        # Atributed related to traces management
        self.new_sources_traces: Dict[ProteusID, List[Trace]] = {}
        self.old_sources_traces: Dict[ProteusID, List[Trace]] = {}
        self.old_sources_states: Dict[ProteusID, ProteusState] = {}
        self.calculate_traces_changes()

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the command, deleting the document.
    # Date       : 03/06/2023
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo the command, deleting the document.
        """
        # Set redo text
        self.setText(f"Mark as DEAD document {self.document.id}")

        # Change the state of the cloned document and his children to FRESH
        self.project_service.change_state(self.document.id, ProteusState.DEAD)

        # Modify the parent state depending on its current state
        self.before_clone_parent_state: ProteusState = self.document.parent.state

        if self.before_clone_parent_state is ProteusState.CLEAN:
            after_clone_parent_state: ProteusState = ProteusState.DIRTY
        else:
            after_clone_parent_state: ProteusState = self.before_clone_parent_state

        self.document.parent.state = after_clone_parent_state

        # Update the traces that where pointing to the object or its children
        for source in self.new_sources_traces.keys():
            self.project_service.update_traces(source, self.new_sources_traces[source])

            # Emit MODIFY_OBJECT event
            # update_view flag prevents the view to be updated every time a source is modified
            # The document view is supposed to be updated just once, when the command is finished
            ModifyObjectEvent().notify(source, False)

        # Emit the event to update the view
        DeleteDocumentEvent().notify(self.document.id)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, marking the document with its previous
    #              state.
    # Date       : 03/06/2023
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo the command, marking the document with its previous state.
        """
        # Set undo text
        self.setText(f"Revert delete document {self.document.id}")

        # Change the state of the cloned document and his children to the old state
        self.project_service.change_state(self.document.id, self.old_document_state)

        # Set the parent state to the old state
        self.document.parent.state = self.before_clone_parent_state

        # Update the traces that where pointing to the object or its children
        # NOTE: We assume that old_sources_traces and old_sources_states have the same keys
        for source in self.old_sources_traces.keys():
            # Update the traces
            self.project_service.update_traces(source, self.old_sources_traces[source])

            # Restore the old state of the source object
            source_object: Object = self.project_service._get_element_by_id(source)
            source_object.state = self.old_sources_states[source]

            # Emit MODIFY_OBJECT event
            # update_view flag prevents the view to be updated every time a source is modified
            # The document view is supposed to be updated just once, when the command is finished
            ModifyObjectEvent().notify(source, False)

        # Emit the event to update the view
        AddDocumentEvent().notify(self.document.id, self.old_position)

    # ----------------------------------------------------------------------
    # Method     : calculate_traces_changes
    # Description: Calculate the traces that will be affected by the deletion
    #              of the object and its children. Stores new and old traces
    #              by source object id. Also stores the old state of the
    #              source objects.
    # Date       : 30/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def calculate_traces_changes(self) -> None:
        """
        Calculate the traces that will be affected by the deletion of the object and its children.
        Stores new and old traces by source object id. Also stores the old state of the source objects.
        """
        # Calculated variables
        self.new_sources_traces = {}
        self.old_sources_traces = {}
        self.old_sources_states = {}

        # Update the traces of the object and its children
        traces_dependencies = self.project_service.get_traces_dependencies_outside(
            self.document.id
        )
        for target in traces_dependencies.keys():
            # For each object (source) that points to the target object
            source: ProteusID
            for source in traces_dependencies[target]:
                # Get the element
                source_object: Object = self.project_service._get_element_by_id(source)

                # Store the old state of the source object
                self.old_sources_states[source] = source_object.state

                # Iterate over the traces to find the traces that point to the target object
                trace: Trace
                new_traces: List[Trace] = []
                old_traces: List[Trace] = []
                for trace in source_object.traces.values():
                    # If the target is found in the trace, create the new trace and store the old one
                    if target in trace.targets:
                        # Store the old trace
                        old_traces.append(trace)

                        # Create the new trace
                        new_targets: List = trace.targets.copy()
                        new_targets.remove(target)
                        new_trace: Trace = trace.clone(new_targets)
                        new_traces.append(new_trace)

                # Store the new and old traces in the dictionaries
                self.new_sources_traces[source] = new_traces
                self.old_sources_traces[source] = old_traces

                # Check both lists are not empty
                assert len(new_traces) > 0 and len(old_traces) > 0, (
                    f"New or old traces list is empty for source {source}."
                    "Check get_traces_dependencies method behavior."
                    "If the target is not found in any trace, the source should not be in the list."
                )
