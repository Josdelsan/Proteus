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

from proteus.services.service_manager import ServiceManager
from proteus.views.utils.event_manager import Event, EventManager


# ----------------------------------------------------------------------
# function    : component
# Description: Decorator for the PROTEUS application views. It is used
#              to create the components of the frontend.
# Date       : 25/05/2023
# Version    : 0.1
# Author     : José María Delgado Sánchez
# ----------------------------------------------------------------------
def component(base_cls, update_events : List[Event] = []):
    """
    Decorator for the PROTEUS application views. It is used to create the
    components of the frontend. Handles the creation of the component,
    dependency injection and event subscription.

    :param base_cls: Base class of the component(PyQT6 class)
    :param update_events: List of events to subscribe to (default: empty list)
    """
    def decorator_func(cls):

        # ----------------------------------------------------------------------
        # class      : Component
        # Description: Component class for the PROTEUS application views.
        # Date       : 25/05/2023
        # Version    : 0.1
        # Author     : José María Delgado Sánchez
        # ----------------------------------------------------------------------
        class Component(cls, base_cls):
            def __init__(self, parent, *args, **kwargs):
                super().__init__(parent, *args, **kwargs)

                # Parent widget
                self.parent = parent

                # Dependency injection
                self.archetype_service = ServiceManager.get_archetype_service_instance()
                self.project_service = ServiceManager.get_project_service_instance()

                # Create the component
                self.create_component()

                # Subscribe to events
                for event in update_events:
                    EventManager.attach(event, self)

        return Component
    return decorator_func