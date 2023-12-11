# ==========================================================================
# File: web_channel_object.py
# Description: PyQT6 web channel object class for the PROTEUS application
# Date: 11/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import pyqtSlot

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.views.components.abstract_component import ProteusComponent
from proteus.views.components.dialogs.property_dialog import PropertyDialog

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: WebChannelObject
# Description: PyQT6 WebChannel object class for the PROTEUS application
# Date: 11/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class WebChannelObject(ProteusComponent):
    @pyqtSlot(str)
    def open_properties_dialog(self, id: str) -> None:
        """
        Open the edit properties dialog for the given object id
        :param id: object id
        """
        if not id:
            log.error(
                f"Method 'open_edit_properties_dialog' called with empty id '{id}'"
            )
            return
        
        proteus_id = ProteusID(id)

        log.debug(
            f"Object '{proteus_id}' was double clicked in the document html, opening edit properties dialog"
        )

        # Create the dialog
        PropertyDialog.create_dialog(self._controller, proteus_id)
