# ==========================================================================
# File: event_manager.py
# Description: Event manager for the PROTEUS events.
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from enum import Enum
from typing import List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Enum: Event
# Description: Events in the frontend of the PROTEUS application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class Event(Enum):
    # Project events
    OPEN_PROJECT = "open_project"
    SAVE_PROJECT = "save_project"

    # Object events
    MODIFY_OBJECT = "modify_object"
    CLONE_OBJECT = "clone_object"
    DELETE_OBJECT = "delete_object"
    SELECT_OBJECT = "select_object"

    # Document events
    CLONE_DOCUMENT = "clone_document"
    DELETE_DOCUMENT = "delete_document"

    # Stack related events
    STACK_CHANGED = "stack_changed"
    

# --------------------------------------------------------------------------
# Class: EventManager
# Description: Event manager for the PROTEUS events.
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class EventManager():
    """
    Event manager for the PROTEUS events. It is used to notify the components
    of the frontend when an event is triggered.
    """

    # Class attributes
    _events : Dict[Event, List] = {}

    # ----------------------------------------------------------------------
    # Method     : attach
    # Description: Attach a component to an event
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def attach(cls, event: Event, component):
        """
        Attach a component to an event.
        """

        # Check if the event was already registered
        if event not in cls._events:
            cls._events[event] = []

        cls._events[event].append(component)

    # ----------------------------------------------------------------------
    # Method     : detach
    # Description: Detach a component to an event
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def detach(cls, event: Event, component):
        """
        Detach a component to an event.
        """

        # Check if the event exists
        if event in cls._events:
            cls._events[event].remove(component)

    # ----------------------------------------------------------------------
    # Method     : notify
    # Description: Notify the components of an event
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def notify(cls, event: Event, *args, **kwargs):
        """
        Notify the components of an event. Adittionally, it passes the
        arguments and keyword arguments to the components.
        """

        # Check if the event exists
        if event in cls._events:
            # Notify the components
            for component in cls._events[event]:
                component.update_component(event, *args, **kwargs)
