# ==========================================================================
# File: text_edit.py
# Description: Text edit input widget for forms.
# Date: 08/05/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


from PyQt6.QtGui import (
    QMouseEvent,
    QContextMenuEvent,
    QTextCursor,
)
from PyQt6.QtCore import (
    QEvent,
    Qt,
)
from PyQt6.QtWidgets import (
    QTextEdit,
    QWidget,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.spellcheck import SpellCheckHighlighter, SpellCheckerWrapper
from proteus.application.resources.translator import Translator


# Module configuration
_ = Translator().text  # Translator

# --------------------------------------------------------------------------
# Class: TextEdit
# Description: Text edit input widget for forms.
# Date: 08/05/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class TextEdit(QTextEdit):
    """
    Text edit input widget for forms. It is used to retrieve the
    text input from the user.

    Implements spellchecking using QSyntaxHighlighter.

    Similar to PyQt6 QLineEdit, QTextEdit, etc.
    """

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Constructor method.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self, parent: QWidget = None):
        """
        Constructor method.
        """
        super().__init__(parent)
        self._highlighter = SpellCheckHighlighter(self.document())
        self._spellchecker = SpellCheckerWrapper()


    # --------------------------------------------------------------------------
    # Method: mousePressEvent
    # Description: Override mousePressEvent to handle right click as left click
    #              so the cursor is placed in the correct position.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Override mousePressEvent to handle right click as left click so the
        cursor is placed in the correct position.
        """
        if event.button() == Qt.MouseButton.RightButton:
            event = QMouseEvent(
                QEvent.Type.MouseButtonPress,
                event.pos().toPointF(),
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )
        super().mousePressEvent(event)


    # --------------------------------------------------------------------------
    # Method: contextMenuEvent
    # Description: Override contextMenuEvent to add spellcheck suggestions.
    # Date: 08/05/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        """
        Override contextMenuEvent to add spellcheck suggestions.
        """
        self.contextMenu = self.createStandardContextMenu()

        textCursor = self.textCursor()

        # If there is no selection, select the word under the cursor to check
        if not textCursor.hasSelection():

            # TODO: Avoid selecting special characters so they are not replaced
            textCursor.select(QTextCursor.SelectionType.WordUnderCursor)
            self.setTextCursor(textCursor)
            word = textCursor.selectedText()

            if self._spellchecker.check(word) is False:
                self.contextMenu.addSeparator()

                suggestions = self._spellchecker.suggest(word) 

                # TODO: Handle misspelled words that have no suggestions
                # Show submenu with 10 suggestions
                if suggestions:
                    submenu = self.contextMenu.addMenu(_("spellcheck.suggestions"))

                    for suggestion in suggestions[:10]:
                        action = submenu.addAction(suggestion)
                        action.triggered.connect(lambda checked, text=suggestion: self.insertPlainText(text))

        self.contextMenu.exec(event.globalPos())