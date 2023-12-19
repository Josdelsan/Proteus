# ==========================================================================
# File: markdown_edit.py
# Description: Markdown edit input widget for forms.
# Date: 14/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import markdown
from PyQt6.QtCore import (
    QSize,
)
from PyQt6.QtWidgets import (
    QWidget,
    QTextEdit,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils.translator import Translator


# --------------------------------------------------------------------------
# Class: MarkdownEdit
# Description: Markdown edit input widget for forms.
# Date: 14/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class MarkdownEdit(QWidget):
    """
    Markdown edit input widget for forms. It is composed by a QTextEdit
    and a QLabel. The user can interact with a button to display a preview
    of the markdown text.

    Similar to PyQt6 QLineEdit, QTextEdit, etc. It is used to retrieve the
    value of the user input.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 14/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Object initialization.
        """
        super().__init__(*args, **kwargs)

        # Initialize widgets variables
        self.input_box: QTextEdit = None
        self.display_box: QTextEdit = None
        self.mode_button: QPushButton = None

        # Translator
        self._translator = Translator()

        # Create input widget
        self.create_input()

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 14/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_input(self) -> None:
        """
        Create the widgets and configure the layout.
        """

        # Display box ------------------------------------------------------
        self.display_box = QTextEdit()
        self.display_box.setReadOnly(True)
        self.display_box.sizeHint = lambda: QSize(250, 100)
        self.display_box.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        self.display_box.setVisible(False)
        # self.display_box.setStyleSheet("background-color: white;")

        # Input box --------------------------------------------------------
        self.input_box = QTextEdit()
        self.input_box.setAcceptRichText(True)
        self.input_box.sizeHint = lambda: QSize(250, 100)
        self.input_box.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )

        # Mode button ------------------------------------------------------
        self.mode_button = QPushButton()
        self.mode_button.setText(self._translator.text("markdown_edit.preview"))
        self.mode_button.clicked.connect(self.on_mode_button_clicked)

        # Layout setup -----------------------------------------------------
        layout = QVBoxLayout()
        layout.addWidget(self.input_box)
        layout.addWidget(self.display_box)
        layout.addWidget(self.mode_button)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    # ----------------------------------------------------------------------
    # Method     : markdown
    # Description: Returns the text of the input box.
    # Date       : 14/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def markdown(self) -> bool:
        """
        Returns the checked state of the checkbox.
        """
        return self.input_box.toPlainText()

    # ----------------------------------------------------------------------
    # Method     : setMarkdown
    # Description: Sets the text of the input box.
    # Date       : 14/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setMarkdown(self, text: str) -> None:
        """
        Sets the checked state of the checkbox.
        """
        self.input_box.setPlainText(text)

    # ----------------------------------------------------------------------
    # Method     : setEnabled
    # Description: Sets the enabled state of the inputs widget.
    # Date       : 14/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setEnabled(self, enabled: bool) -> None:
        """
        Sets the input to enabled or disabled state modifying the browse
        button.
        """
        self.input_box.setEnabled(enabled)

    # ======================================================================
    # Slots (connected to signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Slot       : on_mode_button_clicked
    # Description: Slot connected to the mode button clicked signal.
    # Date       : 14/12/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def on_mode_button_clicked(self) -> None:
        """
        Slot connected to the mode button clicked signal.
        """
        # Enter edit mode
        if self.display_box.isVisible():
            self.display_box.setVisible(False)
            self.input_box.setVisible(True)
            self.mode_button.setText(self._translator.text("markdown_edit.preview"))
        # Enter preview mode
        else:
            text = self.input_box.toPlainText()
            converted_text: str = markdown.markdown(
                text,
                extensions=[
                    "markdown.extensions.fenced_code",
                    "markdown.extensions.codehilite",
                    "markdown.extensions.tables",
                    "markdown.extensions.toc",
                ],
            )

            self.display_box.setHtml(converted_text)
            self.display_box.setVisible(True)
            self.input_box.setVisible(False)
            self.mode_button.setText(self._translator.text("markdown_edit.edit"))
