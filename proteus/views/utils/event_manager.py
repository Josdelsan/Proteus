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
from typing import List, Dict, Tuple

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget

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
    ADD_OBJECT = "add_object"
    DELETE_OBJECT = "delete_object"

    # Selection events
    SELECT_OBJECT = "select_object"
    DESELECT_OBJECT = "deselect_object"

    # Document events
    ADD_DOCUMENT = "add_document"
    DELETE_DOCUMENT = "delete_document"

    # Stack related events
    STACK_CHANGED = "stack_changed"


# --------------------------------------------------------------------------
# Class: EventManager
# Description: Event manager for the PROTEUS events.
# Date: 05/06/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class EventManager:
    """
    Event manager for the PROTEUS events. It is used to notify the components
    of the frontend when an event is triggered.
    """

    # Class attributes
    _events: Dict[Event, List[Tuple[callable, QWidget]]] = {}
    _subscribed_components: Dict[QWidget, List[callable]] = {}

    # ----------------------------------------------------------------------
    # Method     : attach
    # Description: Attach a component method to an event
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def attach(cls, event: Event, method: callable, component: QWidget):
        """
        Attach a component to an event.
        """

        # Check if the event was already registered
        if event not in cls._events:
            cls._events[event] = []

        # Check if the component was already registered
        if component not in cls._subscribed_components:
            cls._subscribed_components[component] = []

        cls._events[event].append((method, component))
        cls._subscribed_components[component].append(method)

    # ----------------------------------------------------------------------
    # Method     : detach
    # Description: Detach a component to an event
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def detach(cls, component: QWidget):
        """
        Detach all the methods of a component from all the events.
        """

        # Check if the component was already registered
        if component in cls._subscribed_components:
            # Detach the component from all the events
            for event in cls._events:
                # Iterate over the methods of the event
                for method, instance in cls._events[event]:
                    # Check if the method belongs to the component
                    if method in cls._subscribed_components[component]:
                        cls._events[event].remove((method, instance))
                        cls._subscribed_components[component].remove(method)

            # Remove the component from the subscribed components
            cls._subscribed_components.pop(component)

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
            for method, component in cls._events[event]:
                method(component, *args, **kwargs)
