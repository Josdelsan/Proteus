
from typing import Any
from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtGui import (
    QStandardItemModel,
)
from PyQt6.QtWidgets import (
    QComboBox,
)

class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)

    def addItem(self, item: str, data: Any, state: Qt.CheckState = Qt.CheckState.Unchecked) -> None:
        super().addItem(item, data)
        item = self.model().item(self.count() - 1, 0)
        item.setCheckState(state)