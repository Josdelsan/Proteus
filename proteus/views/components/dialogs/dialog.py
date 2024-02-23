# ==========================================================================
# File: dialog.py
# Description: Proteus base dialog class and utilities
# Date: 23/02/2024
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

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFontMetrics
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QDialogButtonBox,
    QFormLayout,
    QDialog,
    QToolButton,
    QLayout,
    QSizePolicy,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils.translator import Translator
from proteus.utils.dynamic_icons import DynamicIcons
from proteus.utils import ProteusIconType
from proteus.views.components.abstract_component import ProteusComponent


# Module configuration
_ = Translator().text  # Translator
log = logging.getLogger(__name__)  # Logger


# --------------------------------------------------------------------------
# Class: ProteusDialog
# Description: Class for the PROTEUS application base dialog
# Date: 23/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ProteusDialog(QDialog, ProteusComponent):

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Class constructor
    # Date: 23/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(ProteusDialog, self).__init__(*args, **kwargs)

        # Variables --------------------------------

        # Buttons
        self.accept_button: QToolButton
        self.reject_button: QToolButton

        # Content
        self._content_widget: QWidget = None
        self._content_layout: QLayout = None

        # Layouts
        self._buttons_layout: QVBoxLayout
        self._dialog_layout: QHBoxLayout

        # Dialog configuration --------------------

        # Icon may be overriden by the child class
        proteus_icon = DynamicIcons().icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(proteus_icon)

        self._content_widget = QWidget()
        self._content_widget.setObjectName("dialog_content_widget")

        button_box = QDialogButtonBox()
        button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.accept_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.accept_button.setText(_("dialog.accept_button"))

        self.reject_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.reject_button.setText(_("dialog.reject_button"))


        us_logo: QIcon = DynamicIcons().icon(ProteusIconType.App, "US-digital")
        us_logo_label: QLabel = QLabel()
        us_logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        us_logo_label.setPixmap(us_logo.pixmap(80, 80))

        self._buttons_layout = QVBoxLayout()
        self._buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._buttons_layout.addWidget(self.accept_button)
        self._buttons_layout.addWidget(self.reject_button)
        self._buttons_layout.addStretch()
        self._buttons_layout.addWidget(us_logo_label)

        # Main layout
        self._dialog_layout = QHBoxLayout()
        self._dialog_layout.addLayout(self._buttons_layout)
        self.setLayout(self._dialog_layout)

    # --------------------------------------------------------------------------
    # Method: set_content_layout
    # Description: Set the content layout
    # Date: 23/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def set_content_layout(self, layout: QLayout) -> None:
        """
        Set the content layout
        """

        assert not isinstance(
            self._content_layout, QLayout
        ), "Content layout is already set."

        self._content_widget.setLayout(layout)

        self._content_layout = layout
        self._dialog_layout.insertWidget(0, self._content_widget)
