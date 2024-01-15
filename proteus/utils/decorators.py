# ==========================================================================
# File: decorators.py
# Description: Decorators used in views modules or frontend related modules
# Date: 12/09/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from functools import wraps
import time

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Decorator: proteus_action
# Description: Handles application state when an action is performed by the
# user. It sets the cursor to wait shape.
# Date: 12/09/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def proteus_action(func):
    """
    Handles application state when an action is performed by the
    user. It sets the cursor to wait shape.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Set cursor to wait shape
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))

            # Function call -----------------------
            func_result = func(*args, **kwargs)
        finally:
            # Set cursor to default shape
            QApplication.restoreOverrideCursor()

        return func_result
    return wrapper

def benchmark(func):
    """
    Decorator used to measure the time that takes to execute a function.
    """
    def wrapper(*args, **kwargs):
        t = time.perf_counter()
        res = func(*args, **kwargs)
        total = time.perf_counter()-t

        # Print in ms
        print(f"{func.__name__}: {total*1000:0.4f} ms")
        return res
    return wrapper  
    