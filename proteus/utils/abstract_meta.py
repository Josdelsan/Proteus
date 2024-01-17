# ==========================================================================
# File: abstract_meta.py
# Description: Helper module for creating abstract classes from PyQt6 classes
# Date: 31/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from abc import ABC

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import QObject

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Class: AbstractObjectMeta
# Description: Metaclass for QObject abstract class
# Date: 15/11/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
# NOTE: Workaround to allow multiple inheritance from QObject and ABC
# https://stackoverflow.com/questions/28720217/multiple-inheritance-metaclass-conflict
# https://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
class AbstractObjectMeta(type(QObject), type(ABC)):
    """
    Metaclass for QObject abstract class. It is used to create an abstract class
    that inherits from QObject and ABC.
    """

    pass
