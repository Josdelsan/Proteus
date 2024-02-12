# ==========================================================================
# File: check_combo_box.py
# Description: ComboBox with checkable items input widget for forms.
# Date: 06/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Any

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QFontMetrics

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Class: CheckComboBox
# Description: ComboBox with checkable items input widget for forms.
# Date: 06/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
# TODO: Some methods from QStandardItemModel are not documented in 
# https://www.riverbankcomputing.com/static/Docs/PyQt6/ but they are working.
# They have the same behavior as in PySide6 and multiple examples from PyQt
# use them. Find the reason why they are not documented (deprecated, linting
# issue, etc.) and find an alternative if necessary.
# Methods: appendRow, item, itemFromIndex
class CheckComboBox(QComboBox):
    """
    ComboBox with checkable items input widget for forms. It is composed by a
    QComboBox and a QStandardItemModel that allows to select multiple items
    from a list.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 06/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent=None):
        """
        Class constructor. Set the model and connect the pressed event to the
        handleItemPressed method.
        """
        super(CheckComboBox, self).__init__(parent)

        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

    # ----------------------------------------------------------------------
    # Method     : handleItemPressed
    # Description: Handle the item pressed event to change the check state of
    #              the item.
    # Date       : 06/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def handleItemPressed(self, index: QModelIndex) -> None:
        """
        Handle the item pressed event to change the check state of the item.

        :param index: QModelIndex
        """
        item: QStandardItem = self.model().itemFromIndex(index)
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)

    # ----------------------------------------------------------------------
    # Method     : addItem
    # Description: Add an item to the ComboBox with the specified text, userData,
    #              checked state and icon.
    # Date       : 06/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def addItem(
        self, text, userData: Any = None, checked: bool = False, icon: QIcon = None
    ) -> None:
        """
        Add an item to the ComboBox with the specified text, userData, checked
        state and icon.

        :param text: Text to display in the item
        :param userData: Data stored in the item
        :param checked: Initial check state
        :param icon: Icon to display in the item
        """
        item = QStandardItem(text)
        if userData is not None:
            item.setData(userData, Qt.ItemDataRole.UserRole)

        if icon is not None:
            item.setIcon(icon)

        # Check handling
        item.setCheckable(True)
        item.setCheckState(
            Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        )

        # Calculate width based on the text length
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.averageCharWidth() * int(len(text) * 1.5)
        icon_width = 0 if icon is None else icon.actualSize(self.sizeHint()).width()
        width = text_width + icon_width + 20 # 20 is the width of the checkbox
        if width > self.view().minimumWidth():
            self.view().setMinimumWidth(width)

        # Include item
        self.model().appendRow(item)

    # ----------------------------------------------------------------------
    # Method     : checkedItems
    # Description: Return the list of checked items.
    # Date       : 06/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def checkedItems(self) -> List[str]:
        """
        Return the list of checked items.
        """
        items: List[str] = list()
        index: QModelIndex
        for index in range(self.model().rowCount()):
            item: QStandardItem = self.model().item(index)
            if item.checkState() == Qt.CheckState.Checked:
                items.append(item.text())
        return items

    def checkedItemsData(self) -> List[Any]:
        """
        Return the list of checked items data.
        """
        items: List[Any] = list()
        index: QModelIndex
        for index in range(self.model().rowCount()):
            item: QStandardItem = self.model().item(index)
            if item.checkState() == Qt.CheckState.Checked:
                items.append(item.data(Qt.ItemDataRole.UserRole))
        return items
