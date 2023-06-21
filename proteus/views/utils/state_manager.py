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

from enum import Enum
from typing import List, Dict, Tuple

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model import ProteusID
from proteus.views.utils.event_manager import EventManager, Event


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

    # Class attributes
    current_document: ProteusID = None
    current_object: Dict[ProteusID, ProteusID] = {}

    # --------------------------------------------------------------------------
    # Method: set_current_document
    # Description: Sets the current document id.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @classmethod
    def set_current_document(cls, document_id: ProteusID) -> None:
        """
        Sets the current document id.
        """
        proteus.logger.info(f"Setting current document {document_id}")
        cls.current_document = document_id

        # If the current document is not in the current object dictionary,
        # add it.
        if document_id not in cls.current_object:
            cls.current_object[document_id] = None

        # Notify the event manager that the current document has changed
        # and that the current object must be updated.
        EventManager.notify(
            Event.CURRENT_DOCUMENT_CHANGED, document_id=cls.current_document
        )
        EventManager.notify(Event.SELECT_OBJECT)

    # --------------------------------------------------------------------------
    # Method: get_current_document
    # Description: Returns the current document id.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @classmethod
    def get_current_document(cls) -> ProteusID:
        """
        Returns the current document id. If no document is selected, it returns
        None.
        """
        return cls.current_document

    # --------------------------------------------------------------------------
    # Method: set_current_object
    # Description: Sets the current object id for the current document.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @classmethod
    def set_current_object(cls, object_id: ProteusID, document_id: ProteusID) -> None:
        """
        Sets the current object id for the current document.
        """
        proteus.logger.info(f"Selecting object {object_id} in document {document_id}")
        cls.current_object[document_id] = object_id
        EventManager.notify(Event.SELECT_OBJECT)

    # --------------------------------------------------------------------------
    # Method: get_current_object
    # Description: Returns the current object id for the current document.
    # Date: 19/06/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @classmethod
    def get_current_object(cls) -> ProteusID:
        """
        Returns the current object id for the current document. If no object
        is selected, it returns None.
        """
        document_id = cls.get_current_document()

        # If no document is selected, return None.
        if document_id is None:
            return None

        assert (
            document_id in cls.current_object
        ), f"Document id {document_id} not found in current application state dictionary."

        return cls.current_object[document_id]

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
    @classmethod
    def deselect_object(cls, object_id: ProteusID) -> None:
        """
        Deselects the current object if found selected in the state manager
        dictionary.

        This method is primarily used when objects are marked as deleted (DEAD)
        when controller commands are executed.
        """
        for document_id in cls.current_object:
            if cls.current_object[document_id] == object_id:
                cls.current_object[document_id] = None
                EventManager.notify(Event.SELECT_OBJECT)
