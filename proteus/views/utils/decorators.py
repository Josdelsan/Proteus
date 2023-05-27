# ==========================================================================
# File: decorators.py
# Description: Decorators for the PROTEUS application views
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.utils.event_manager import EventManager, Event


# ----------------------------------------------------------------------
# function   : subscribe_to (decorator)
# Description: Decorator for the PROTEUS application views. It is used
#              to subscribe the component to the events of the
#              application.
# Date       : 25/05/2023
# Version    : 0.1
# Author     : José María Delgado Sánchez
# ----------------------------------------------------------------------
def subscribe_to(update_events : List[Event] = []):
    """
    Decorator for the PROTEUS application views. It is used to subscribe
    the component to the events of the application.

    :param update_events: List of events to subscribe to (default: empty list)
    """
    def decorator(cls):

        # Call the original __init__ method before subscribing to events
        # Override the __init__ method of the class
        original_init = cls.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            # Subscribe to events
            for event in update_events:
                EventManager.attach(event, self)
        cls.__init__ = new_init
        return cls
    return decorator
