# ==========================================================================
# File: state_manager.py
# Description: State restorer module for PROTEUS application.
# Date: 02/01/2023
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

from pathlib import Path
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
from proteus.controller.command_stack import Controller
from proteus.views.components.document_tree import DocumentTree
from proteus.utils.state_manager import StateManager

# logging configuration
log = logging.getLogger(__name__)

STATE_FILE_NAME = "state.yaml"


# --------------------------------------------------------------------------
# Function: write_state_to_file
# Description: Writes the current state manager to a file.
# Date: 02/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def write_state_to_file(path: Path, state_manager: StateManager) -> None:
    """
    Writes the current app state to a yaml file. It stores the state manager
    variables and the document tree objects (expanded attribute).

    :param file_path: Path where the file will be written
    :param state_manager: State manager instance
    """
    log.debug(f"Writing app state to file {path}/{STATE_FILE_NAME}")

    # -----------------------------
    # File path building
    # -----------------------------
    # Check if the path exists
    assert (
        path.exists()
    ), f"Path {path} does not exist. The state file cannot be written."

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

    # -----------------------------
    # Data writing
    # -----------------------------

    # Build the state dictionary
    state_dict = {
        "expanded_objects": expanded_objects_config,
        "selected_objects": selected_objects,
        "selected_document": current_document,
        "selected_view": current_view,
    }

    # Write the state dictionary to the file
    with open(file_path, "w") as file:
        yaml.dump(state_dict, file, default_flow_style=False)


# --------------------------------------------------------------------------
# Function: read_state_from_file
# Description: Reads the state manager from a file.
# Date: 02/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def read_state_from_file(
    path: Path, controller: Controller, state_manager: StateManager
) -> None:
    """
    Reads the app state stored in a yaml file. It restores the state of the
    state manager and the document tree objects (expanded attribute).

    Validation is performed to ensure that the data is correct (state manager).
    If objects and document data is not valid, it is ignored. If view data is
    not valid, the default view is set. Tree data is validated for each object
    and if it is not valid, it is set to False.

    :param file_path: Path where the file will be read
    :param controller: Controller instance
    :param state_manager: State manager instance
    """
    log.debug(f"Reading app state from file {path}/{STATE_FILE_NAME}")

    # -----------------------------
    # File reading
    # -----------------------------
    # Build the file path
    file_path = path / STATE_FILE_NAME

    # If the file does not exist, ignore it
    if not file_path.exists():
        log.warning(
            f"Could not find state file in {file_path}, app state will not be restored."
        )
        return

    # Read the state dictionary from the file
    with open(file_path, "r") as file:
        state_dict = yaml.load(file, Loader=yaml.FullLoader)

    # -----------------------------
    # Data validation
    # -----------------------------
    # Variables
    current_document: ProteusID = ProteusID(state_dict["selected_document"])
    current_view: str = state_dict["selected_view"]
    selected_objects: dict = state_dict["selected_objects"]

    # Correct data flags
    # NOTE: Validation is performed separately because view might not be present
    # in the proteus instalation if project is shared.
    objects_valid = True
    view_valid = True

    # Project Ids validation (current document and selected objects)
    try:
        controller.get_element(current_document)
        for _, object_id in selected_objects.items():
            if object_id is not None:
                controller.get_element(object_id)
    except AssertionError as error:
        log.error(f"Error restoring app state from file {file_path}: {error}")
        objects_valid = False

    # Current view validation
    try:
        available_views = controller.get_available_xslt()
        assert (
            current_view in available_views
        ), f"View '{current_view}' not found in proteus available views {available_views}"
    except AssertionError as error:
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
    expanded_objects_config: Dict[ProteusID, bool] = state_dict["expanded_objects"]
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
