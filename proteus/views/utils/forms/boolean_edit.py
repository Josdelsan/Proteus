# ==========================================================================
# File: boolean_edit.py
# Description: Boolean edit input widget for forms.
# Date: 12/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtWidgets import (
    QWidget,
    QCheckBox,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.utils.translator import Translator


# --------------------------------------------------------------------------
# Class: BooleanEdit
# Description: Boolean edit input widget for forms.
# Date: 12/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class BooleanEdit(QWidget):
    """
    Boolean edit input widget for forms. It is composed by a QCheckBox and a
    QLabel that shows the tooltip if any.

    Similar to PyQt6 QLineEdit, QTextEdit, etc. It is used to retrieve the
    value of the user input.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 12/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, tooltip: str = "", *args, **kwargs):
        """
        Object initialization.
        """
        super().__init__(*args, **kwargs)

        # Initialize widgets variables
        self.checkbox: QCheckBox = None
        self.label: QLabel = None

        # Initialize variables
        self.tooltip_str: str = tooltip

        # Translator
        self._translator = Translator()

        # Create input widget
        self.create_input()

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 12/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_input(self) -> None:
        """
        Create the widgets and configure the layout.
        """

        # Widgets creation --------------------------------------------------
        self.checkbox = QCheckBox()
        self.label = QLabel()
        self.label.setText(self._translator.text(self.tooltip_str))
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Layout setup -----------------------------------------------------
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)

        # Set alignment for the layout
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    # ----------------------------------------------------------------------
    # Method     : checked
    # Description: Returns the checked state of the checkbox.
    # Date       : 12/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def checked(self) -> bool:
        """
        Returns the checked state of the checkbox.
        """
        return self.checkbox.isChecked()

    # ----------------------------------------------------------------------
    # Method     : setChecked
    # Description: Sets the checked state of the checkbox.
    # Date       : 12/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setChecked(self, checked: bool) -> None:
        """
        Sets the checked state of the checkbox.
        """
        state = Qt.CheckState.Checked if bool(checked) else Qt.CheckState.Unchecked
        self.checkbox.setCheckState(state)

    # ----------------------------------------------------------------------
    # Method     : setEnabled
    # Description: Sets the enabled state of the inputs widget.
    # Date       : 12/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setEnabled(self, enabled: bool) -> None:
        """
        Sets the input to enabled or disabled state modifying the browse
        button.
        """
        self.checkbox.setEnabled(enabled)

    # ======================================================================
    # Slots (connected to signals)
    # ======================================================================
