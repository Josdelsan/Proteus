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
    QKeyEvent,
    QContextMenuEvent,
    QTextCursor,
    QTextCharFormat,
    QColor,
)
from PyQt6.QtCore import (
    QEvent,
    Qt,
    QStringListModel,
    QTimer,
)
from PyQt6.QtWidgets import (
    QTextEdit,
    QWidget,
    QMenu,
    QCompleter,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.spellcheck import SpellCheckHighlighter, SpellCheckerWrapper
from proteus.application.resources.translator import translate as _
from proteus.application.resources.plugins import Plugins
from proteus.application.utils.autocompleter import AutocompleterInterface

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

        # Autocompletion handling ----------------------------        
        self.completer = QCompleter(self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self._insert_completion)


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


    def _insert_completion(self, completion):
        if self.completer.widget() is not self:
            return
        
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Left)
        tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def _text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        return tc.selectedText()
    
    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        super().focusInEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if self.completer and self.completer.popup().isVisible():
            # Don't handle keypresses while popup is visible
            if event.key() in (
                Qt.Key.Key_Enter,
                Qt.Key.Key_Return,
                Qt.Key.Key_Escape,
                Qt.Key.Key_Tab,
                Qt.Key.Key_Backtab
            ):
                event.ignore()
                return

        # Handle standard Tab key press
        isShortcut = (event.modifiers() == Qt.KeyboardModifier.ControlModifier and
                     event.key() == Qt.Key.Key_Space)
        
        if not self.completer or not isShortcut:
            super().keyPressEvent(event)
        
        ctrlOrShift = event.modifiers() in (Qt.KeyboardModifier.ControlModifier,
                                          Qt.KeyboardModifier.ShiftModifier)
        if ctrlOrShift and event.text() == '':
            return
        
        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        hasModifier = (event.modifiers() != Qt.KeyboardModifier.NoModifier) and not ctrlOrShift
        completionPrefix = self._text_under_cursor()

        copilot: AutocompleterInterface = Plugins().get_autocompleters().get('copilot')
        string = copilot.autocomplete(completionPrefix)
        model = QStringListModel()
        model.setStringList(string)
        self.completer.setModel(model)
        
        if not isShortcut and (hasModifier or event.text() == '' or
                              len(completionPrefix) < 1 or
                              event.text()[-1] in eow):
            self.completer.popup().hide()
            return
        
        if completionPrefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completionPrefix)
            self.completer.popup().setCurrentIndex(
                self.completer.completionModel().index(0, 0))
        
        # Only complete if it is at the end of the text (not including spaces)
        cursor = self.textCursor()
        if cursor.position() - cursor.block().position() != cursor.block().length() - 1:
            return
        
        cursor_rect = self.cursorRect()
        cursor_rect.setWidth(self.completer.popup().sizeHintForColumn(0) +
                           self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cursor_rect)


        