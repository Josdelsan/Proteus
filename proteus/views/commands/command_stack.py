# ==========================================================================
# File: command_stack.py
# Description: Command stack to manage undo and redo operations.
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoStack

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Class: CommandStack
# Description: Command stack class to manage undo and redo operations.
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class CommandStack():
    """
    Command stack class to manage undo and redo operations.
    """

    # Class attributes
    _stack : QUndoStack = None

    # ----------------------------------------------------------------------
    # Method     : get_instance
    # Description: Get the command stack instance
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def get_instance(cls):
        if cls._stack is None:
            cls._stack = QUndoStack()
        return cls._stack
    
    # ----------------------------------------------------------------------
    # Method     : push
    # Description: Push a command to the command stack
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def push(cls, command):
        cls.get_instance().push(command)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the last command
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def undo(cls):
        cls.get_instance().undo()

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the last command
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @classmethod
    def redo(cls):
        cls.get_instance().redo()
