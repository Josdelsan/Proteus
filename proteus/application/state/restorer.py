# ==========================================================================
# File: restorer.py
# Description: State restorer module for PROTEUS application.
# Date: 04/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
# TODO: Refactor to allow access to different views components avoiding
# circular imports. This will be neccesary if the user wants to restore
# the window size, position or other attributes stored in the widgets.
# TODO: Allow the user to select if restore the state or not in Config?

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import yaml
from PyQt6.QtWidgets import QApplication, QTreeWidgetItem

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.application.state import (
    STATE_FILE_NAME,
    STATE_DATA_EXPANDED_OBJECTS,
    STATE_DATA_SELECTED_VIEW,
    STATE_DATA_OPENED_VIEWS,
    STATE_DATA_SELECTED_DOCUMENT,
    STATE_DATA_SELECTED_OBJECTS,
)
from proteus.controller.command_stack import Controller
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.views_container import ViewsContainer
from proteus.application.state.manager import StateManager

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Function: read_state_from_file
# Description: Reads the state manager from a file.
# Date: 02/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def read_state_from_file(controller: Controller) -> None:
    """
    Reads the app state stored in a yaml file. It restores the state of the
    state manager and the document tree objects (expanded attribute).

    Validation is performed to ensure that the data is correct (state manager).
    If objects and document data is not valid, it is ignored. If view data is
    not valid, the default view is set. Tree data is validated for each object
    and if it is not valid, it is set to False. Opened views that are not
    available in the application are ignored.

    :param controller: Controller instance
    """
    state_manager = StateManager()
    path = state_manager.current_project_path

    log.debug(f"Reading app state from file '{path}/{STATE_FILE_NAME}'")

    # -----------------------------
    # File reading
    # -----------------------------
    # Build the file path
    file_path = path / STATE_FILE_NAME

    # If the file does not exist, ignore it
    if not file_path.exists():
        log.warning(
            f"Could not find state file in '{file_path}', app state will not be restored."
        )
        return

    # Read the state dictionary from the file
    with open(file_path, "r") as file:
        state_dict = yaml.load(file, Loader=yaml.FullLoader)

    # -----------------------------
    # Data validation
    # -----------------------------

    # Correct data flags
    # NOTE: Validation is performed separately because view might not be present
    # in the proteus instalation if project is shared.
    objects_valid = True
    view_valid = True

    # Project Ids validation (current document and selected objects)
    try:
        selected_objects: dict = state_dict[STATE_DATA_SELECTED_OBJECTS]
        current_document: ProteusID = ProteusID(
            state_dict[STATE_DATA_SELECTED_DOCUMENT]
        )

        controller.get_element(current_document)
        for _, object_id in selected_objects.items():
            if object_id is not None:
                controller.get_element(object_id)
    except Exception as error:
        log.error(f"Error restoring app state from file {file_path}: {error}")
        objects_valid = False

    # Current view validation
    try:
        current_view: str = state_dict[STATE_DATA_SELECTED_VIEW]

        project_views = controller.get_available_xslt()
        assert (
            current_view in project_views
        ), f"View '{current_view}' not found in proteus available views {project_views}"
    except Exception as error:
        log.error(f"Error restoring app state from file {file_path}: {error}")
        view_valid = False

    # -----------------------------
    # Data restoration
    # -----------------------------

    # Restore objects and document if valid
    if objects_valid:
        for document_id, object_id in selected_objects.items():
            if object_id is not None and document_id is not None:
                state_manager.current_object[document_id] = None
                state_manager.set_current_object(object_id, document_id, False)

        state_manager.set_current_document(current_document)

    # Restore view if valid
    if view_valid:
        state_manager.set_current_view(current_view)

    # -----------------------------
    # Document tree restoration
    # -----------------------------
    # NOTE: The only validation performed is checking if the object is present in
    # the state file. If it is not, just ignore it. This data is not critical for
    # the app to work properly.
    # Document tree data
    expanded_objects_config: Dict[ProteusID, bool] = state_dict[
        STATE_DATA_EXPANDED_OBJECTS
    ]
    try:
        document_tree_list: List[DocumentTree] = [
            w for w in QApplication.allWidgets() if isinstance(w, DocumentTree)
        ]

        for document_tree in document_tree_list:
            object_id: ProteusID
            tree_widget: QTreeWidgetItem
            for object_id, tree_widget in document_tree.tree_items.items():
                # If the object config is present in the state file, restore it
                if object_id in expanded_objects_config:
                    object_config = expanded_objects_config[object_id]

                    expanded_objects_config[object_id] = tree_widget.setExpanded(
                        object_config
                    )

    except Exception as error:
        log.error(f"Error restoring app state from file {file_path}. Error {error}")

    # -----------------------------
    # Opened views restoration
    # -----------------------------

    # Opened views data
    try:
        opened_views: List[str] = list(state_dict[STATE_DATA_OPENED_VIEWS])

        # Remove views that are not available in the project
        opened_views = [v for v in opened_views if v in project_views]

        views_container_list: List[ViewsContainer] = [
            w for w in QApplication.allWidgets() if isinstance(w, ViewsContainer)
        ]

        # Only one views container is expected
        if len(views_container_list) > 1:
            log.error(
                f"More than one views container found in the application. "
                f"Only one is expected. Found: {len(views_container_list)}"
            )

        views_container: ViewsContainer = views_container_list[0]

        # This is also validated in the ViewsContainer class before each view is added
        for view in opened_views:
            views_container.add_view(view)

        assert (
            set(views_container.tabs.keys())
            == set(opened_views)
            == set(state_manager.opened_views)
        ), f"Opened views do not match the views in the views container. Opened views: '{opened_views}', views container: '{views_container.tabs.keys()}'."

    except Exception as error:
        log.error(f"Error restoring app state from file {file_path}. Error {error}")
