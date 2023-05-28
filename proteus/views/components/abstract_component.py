# ==========================================================================
# File: abstract_component.py
# Description: Abstract component class for the PROTEUS application
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from abc import abstractmethod

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Class: AbstractComponent
# Description: AbstractComponent class for the PROTEUS application
#              components. It provides the basic methods to create and
#              update a component. It also provides the element_id
#              attribute to identify the component if it is necessary.
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
# NOTE: Cannot inherit from ABC because it is not compatible with PyQt6
#       metaclasses.
class AbstractComponent():
    """
    AbstractComponent class for the PROTEUS application components. It
    provides the basic methods to create and update a component. It also
    provides the element_id attribute to identify the component if it is
    necessary.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, optionally set the element_id
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, element_id : str = None) -> None:
        self.element_id = element_id


    # ----------------------------------------------------------------------
    # Method     : create_component (abstract)
    # Description: Abstract method to create the component
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @abstractmethod
    def create_component(self):
        pass

    # ----------------------------------------------------------------------
    # Method     : update_component (abstract)
    # Description: Abstract method to update the component
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @abstractmethod
    def update_component(self, event, *args, **kwargs):
        pass

    