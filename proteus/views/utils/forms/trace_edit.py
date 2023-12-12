# ==========================================================================
# File: trace_edit.py
# Description: Trace edit input widget for forms.
# Date: 25/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from pathlib import Path
from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QSizePolicy,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, ProteusClassTag, PROTEUS_NAME, PROTEUS_CODE
from proteus.model.object import Object
from proteus.model.properties.property import Property
from proteus.model.properties.code_property import ProteusCode
from proteus.controller.command_stack import Controller
from proteus.views import APP_ICON_TYPE
from proteus.views import TREE_MENU_ICON_TYPE
from proteus.config import Config
from proteus.views.utils.translator import Translator

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: TraceEdit
# Description: Trace edit input widget for forms.
# Date: 25/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class TraceEdit(QWidget):
    """
    Trace edit input widget for forms.

    It needs a controller instance in order to show user traced object data
    and list of available objects to trace.

    Similar to PyQt6 QLineEdit, QTextEdit, etc. It is used to retrieve the
    traces from the user.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        controller: Controller = None,
        accepted_targets: List[ProteusClassTag] = [],
        *args,
        **kwargs,
    ):
        """
        Object initialization.
        """
        super().__init__(*args, **kwargs)

        # Validate controller
        assert isinstance(
            controller, Controller
        ), f"TraceEdit requires a Controller instance to be initialized. Controller argument is type {type(controller)}"

        # Arguments initialization
        self.controller: Controller = controller
        self.accepted_targets: List[ProteusClassTag] = accepted_targets

        # Initialize widgets
        self.list_widget: QListWidget = None
        self.add_button: QPushButton = None
        self.remove_button: QPushButton = None

        # Create input widget
        self.create_input()

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_input(self) -> None:
        """
        Create the widgets and configure the layout.
        """

        # Widgets creation --------------------------------------------------
        # Create a QListWidget
        self.list_widget = QListWidget(self)
        self.list_widget.setMovement(QListWidget.Movement.Static)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        # Reimplement sizeHint to set a minimun height of 80px
        # NOTE: Recomended in https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qwidget.html
        self.list_widget.sizeHint = lambda: QSize(0, 80)

        # Create QPushButtons
        self.add_button = QPushButton()
        add_icon_path: Path = Config().get_icon(APP_ICON_TYPE, "add_trace_icon")
        add_button_icon = QIcon()
        add_button_icon.addFile(add_icon_path.as_posix())
        self.add_button.setIcon(add_button_icon)

        self.remove_button = QPushButton()
        self.remove_button.setEnabled(False)
        remove_icon_path: Path = Config().get_icon(APP_ICON_TYPE, "remove_trace_icon")
        remove_button_icon = QIcon()
        remove_button_icon.addFile(remove_icon_path.as_posix())
        self.remove_button.setIcon(remove_button_icon)

        # Create a layout for the buttons (vertically stacked)
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a layout for the QListWidget and button layout (horizontally arranged)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(button_layout)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(main_layout)

        # Connect signals ---------------------------------------------------
        self.add_button.clicked.connect(self.add_trace)
        self.remove_button.clicked.connect(self.remove_trace)
        self.list_widget.currentItemChanged.connect(self.update_remove_button)

    # ----------------------------------------------------------------------
    # Method     : traces
    # Description: Returns the asset.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def traces(self) -> List[ProteusID]:
        """
        Returns the traces.
        """
        # Iterate over the QListWidget items and get the traces (ids)
        traces: List[ProteusID] = list()
        for i in range(self.list_widget.count()):
            trace_item: QListWidgetItem = self.list_widget.item(i)
            traces.append(trace_item.data(Qt.ItemDataRole.UserRole))

        return traces

    # ----------------------------------------------------------------------
    # Method     : setTraces
    # Description: Sets the asset.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def setTraces(self, traces: List[ProteusID]) -> None:
        """
        Sets the traces.
        """
        trace: ProteusID
        for trace in traces:
            # Get object from the id
            object: Object = self.controller.get_element(element_id=trace)

            # Validate object type
            assert isinstance(
                object, Object
            ), f"Trace must be a reference to an object, id '{trace}' is not a reference to an object but to a '{type(object)}' type."

            # Create QListWidgetItem
            trace_item: QListWidgetItem = QListWidgetItem(parent=self.list_widget)
            _list_item_setup(trace_item, object)

            self.list_widget.addItem(trace_item)

    # ======================================================================
    # Slots (connected to signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method: add_trace
    # Description: Adds a trace to the list widget.
    # Date: 25/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_trace(self):
        """
        Connected to the add trace button, it triggers the add trace dialog
        and handles the result adding or not the trace to the list widget.
        """
        # Create dialog
        trace: ProteusID = TraceEditDialog.create_dialog(
            controller=self.controller,
            accepted_classes=self.accepted_targets,
            targets=self.traces(),
        )

        # Check if the dialog was accepted
        if trace:
            # Get object from the id
            object: Object = self.controller.get_element(element_id=trace)

            # Validate object type
            assert isinstance(
                object, Object
            ), f"Trace must be a reference to an object, id '{trace}' is not a reference to an object but to a '{type(object)}' type."

            # Create QListWidgetItem
            trace_item: QListWidgetItem = QListWidgetItem(parent=self.list_widget)
            _list_item_setup(trace_item, object)

            # Add item to the QListWidget
            self.list_widget.addItem(trace_item)

    # ----------------------------------------------------------------------
    # Method: remove_trace
    # Description: Removes a trace from the list widget.
    # Date: 25/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def remove_trace(self):
        """
        Connected to the remove trace button, it removes the selected trace
        from the list widget without asking for confirmation.
        """
        # Get the current item
        current_item: QListWidgetItem = self.list_widget.currentItem()

        # Remove the item
        self.list_widget.takeItem(self.list_widget.row(current_item))

    # ----------------------------------------------------------------------
    # Method: update_remove_button
    # Description: Updates the remove button status.
    # Date: 25/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_remove_button(self):
        """
        Connected to the list widget selection changed signal, it updates
        the remove button status.
        """
        if self.list_widget.currentItem():
            self.remove_button.setEnabled(True)
        else:
            self.remove_button.setEnabled(False)


# --------------------------------------------------------------------------
# Class: TraceEditDialog
# Description: Dialog to select a trace.
# Date: 25/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class TraceEditDialog(QDialog):
    """
    Dialog to select a trace from a list of available objects. It shows
    only objects from the given object class. Discard objects that are
    already traced.

    TODO: Hide the object itself from the list of available objects and
    allow the user to select it by clicking on a checkbox.
    TODO: Add a search bar to filter objects by name.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        controller: Controller,
        accepted_classes: List[ProteusClassTag],
        targets: List[ProteusID] = [],
        *args,
        **kwargs,
    ):
        """
        Dialog initialization.
        """
        super().__init__(*args, **kwargs)

        # Validate controller
        assert isinstance(
            controller, Controller
        ), f"TraceEditDialog requires a Controller instance to be initialized. Controller argument is type {type(controller)}"
        self.controller: Controller = controller

        # Validate object class
        assert isinstance(
            accepted_classes, list
        ), f"TraceEditDialog requires a string as object class. Object class argument is type {type(accepted_classes)}"
        self.accepted_classes: List[ProteusClassTag] = accepted_classes

        # Validate targets
        assert isinstance(
            targets, list
        ), f"TraceEditDialog requires a list of ProteusID as targets. Targets argument is type {type(targets)}"
        self.targets: List[ProteusID] = targets

        # Initialize widgets
        self.list_widget: QListWidget = None

        # Initialize variables
        self.selected_object: ProteusID = None

        # Create component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Creates the dialog component.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Creates the dialog component.
        """
        # Set dialog title
        title: str = Translator().text("trace_edit_dialog.title")
        self.setWindowTitle(title)

        # Create a QListWidget
        self.list_widget = QListWidget(self)
        self.list_widget.setMovement(QListWidget.Movement.Static)
        self.list_widget.setMinimumHeight(100)

        # Get list of project objects
        objects: List[Object] = self.controller.get_objects(
            classes=self.accepted_classes
        )

        # Populate the QListWidget
        object: Object
        for object in objects:
            # Skip objects that are already traced
            if object.id in self.targets:
                continue

            # Create QListWidgetItem
            object_item: QListWidgetItem = QListWidgetItem(parent=self.list_widget)
            _list_item_setup(object_item, object)

            # Add item to the QListWidget
            self.list_widget.addItem(object_item)

        # Create accept and reject buttons
        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        # Disable accept button (until an item is selected)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)

        # Create a layout for the QListWidget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.button_box)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(main_layout)

        # Connect signals
        self.list_widget.currentItemChanged.connect(self.enable_accept_button)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    # ----------------------------------------------------------------------
    # Method     : enable_accept_button
    # Description: Enables the accept button.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def enable_accept_button(self) -> None:
        """
        Enables the accept button.
        """
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)

    # ----------------------------------------------------------------------
    # Method     : accept
    # Description: Accepts the dialog.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def accept(self) -> None:
        """
        Accepts the dialog. It sets the selected object id.
        """
        # Get the current item
        current_item: QListWidgetItem = self.list_widget.currentItem()

        # Get the object id
        self.selected_object = current_item.data(Qt.ItemDataRole.UserRole)

        # Accept the dialog
        super().accept()

    # ----------------------------------------------------------------------
    # Method     : reject
    # Description: Rejects the dialog.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def reject(self) -> None:
        """
        Rejects the dialog.
        """
        # Reject the dialog
        super().reject()

    # ----------------------------------------------------------------------
    # Method     : create_dialog
    # Description: Creates and executes the dialog.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(
        controller: Controller,
        accepted_classes: List[ProteusClassTag],
        targets: List[ProteusID] = [],
    ) -> List[ProteusID]:
        """
        Creates and executes the dialog.
        """
        # Create dialog
        dialog = TraceEditDialog(controller, accepted_classes, targets)

        # Execute dialog
        result = dialog.exec()

        # Get traces
        trace: ProteusID = None
        if result == QDialog.DialogCode.Accepted:
            trace = dialog.selected_object

        return trace


# --------------------------------------------------------------------------
# Function: _list_item_setup
# Description: Setup the list item with the information of the object.
# Date: 01/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def _list_item_setup(list_item: QListWidgetItem, object: Object) -> None:
    """
    Helper function to setup the list item with the information of the object.

    :param list_item: QListWidgetItem to setup.
    :param object: Object to get the information from.
    """
    # Create item string from object properties
    name_str = ""
    code_str = ""

    # Check for PROTEUS_CODE property
    if object.get_property(PROTEUS_CODE) is not None:
        code: ProteusCode = object.get_property(PROTEUS_CODE).value

        # If not instance of ProteusCode, cast to string and log warning
        if isinstance(code, ProteusCode):
            code_str = f"[{code.to_string()}]"
        else:
            log.warning(
                f"PROTEUS_CODE property of object {object.id} is not instance of ProteusCode, casting to string."
            )
            code_str = f"[{str(code)}]"

    # Check for PROTEUS_NAME property
    name_property = object.get_property(PROTEUS_NAME)

    assert isinstance(
        name_property, Property
    ), f"Every object must have a PROTEUS_NAME property. Check object {object.id} properties, current return type is {type(name_property)}"

    name_str = str(name_property.value)

    # Build the name string
    item_string = f"{code_str} {name_str}".strip()
    list_item.setText(item_string)

    # Set data (ProteusID)
    list_item.setData(Qt.ItemDataRole.UserRole, object.id)

    # Set icon
    object_class: ProteusClassTag = object.classes[-1]
    icon_path: Path = Config().get_icon(TREE_MENU_ICON_TYPE, object_class)
    list_item.setIcon(QIcon(icon_path.as_posix()))
