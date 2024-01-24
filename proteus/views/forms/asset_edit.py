# ==========================================================================
# File: asset_edit.py
# Description: Asset edit input widget for forms.
# Date: 17/10/2023
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
    QMessageBox,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.utils import ProteusIconType
from proteus.model import ASSETS_REPOSITORY
from proteus.utils.config import Config
from proteus.utils.translator import Translator


# --------------------------------------------------------------------------
# Class: AssetEdit
# Description: Asset edit input widget for forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class AssetEdit(QWidget):
    """
    Asset edit input widget for forms. It copies the selected file into the
    assets directory if it is not already there.

    Similar to PyQt6 QLineEdit, QTextEdit, etc. It is used to retrieve the
    value of the user input.

    NOTE: It is meant to be used standalone or in FilePropertyInput. Do not
    confuse it with FilePropertyInput.
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
        browse_icon_path: Path = Config().get_icon(ProteusIconType.App, "browse_asset_icon")
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
        self.browse_button.clicked.connect(self._open_file_dialog)

    # ----------------------------------------------------------------------
    # Method     : asset
    # Description: Returns the asset.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def asset(self) -> str:
        """
        Returns the asset.
        """
        return self.input.text()

    # ----------------------------------------------------------------------
    # Method     : setAsset
    # Description: Sets the asset.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setAsset(self, asset: str) -> None:
        """
        Sets the asset.
        """
        self.input.setText(asset)

    # ----------------------------------------------------------------------
    # Method     : setEnabled
    # Description: Sets the enabled state of the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setEnabled(self, enabled: bool) -> None:
        """
        Sets the input to enabled or disabled state modifying the browse
        button.
        """
        self.browse_button.setEnabled(enabled)

    # ======================================================================
    # Slots (connected to signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : open_file_dialog
    # Description: Opens a file dialog.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _open_file_dialog(self) -> None:
        """
        Opens a file dialog and sets the selected file as the input value.
        Copies the file to the assets directory if it is not already there.
        """
        # Assets directory
        assets_path = f"{Config().current_project_path}/{ASSETS_REPOSITORY}"

        file_dialog = QFileDialog()

        # TODO: Translate using the translator
        # Get the name of the selected file
        selected_file = file_dialog.getOpenFileName(
            self,
            caption="Select image",
            directory=assets_path,
            filter="Images (*.png *.jpeg *.jpg *.gif *.svg *.bmp *.ico *.tiff *.tif)",
        )

        if selected_file[0] != "":
            selected_file = selected_file[0]

            # Build file path
            file_path: Path = Path(selected_file)

            # NOTE: We copy the file to the project directory
            # so we can perform undo/redo operations. If we don't
            # copy it now, we cannot access the file when properties
            # are updated. Every file that is not used by any property
            # must be deleted when the project closes.

            # Avoid copying the file if it was selected from the assets directory
            # It triggers an error when the file is copied to the same directory
            if file_path.parent.as_posix() != assets_path:
                # Before copying the file, check if it already exists
                # a file with the same name in the assets directory
                if Path(f"{assets_path}/{file_path.name}").exists():
                    # Ask the user if he wants to overwrite the file
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setWindowTitle(
                        Translator().text("asset_edit.warning.title")
                    )
                    msg_box.setText(Translator().text("asset_edit.warning.text"))
                    msg_box.setStandardButtons(
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    msg_box.setDefaultButton(QMessageBox.StandardButton.No)
                    msg_box.exec()

                    if msg_box.result() == QMessageBox.StandardButton.No:
                        return
                else:
                    shutil.copy(file_path, assets_path)

            # Get file name
            # NOTE: It will be stored in the property value and
            # used to create the path to the file relative to
            # the project directory
            file_name = file_path.name
            self.input.setText(file_name)
