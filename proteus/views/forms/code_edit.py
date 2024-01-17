# ==========================================================================
# File: code_edit.py
# Description: Code edit input widget for forms.
# Date: 10/11/2023
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
    QSize,
)
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Class: CodeEdit
# Description: Code edit input widget for forms.
# Date: 10/11/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class CodeEdit(QWidget):
    """
    Code edit input widget for forms. It is composed by a multiples QLineEdit
    widgets to let the user input prefix, number and suffix separately.

    Similar to PyQt6 QLineEdit, QTextEdit, etc. It is used to retrieve the
    value of the user input.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 10/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Object initialization.
        """
        super().__init__(*args, **kwargs)

        # Initialize widgets
        self.prefix_input: QLineEdit = None
        self.number_input: QLineEdit = None
        self.suffix_input: QLineEdit = None

        # Create input widget
        self.create_input()


    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 10/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_input(self) -> None:
        """
        Create the widgets and configure the layout.
        """

        # Widgets creation --------------------------------------------------
        self.prefix_input = QLineEdit()
        self.number_input = QLineEdit()
        self.suffix_input = QLineEdit()

        # Set QLineEdit alignments
        self.prefix_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.number_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        # Reimplement sizeHint to set a minimun width of 35px
        # NOTE: Recomended in https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qwidget.html
        self.prefix_input.sizeHint = lambda: QSize(35, 0)
        self.number_input.sizeHint = lambda: QSize(15, 0)
        self.suffix_input.sizeHint = lambda: QSize(35, 0)

        # Set size policy
        self.prefix_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.number_input.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.suffix_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Layout setup -----------------------------------------------------
        layout = QHBoxLayout()
        layout.addWidget(self.prefix_input)
        layout.addWidget(self.number_input)
        layout.addWidget(self.suffix_input)

        # Set alignment for the layout
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


    # ----------------------------------------------------------------------
    # Method     : code
    # Description: Returns the code.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def code(self) -> (str, str, str):
        """
        Returns the prefix, number and suffix of the code.
        """
        prefix: str = self.prefix_input.text()
        number: str = self.number_input.text()
        suffix: str = self.suffix_input.text()
        return prefix, number, suffix
    
    # ----------------------------------------------------------------------
    # Method     : setCode
    # Description: Sets the code.
    # Date       : 10/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setCode(self, prefix: str, number: str, suffix: str) -> None:
        """
        Sets the code.
        """
        self.prefix_input.setText(prefix)
        self.number_input.setText(number)
        self.suffix_input.setText(suffix)

    # ----------------------------------------------------------------------
    # Method     : setEnabled
    # Description: Sets the enabled state of the inputs widget.
    # Date       : 10/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setEnabled(self, enabled: bool) -> None:
        """
        Sets the input to enabled or disabled state modifying QLineEdit widgets.
        """
        self.prefix_input.setEnabled(enabled)
        self.number_input.setEnabled(enabled)
        self.suffix_input.setEnabled(enabled)

    
    # ======================================================================
    # Slots (connected to signals)
    # ======================================================================