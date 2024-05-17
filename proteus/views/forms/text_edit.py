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

from typing import List

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
    QMenu,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.spellcheck import SpellCheckHighlighter, SpellCheckerWrapper
from proteus.application.resources.translator import translate as _



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

        SpellChecking will only be shown if no text is selected and the user
        right-clicks on a word that is suspected to be misspelled.
        """
        self.contextMenu = self.createStandardContextMenu()

        textCursor = self.textCursor()

        # If there is no selection, select the word under the cursor to check
        if not textCursor.hasSelection():

            # WordUnderCursor will select underscores as part of the word
            # this might be a problem for some markdown syntax
            textCursor.select(QTextCursor.SelectionType.WordUnderCursor)
            self.setTextCursor(textCursor)
            word = textCursor.selectedText()

            if self._spellchecker.check(word) is False and len(word) > 1:
                self.contextMenu.addSeparator()

                suggestions: List[str] = self._spellchecker.suggest(word)

                # TODO: Handle misspelled words that have no suggestions
                if suggestions:
                    submenu: QMenu = None

                    # Show up to 3 suggestions in the context menu
                    for i, suggestion in enumerate(suggestions):
                        if i < 3:
                            action = self.contextMenu.addAction(suggestion)
                            action.triggered.connect(
                                lambda checked, text=suggestion: self.insertPlainText(
                                    text
                                )
                            )
                        # If there are more than 3 suggestions, show them in a submenu
                        else:
                            if submenu is None:
                                submenu = self.contextMenu.addMenu(
                                    _("spellcheck.more_suggestions")
                                )

                            action = submenu.addAction(suggestion)
                            action.triggered.connect(
                                lambda checked, text=suggestion: self.insertPlainText(
                                    text
                                )
                            )

        self.contextMenu.exec(event.globalPos())
