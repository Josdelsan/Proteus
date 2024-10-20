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

from proteus.model import ASSETS_REPOSITORY
from proteus.application.state.manager import StateManager
from proteus.application.resources.translator import translate as _
from proteus.application.resources.icons import Icons, ProteusIconType


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

        # Delete button
        delete_button_icon: Path = Icons().icon(
            ProteusIconType.App, "delete_file_input_icon"
        )
        self.delete_button = QPushButton()
        self.delete_button.setIcon(delete_button_icon)

        # Browse button
        browse_button_icon: Path = Icons().icon(
            ProteusIconType.App, "browse_asset_icon"
        )
        self.browse_button = QPushButton()
        self.browse_button.setIcon(browse_button_icon)

        # Layout setup -----------------------------------------------------
        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.browse_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Connect signals --------------------------------------------------
        self.browse_button.clicked.connect(self._open_file_dialog)
        self.delete_button.clicked.connect(self.delete_input_button_clicked)

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
        # Copy file path variable
        asset_file_path = None

        # Assets directory
        assets_path = StateManager().current_project_path / ASSETS_REPOSITORY

        # Check if the assets directory exists
        if not assets_path.exists():
            assets_path.mkdir()

        file_dialog = QFileDialog()

        # Get the name of the selected file
        selected_file = file_dialog.getOpenFileName(
            self,
            caption=_('asset_edit.file_dialog.title'),
            directory=(assets_path / self.input.text()).as_posix(),
            filter=f"{_('asset_edit.file_dialog.filter')} (*.png *.jpeg *.jpg *.gif *.svg *.bmp *.ico *.tiff *.tif)",
        )

        if selected_file[0] != "":
            selected_file = selected_file[0]

            # Build file path
            file_path: Path = Path(selected_file)
            asset_file_path = file_path

            # NOTE: We copy the file to the project directory
            # so we can perform undo/redo operations. If we don't
            # copy it now, we cannot access the file when properties
            # are updated. Every file that is not used by any property
            # must be deleted when the project closes.

            # Avoid copying the file if it was selected from the assets directory
            # It triggers an error when the file is copied to the same directory
            if file_path.parent != assets_path:
                # Before copying the file, check if it already exists
                # a file with the same name in the assets directory
                if (assets_path / file_path.name).exists():
                    
                    # Add a number to the file name
                    file_name = file_path.stem
                    file_extension = file_path.suffix
                    number = 1
                    while (assets_path / f"{file_name} ({number}){file_extension}").exists():
                        number += 1

                    # Copy the file
                    asset_file_path = shutil.copy2(file_path, assets_path / f"{file_name} ({number}){file_extension}")

                else:
                    asset_file_path = shutil.copy2(file_path, assets_path)

            # Get file name
            # NOTE: It will be stored in the property value and
            # used to create the path to the file relative to
            # the project directory
            file_name = Path(asset_file_path).name
            self.input.setText(file_name)
       
    # ----------------------------------------------------------------------
    # Method     : delete_input_button_clicked
    # Description: Deletes the input text.
    # Date       : 10/09/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_input_button_clicked(self) -> None:
        """
        Deletes the input text.
        """
        self.input.clear()