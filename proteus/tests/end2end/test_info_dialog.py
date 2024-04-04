# ==========================================================================
# File: test_info_dialog.py
# Description: pytest file for the PROTEUS pyqt info dialog
# Date: 29/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================


# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.components.main_window import MainWindow
from proteus.views.components.dialogs.information_dialog import InformationDialog
from proteus.tests.end2end.fixtures import app, get_dialog


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

    dialog: InformationDialog = get_dialog(info_button.click)

    # --------------------------------------------
    # Assert
    # --------------------------------------------
    assert isinstance(
        dialog, InformationDialog
    ), f"Information dialog must be instance of InformationDialog but it is {type(dialog)}"
