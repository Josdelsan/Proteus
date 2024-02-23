# ==========================================================================
# File: test_delete_document.py
# Description: pytest file for the PROTEUS pyqt delete document use case
# Date: 16/08/2023
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

from proteus.views.components.dialogs.delete_dialog import DeleteDialog
from proteus.views.components.main_window import MainWindow
from proteus.tests.end2end.fixtures import app, load_project, get_dialog

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

PROJECT_NAME = "one_doc_project"

# --------------------------------------------------------------------------
# End to end "delete document" tests
# --------------------------------------------------------------------------


def test_delete_document(app):
    """
    Test the delete document use case. Delete the only document in an
    project. It tests the following steps:
        - Open the confirmation dialog
        - Handle the dialog
        - Check the document is deleted
        - Check buttons state changed
    """
    # --------------------------------------------
    # Arrange
    # --------------------------------------------
    main_window: MainWindow = app

    load_project(main_window=main_window, project_name=PROJECT_NAME)

    # Buttons that should change state when document is created in an empty project
    save_button_state = main_window.main_menu.save_button.isEnabled()
    delete_doc_button_state = main_window.main_menu.delete_document_button.isEnabled()
    export_doc_button_state = main_window.main_menu.export_document_button.isEnabled()
    undo_button_state = main_window.main_menu.undo_button.isEnabled()

    # --------------------------------------------
    # Act
    # --------------------------------------------

    # Dialog handling and delete button click
    delete_document_button = main_window.main_menu.delete_document_button
    dialog: DeleteDialog = get_dialog(delete_document_button.click)
    dialog.accept_button.clicked.emit()

    # --------------------------------------------
    # Assert
    # --------------------------------------------

    # Check buttons state changed
    assert save_button_state != main_window.main_menu.save_button.isEnabled(), (
        "Save button state should change from DISABLED to ENABLED when a document is created in an empty project"
        f"Current state: {main_window.main_menu.save_button.isEnabled()}"
    )
    assert (
        delete_doc_button_state
        != main_window.main_menu.delete_document_button.isEnabled()
    ), (
        "Delete document button state should change from ENABLED to DISABLED when a document is deleted and there are no more documents in the project"
        f"Current state: {main_window.main_menu.delete_document_button.isEnabled()}"
    )
    assert (
        export_doc_button_state
        != main_window.main_menu.export_document_button.isEnabled()
    ), (
        "Export document button state should change from ENABLED to DISABLED when a document is deleted and there are no more documents in the project"
        f"Current state: {main_window.main_menu.export_document_button.isEnabled()}"
    )
    assert (
        undo_button_state != main_window.main_menu.undo_button.isEnabled()
    ), (
        "Undo button state should change from DISABLED to ENABLED when a document is deleted in a project"
        f"Current state: {main_window.main_menu.undo_button.isEnabled()}"
    )

     # Check documents container does not include the document
    documents_container = main_window.project_container.documents_container
    assert (
        documents_container.tabs.keys().__len__() == 0
    ), f"Documents container should not include any document tab, number of tabs: '{documents_container.tabs.keys().__len__()}'"

    # Check that the tab was deleted from the tabbar
    tab_bar = documents_container.tabBar()
    assert (
        tab_bar.count() == 0
    ), f"Documents container tab bar should not include any tab, number of tabs: '{tab_bar.count()}'"

