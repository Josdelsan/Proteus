# ==========================================================================
# File: state_manager.py
# Description: State manager for the PROTEUS application. It manages the
#              state of the current selected object and the current selected
#              document.
# Date: 19/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================


# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict
import logging
import threading

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.utils.event_manager import EventManager, Event

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: StateManager
# Description: State manager for the PROTEUS application.
# Date: 19/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class StateManager:
    """
    State manager for the PROTEUS application. It stores the current
    selected document and the selected object for each document tree.
    """

    # Singleton instance
    __instance = None
    __lock = threading.Lock()  # Ensure thread safety

    # --------------------------------------------------------------------------
    # Method: __new__
    # Description: Singleton constructor for StateManager class.
    # Date: 15/11/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        It creates a singleton instance for StateManager class.
        """
        if not cls.__instance:
            log.info("Creating StateManager instance")
            cls.__instance = super(StateManager, cls).__new__(cls)
            cls.__instance._initialized = False
        return cls.__instance
    
    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Constructor for StateManager class.
    # Date: 15/11/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        It initializes the StateManager class.
        """
        # Check if the instance has been initialized
        with self.__class__.__lock:
            if self._initialized:
                return
            self._initialized = True

        # Instance variables
        self.current_document: ProteusID = None
        self.current_object: Dict[ProteusID, ProteusID] = {}
        self.current_view: str = None

    # --------------------------------------------------------------------------
    # Method: set_current_document
    # Description: Sets the current document id.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def set_current_document(self, document_id: ProteusID) -> None:
        """
        Sets the current document id.
        """
        log.debug(f"Setting current document {document_id}")
        self.current_document = document_id

        # If the current document is not in the current object dictionary,
        # add it.
        if document_id not in self.current_object:
            self.current_object[document_id] = None

        # Notify the event manager that the current document has changed
        # and that the current object must be updated.
        EventManager().notify(
            Event.CURRENT_DOCUMENT_CHANGED, document_id=self.current_document
        )

    # --------------------------------------------------------------------------
    # Method: get_current_document
    # Description: Returns the current document id.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def get_current_document(self) -> ProteusID:
        """
        Returns the current document id. If no document is selected, it returns
        None.
        """
        return self.current_document

    # --------------------------------------------------------------------------
    # Method: set_current_object
    # Description: Sets the current object id for the current document.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def set_current_object(self, object_id: ProteusID, document_id: ProteusID) -> None:
        """
        Sets the current object id for the current document.
        """
        log.debug(f"Selecting object {object_id} in document {document_id}")
        self.current_object[document_id] = object_id
        EventManager().notify(Event.SELECT_OBJECT)

    # --------------------------------------------------------------------------
    # Method: get_current_object
    # Description: Returns the current object id for the current document.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def get_current_object(self) -> ProteusID:
        """
        Returns the current object id for the current document. If no object
        is selected, it returns None.
        """
        document_id = self.get_current_document()

        # If no document is selected, return None.
        if document_id is None:
            return None

        assert (
            document_id in self.current_object
        ), f"Document id {document_id} not found in current application state dictionary."

        return self.current_object[document_id]

    # --------------------------------------------------------------------------
    # Method: deselect_object
    # Description: Deselects the current object if found selected in the state
    #              manager dictionary.
    # Date: 21/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    # NOTE: This method is primarily used when objects are marked as deleted
    #       (DEAD) when controller commands are executed.
    def deselect_object(self, object_id: ProteusID) -> None:
        """
        Deselects the current object if found selected in the state manager
        dictionary.

        This method is primarily used when objects are marked as deleted (DEAD)
        when controller commands are executed.
        """
        for document_id in self.current_object:
            if self.current_object[document_id] == object_id:
                self.current_object[document_id] = None
                EventManager().notify(Event.SELECT_OBJECT)

    # --------------------------------------------------------------------------
    # Method: set_current_view
    # Description: Sets the current view id.
    # Date: 03/07/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def set_current_view(self, view_name: str) -> None:
        """
        Sets the current view id.
        """
        log.debug(f"Setting current view {view_name}")
        self.current_view = view_name

        # Notify the event manager that the current view has changed.
        EventManager().notify(Event.CURRENT_VIEW_CHANGED, view_name=view_name)

    # --------------------------------------------------------------------------
    # Method: get_current_view
    # Description: Returns the current view id.
    # Date: 03/07/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def get_current_view(self) -> str:
        """
        Returns the current view id. If no view is selected, it returns None.
        """
        return self.current_view
    
    # --------------------------------------------------------------------------
    # Method: clear
    # Description: Clears the current state manager.
    # Date: 15/11/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def clear(self) -> None:
        """
        Clears the current state manager.
        """
        log.debug("Clearing state manager")
        self.current_document = None
        self.current_object = {}
        self.current_view = None