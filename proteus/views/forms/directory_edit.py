# ==========================================================================
# File: directory_edit.py
# Description: Directory edit input widget for forms.
# Date: 18/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

import shutil
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QFileDialog,
    QPushButton,
    QHBoxLayout,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils import ProteusIconType
from proteus.utils.config import Config


# --------------------------------------------------------------------------
# Class: DirectoryEdit
# Description: Directory edit input widget for forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DirectoryEdit(QWidget):
    """
    Directory edit input widget for forms. It allows the user to select a
    directory from the file system.

    Similar to PyQt6 QLineEdit, QTextEdit, etc. It is used to retrieve the
    value of the user input.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Object initialization.
        """
        super().__init__(*args, **kwargs)

        # Initialize widgets
        self.input: QLineEdit = None
        self.browse_button: QPushButton = None

        # Create input widget
        self.create_input()


    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_input(self) -> None:
        """
        Create the widgets and configure the layout.
        """

        # Widgets creation --------------------------------------------------
        # Line edit
        self.input = QLineEdit()
        self.input.setDisabled(True)
        
        # Browse button
        browse_icon_path: Path = Config().get_icon(ProteusIconType.App, "browse_dir_icon")
        browse_button_icon = QIcon()
        browse_button_icon.addFile(browse_icon_path.as_posix())

        self.browse_button = QPushButton()
        self.browse_button.setIcon(browse_button_icon)

        # Layout setup -----------------------------------------------------
        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.browse_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Connect signals --------------------------------------------------
        self.browse_button.clicked.connect(self._browse_directory_dialog)

    # ----------------------------------------------------------------------
    # Method     : directory
    # Description: Returns the directory.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def directory(self) -> str:
        """
        Returns the selected directory.
        """
        return self.input.text()
    
    # ----------------------------------------------------------------------
    # Method     : setDirectory
    # Description: Sets the directory.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setDirectory(self, directory: str) -> None:
        """
        Sets the directory.
        """
        self.input.setText(directory)

    
    # ======================================================================
    # Slots (connected to signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : _browse_directory_dialog
    # Description: Browse directory dialog.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _browse_directory_dialog(self) -> None:
            """
            Browse directory dialog.
            """
            file_dialog: QFileDialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.Directory)
            path: str = file_dialog.getExistingDirectory()
            self.input.setText(path)