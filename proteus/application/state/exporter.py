# ==========================================================================
# File: exporter.py
# Description: State exporter module for PROTEUS application.
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
from proteus.views.components.document_tree import DocumentTree
from proteus.views.components.views_container import ViewsContainer
from proteus.application.state.manager import StateManager


# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Function: write_state_to_file
# Description: Writes the current state manager to a file.
# Date: 02/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def write_state_to_file() -> None:
    """
    Writes the current app state to a yaml file. It stores the state manager
    variables and the document tree objects (expanded attribute).
    """
    state_manager = StateManager()
    path = state_manager.current_project_path

    log.debug(f"Writing app state to file '{path}/{STATE_FILE_NAME}'")

    # -----------------------------
    # File path building
    # -----------------------------
    # Check if the path exists
    assert (
        path.exists()
    ), f"Path '{path}' does not exist. The state file cannot be written."

    # Build the file path
    file_path = path / STATE_FILE_NAME

    # -----------------------------
    # Data collection
    # -----------------------------
    # State manager data
    current_view = state_manager.current_view
    current_document = state_manager.current_document
    selected_objects = state_manager.current_object

    # Document tree data
    expanded_objects_config: Dict[ProteusID, bool] = {}
    try:
        document_tree_list: List[DocumentTree] = [
            w for w in QApplication.allWidgets() if isinstance(w, DocumentTree)
        ]

        for document_tree in document_tree_list:
            object_id: ProteusID
            tree_widget: QTreeWidgetItem
            for object_id, tree_widget in document_tree.tree_items.items():
                expanded_objects_config[object_id] = tree_widget.isExpanded()
    except Exception as error:
        log.error(f"Error writing app state to file {file_path}. Error: {error}")

    # Opened views data
    opened_views: List[str] = []
    try:
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
        opened_views.extend(views_container.tabs.keys())

    except Exception as error:
        log.error(f"Error writing app state to file {file_path}. Error: {error}")

    # -----------------------------
    # Data writing
    # -----------------------------

    # Build the state dictionary
    state_dict = {
        STATE_DATA_EXPANDED_OBJECTS: expanded_objects_config,
        STATE_DATA_SELECTED_OBJECTS: selected_objects,
        STATE_DATA_SELECTED_DOCUMENT: current_document,
        STATE_DATA_SELECTED_VIEW: current_view,
        STATE_DATA_OPENED_VIEWS: opened_views,
    }

    log.debug(f"Selected objects: {selected_objects}")
    log.debug(f"Selected document: '{current_document}'")
    log.debug(f"Selected view: '{current_view}'")
    log.debug(f"Opened views: {opened_views}")
    log.debug(f"Stored expanded info for {len(expanded_objects_config)} objects")

    # Write the state dictionary to the file
    with open(file_path, "w") as file:
        yaml.dump(state_dict, file, default_flow_style=False)
