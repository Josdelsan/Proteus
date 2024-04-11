# ==========================================================================
# File: abstract_meta.py
# Description: Helper module for creating meta classes for Proteus classes
# Date: 31/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from abc import ABC
from threading import Lock

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


# --------------------------------------------------------------------------
# Class: SingletonMeta
# Description: Metaclass for Singleton classes
# Date: 07/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class SingletonMeta(type):
    """
    Metaclass for Singleton classes. It is used to create a singleton class.

    Thread-safe implementation. Do not instantiate a singleton class inside
    the __init__ method of another singleton class. It will cause a deadlock.
    """

    _instances = {}         # Instances
    _lock: Lock = Lock()    # Ensure thread safety


    def __call__(cls, *args, **kwargs):
        """
        Accessed when the class is called, creates a new instance if it does not
        exist.
        """

        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]