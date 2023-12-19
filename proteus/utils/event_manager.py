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
import logging
from typing import List, Dict, Tuple
import threading

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------


# logging configuration
log = logging.getLogger(__name__)

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

    # Document events
    ADD_DOCUMENT = "add_document"
    DELETE_DOCUMENT = "delete_document"

    # Object events
    MODIFY_OBJECT = "modify_object"
    ADD_OBJECT = "add_object"
    DELETE_OBJECT = "delete_object"

    # Selection events
    SELECT_OBJECT = "select_object"
    CURRENT_DOCUMENT_CHANGED = "current_document_changed"
    CURRENT_VIEW_CHANGED = "current_view_changed"

    # Stack related events
    STACK_CHANGED = "stack_changed"
    REQUIRED_SAVE_ACTION = "required_save_action"

    # Render view events
    ADD_VIEW = "add_view"
    DELETE_VIEW = "delete_view"


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

    # Singleton instance
    __instance = None
    __lock = threading.Lock()  # Ensure thread safety

    # --------------------------------------------------------------------------
    # Method: __new__
    # Description: Singleton constructor for EventManager class.
    # Date: 16/11/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        It creates a singleton instance for EventManager class.
        """
        if not cls.__instance:
            log.info("Creating EventManager instance")
            cls.__instance = super(EventManager, cls).__new__(cls)
            cls.__instance._initialized = False
        return cls.__instance
    
    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Constructor for EventManager class.
    # Date: 16/11/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        It initializes the EventManager class.
        """
        # Check if the instance has been initialized
        with self.__class__.__lock:
            if self._initialized:
                return
            self._initialized = True

        # Instance variables
        self._events: Dict[Event, List[Tuple[callable, QWidget]]] = {}
        self._subscribed_components: Dict[QWidget, List[callable]] = {}

    # ----------------------------------------------------------------------
    # Method     : attach
    # Description: Attach a component method to an event
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
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

    # ----------------------------------------------------------------------
    # Method     : clear
    # Description: Clear the event manager
    # Date       : 14/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def clear(cls):
        """
        Clear the event manager.

        NOTE: This method is used for testing purposes.
        """

        cls._events = {}
        cls._subscribed_components = {}

