# ==========================================================================
# File: clipboard.py
# Description: Clipboard module for Proteus application
# Date: 30/07/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
# TODO: Consider if this class could be interpreted as a ProteusComponent child
# of main_window and could be accessed through the main window instance instead
# of being a singleton class in the application layer.

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from enum import Enum
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.model import ProteusID, PROTEUS_DOCUMENT
from proteus.controller.command_stack import Controller
from proteus.application.utils.abstract_meta import SingletonMeta
from proteus.application.state_manager import StateManager
from proteus.application.resources.translator import translate as _
from proteus.application.events import ClipboardChangedEvent
from proteus.views.components.dialogs.base_dialogs import MessageBox


# logging configuration
log = logging.getLogger(__name__)


class ClipboardStatus(Enum):
    """
    Clipboard status enumeration for internal use in the Clipboard class.
    """

    COPY = 0
    CUT = 1
    CLEAR = 2


# --------------------------------------------------------------------------
# Class: Clipboard
# Description: Clipboard class for Proteus application. Handles the
#              cut/copy/paste operations
# Date: 30/07/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class Clipboard(metaclass=SingletonMeta):
    """
    Clipboard class for Proteus application. Handles the cut/copy/paste operations
    for the objects in the application.

    Clipboard operations can only be performed in objects. Documents are not
    allowed to be copied or cut.
    """

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Constructor for Clipboard class.
    # Date: 30/07/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self, controller: Controller) -> None:

        assert (
            controller is not None
        ), "Controller instance is required for Clipboard initialization"

        # NOTE: QClipboard is not used to avoid inconsistencies between the
        #       clipboard and the application state.
        self._clipboard: ProteusID = ProteusID("")
        self._controller: Controller = controller
        self._status: ClipboardStatus = ClipboardStatus.CLEAR
        
    # --------------------------------------------------------------------------
    # Getters
    # --------------------------------------------------------------------------

    def get_content(self) -> ProteusID | None:
        """
        Get the content of the clipboard.

        Returns: The ProteusID of the object in the clipboard or None if the
                 clipboard is empty or content invalid.
        """
        if self._status == ClipboardStatus.CLEAR:
            return None
        
        try:
            self._controller.get_element(self._clipboard)
            return self._clipboard
        except Exception as e:
            log.error(f"Error while getting content of clipboard: {e}")
            return None
        
    def get_status(self) -> ClipboardStatus:
        """
        Get the status of the clipboard.

        Returns: The status of the clipboard.
        """
        return self._status

    # --------------------------------------------------------------------------
    # Clipboard operations
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Method: cut
    # Description: Cut the current selected object to the clipboard. Check if the object
    #              exists in the project and if it is a valid object to be cut.
    # Date: 30/07/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def cut(self) -> bool:
        """
        Cut the current selected object to the clipboard. Check if the object
        exists in the project and if it is a valid object to be cut.

        Notify clipboard changed event if the cut operation was successful.

        Returns: True if the cut operation was successful, False otherwise.
        """

        object_id = StateManager().get_current_object()

        # Check if cut operation can be performed
        if not self.can_cut_and_copy():
            log.error(f"Cut operation cannot be performed when object with ProteusID '{object_id}' is selected")
            return False

        log.debug(
            f"Cut operation for object with ProteusID: {object_id}"
        )

        # Check if the object is a valid object to be cut
        self._clipboard = object_id
        self._status = ClipboardStatus.CUT

        # Notify clipboard change
        ClipboardChangedEvent().notify()

        return True

    # --------------------------------------------------------------------------
    # Method: copy
    # Description: Copy the current selected object to the clipboard. Check if the object
    #              exists in the project and if it is a valid object to be copied.
    # Date: 30/07/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def copy(self) -> bool:
        """
        Copy the current selected object to the clipboard. Check if the object
        exists in the project and if it is a valid object to be copied.

        Notify clipboard changed event if the copy operation was successful.

        Returns: True if the copy operation was successful, False otherwise.
        """

        object_id = StateManager().get_current_object()

        # Check if copy operation can be performed
        if not self.can_cut_and_copy():
            log.error(f"Copy operation cannot be performed when object with ProteusID '{object_id}' is selected")
            return False

        log.debug(
            f"Copy operation for object with ProteusID: {object_id}"
        )

        self._clipboard = object_id
        self._status = ClipboardStatus.COPY

        # Notify clipboard change
        ClipboardChangedEvent().notify()

        return True

    # --------------------------------------------------------------------------
    # Method: paste
    # Description: Paste the object in the clipboard into the current select object. Check if
    #              the object in the clipboard exists and if the parent object exists.
    # Date: 30/07/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def paste(self) -> bool:
        """
        Paste the object in the clipboard into the current select object. Check if
        the object in the clipboard exists and if the parent object exists.

        Notify clipboard changed event if the paste operation was successful.

        If the object in the clipboard was copied, a clone operation is performed.
        If the object in the clipboard was cut, a move operation is performed and
        the clipboard is cleared.

        Returns: True if the paste operation was successful, False otherwise.
        """

        # Check if clipboard is empty or CLEAR
        if self._clipboard == "" or self._status == ClipboardStatus.CLEAR:
            log.debug("Clipboard is empty, nothing to paste")

            MessageBox.information(
                _("clipboard.paste_action.message_box.empty_error.title"),
                _(
                    "clipboard.paste_action.message_box.empty_error.text",
                ),
            )

            return False

        # Check if paste operation can be performed
        if not self.can_paste():
            log.error("Paste operation cannot be performed")

            # If copy action is not allowed, show a message box
            MessageBox.warning(
                _("clipboard.paste_action.message_box.error.title"),
                _(
                    "clipboard.paste_action.message_box.error.text",
                ),
            )

            return False
        
        parent_id = StateManager().get_current_object()
        object_id = self._clipboard

        # Handle paste from copy operation ------------------------------
        if self._status == ClipboardStatus.COPY:
            return self._paste_copy(object_id, parent_id)
        # Handle paste from cut operation
        elif self._status == ClipboardStatus.CUT:
            return self._paste_cut(object_id, parent_id)
        else:
            log.error(
                f"No operation was performed, clipboard status is '{self._status}'"
            )
            return False

    def _paste_cut(self, object_id: ProteusID, parent_id: ProteusID) -> bool:
        """
        Private method to handle the paste operation from a cut operation.
        """
        log.debug(f"Paste operation, moving object with ProteusID: {object_id}")

        # Position check is already done in the move operation, if it fails it
        # will raise an exception.
        try:
            self._controller.change_object_position(object_id, parent_id)
        except Exception as e:
            log.error(
                f"Move operation failed for object with id '{object_id}' error: {e}"
            )
            return False

        self._clipboard = ProteusID("")
        self._status = ClipboardStatus.CLEAR

        # Notify clipboard change
        ClipboardChangedEvent().notify()

        return True

    def _paste_copy(self, object_id: ProteusID, parent_id: ProteusID) -> bool:
        """
        Private method to handle the paste operation from a copy operation.
        """
        log.debug(f"Paste operation, cloning object with ProteusID: {object_id}")

        try:
            self._controller.clone_object(object_id, parent_id)
        except Exception as e:
            log.error(
                f"Clone operation failed for object with id '{object_id}' error: {e}"
            )
            return False

        return True


    # --------------------------------------------------------------------------
    # Check operations
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Method: can_cut_and_copy
    # Description: Check if the current selected object can be copied or cut.
    # Date: 30/07/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def can_cut_and_copy(self) -> bool:
        """
        Check if the current selected object can be copied or cut.

        Returns: True if copy or cut operations can be performed, False otherwise.
        """

        object_id = StateManager().get_current_object()

        # Check if an object is selected
        if object_id is None:
            return False

        # Check if the object exists in the project
        try:
            object = self._controller.get_element(object_id)
        except Exception as e:
            log.warning(
                f"Error while checking if object with ProteusID '{object_id}' can be copied or cut: {e}"
            )
            return False

        # Check the object is not a document
        if PROTEUS_DOCUMENT in object.classes:
            log.warning(
                f"Documents cannot be copied or cut, ignoring object with ProteusID: {object_id}"
            )
            return False

        # Check the object is not in DEAD state
        if object.state == ProteusState.DEAD:
            log.warning(
                f"Object with ProteusID '{object_id}' is in DEAD state, cannot be copied or cut"
            )
            return False

        return True

    # --------------------------------------------------------------------------
    # Method: can_paste
    # Description: Check if the object in the clipboard can be pasted into the
    #              current selected object.
    # Date: 30/07/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def can_paste(self) -> bool:
        """
        Check if the object in the clipboard can be pasted into the
        current selected object. If there are inconsistencies in the clipboard
        or the object cannot be pasted, the clipboard is cleared and clipboard
        changed event is notified.

        Returns: True if the paste operation can be performed, False otherwise.
        """

        # Check clipboard status
        if self._status == ClipboardStatus.CLEAR:
            log.debug("Clipboard is CLEAR, nothing to paste")
            return False
        
        # Check if the object in the clipboard exists in the project
        if self._clipboard == "" or self._clipboard is None:
            log.error("Clipboard is empty, changing to CLEAR status")
            # Clear inconsistent clipboard
            self.clear()
            return False

        # Check if a parent object is selected
        parent_id = StateManager().get_current_object()
        if parent_id is None:
            return False

        # Check if the object and parent are valid objects
        try:
            parent = self._controller.get_element(parent_id)
            object = self._controller.get_element(self._clipboard)
        except Exception as e:
            log.warning(
                f"Error while checking if object with ProteusID '{self._clipboard}' can be pasted into '{parent_id}': {e}"
            )
            # Clear inconsistent clipboard
            self.clear()
            return False

        # Check the parent object is not in DEAD state
        if parent.state == ProteusState.DEAD or object.state == ProteusState.DEAD:
            log.warning(
                f"Object or parent object is in DEAD state, cannot be pasted. Object state: {object.state}, Parent state: {parent.state}"
            )
            # Clear inconsistent clipboard
            self.clear()
            return False

        # Check move and clone operations
        if self._status == ClipboardStatus.COPY:
            return parent.accept_descendant(object)
        elif self._status == ClipboardStatus.CUT:
            return self._controller.check_position_change(self._clipboard, parent_id)
        else:
            return False


    # --------------------------------------------------------------------------
    # Auxiliary methods
    # --------------------------------------------------------------------------

    def clear(self) -> None:
        """
        Clear the clipboard.

        Notify clipboard changed event.
        """
        self._clipboard = ProteusID("")
        self._status = ClipboardStatus.CLEAR
        ClipboardChangedEvent().notify()