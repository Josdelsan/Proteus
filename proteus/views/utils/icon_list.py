import sys

from PyQt6.QtWidgets import (QApplication, QGridLayout, QPushButton, QStyle,
                             QWidget)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        icons = sorted([attr for attr in dir(QStyle.StandardPixmap) if attr.startswith("SP_")])
        layout = QGridLayout()

        for n, name in enumerate(icons):
            btn = QPushButton(name)

            pixmapi = getattr(QStyle.StandardPixmap, name)
            icon = self.style().standardIcon(pixmapi)
            btn.setIcon(icon)
            layout.addWidget(btn, int(n/4), int(n%4))

        self.setLayout(layout)


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()