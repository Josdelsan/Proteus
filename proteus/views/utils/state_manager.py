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
        cls.current_document = document_id
        EventManager.notify(
            Event.CURRENT_DOCUMENT_CHANGED, document_id=cls.current_document
        )

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
        Returns the current document id.
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
        Returns the current object id for the current document.
        """

        document_id = cls.get_current_document()

        assert (
            document_id is not None
        ), "A document must be selected before getting the current object."

        assert (
            document_id in cls.current_object
        ), f"Document id {document_id} not found in current application state dictionary."

        return cls.current_object[document_id]
