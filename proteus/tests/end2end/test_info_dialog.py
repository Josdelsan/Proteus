# ==========================================================================
# File: test_info_dialog.py
# Description: pytest file for the PROTEUS pyqt info fialog
# Date: 29/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/37
# QApplication instace cannot be deleted. This might cause tests failures.

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/256
# Dialog handling can interfere with running tests together. Workaround
# listed in the issue with 5ms delay in QTimer seems to work. Since
# dialogs are an important part of the app, this might be a problem
# in the future. No complete solution found yet.

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.information_dialog import InformationDialog
from proteus.tests.end2end.fixtures import app


# --------------------------------------------------------------------------
# End to end "info dialog" tests
# --------------------------------------------------------------------------


def test_info_dialog(app):
    """
    Simple test that checks if the info dialog is shown when the user
    clicks on the info button.
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    # Get info button
    info_button = main_window.main_menu.information_button

    # --------------------------------------------
    # Act
    # --------------------------------------------

    dialog: InformationDialog = None

    def handle_dialog():
        nonlocal dialog
        dialog = QApplication.activeModalWidget()
        while dialog is None:
            dialog = QApplication.activeModalWidget()

        dialog.close()

    # Open info dialog
    QTimer.singleShot(5, handle_dialog)  # Wait for the dialog to be created
    info_button.click()

    # --------------------------------------------
    # Assert
    # --------------------------------------------
    assert isinstance(
        dialog, InformationDialog
    ), f"Information dialog must be instance of InformationDialog but it is {type(dialog)}"
