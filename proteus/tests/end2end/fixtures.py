# ==========================================================================
# File: fixtures.py
# Description: pytest fixtures for end2end testing PROTEUS
# Date: 12/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# NOTE: https://github.com/pytest-dev/pytest-qt/issues/37
# QApplication instace cannot be deleted. This causes subsequent tests
# to fail. It also occurs with the main window instance. Due to the
# nature of the end2end tests, they will be executed manually.

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
from PyQt6.QtWidgets import QApplication

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.views.main_window import MainWindow

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture(scope="function")
def app(qtbot, mocker):
    """
    Handle the creation of the QApplication instance and the main window.
    """
    # Create the QApplication instance and the main window
    test_app = QApplication([])
    main_window = MainWindow(parent=None)
    main_window.show()
    qtbot.addWidget(main_window)

    # Call the mock_views_container function to mock the ViewsContainer methods
    mock_views_container(mocker)

    # Return the main window
    yield test_app

    # Teardown
    test_app.quit()
    test_app.deleteLater()



def mock_views_container(mocker):
    """
    Mocks ViewsContainer methods to avoid the creation of the QWebEngineView
    and QWebEnginePage instances. This is necessary because the QWebEngineView
    class is not supported by the pytest-qt plugin.
    """

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.create_component", 
        lambda *args, **kwargs: None
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_component",
        lambda *args, **kwargs: None
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.delete_component",
        lambda *args, **kwargs: None
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_on_add_view",
        lambda *args, **kwargs: None
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_on_select_object",
        lambda *args, **kwargs: None
    )

    mocker.patch(
        "proteus.views.components.views_container.ViewsContainer.update_on_delete_view",
        lambda *args, **kwargs: None
    )