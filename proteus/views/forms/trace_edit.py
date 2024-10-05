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
from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QSizePolicy,
    QLineEdit,
    QAbstractItemView,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import (
    ProteusID,
    ProteusClassTag,
    PROTEUS_NAME,
    PROTEUS_CODE,
    PROTEUS_ANY,
    PROTEUS_ACRONYM,
)
from proteus.model.object import Object
from proteus.model.properties.trace_property import NO_TARGETS_LIMIT
from proteus.model.properties.property import Property
from proteus.model.properties.code_property import ProteusCode
from proteus.controller.command_stack import Controller
from proteus.views.forms.check_combo_box import CheckComboBox
from proteus.application.resources.icons import Icons, ProteusIconType
from proteus.application.resources.translator import translate as _

# Module configuration
log = logging.getLogger(__name__)  # Logger


# Constants

ANY_DOCUMENT = ":Proteus-any-document"  # Used to filter documents


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

    tracesChanged = pyqtSignal()

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Object initialization.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        element_id: ProteusID,
        controller: Controller = None,
        accepted_targets: List[ProteusClassTag] = [],
        limit: int = NO_TARGETS_LIMIT,
        *args,
        **kwargs,
    ):
        """
        Object initialization.

        :param element_id: ProteusID of the element that is being edited.
        :param controller: Controller instance to get the objects.
        :param accepted_targets: List of ProteusClassTag as accepted targets.
        :param limit: Maximum number of targets allowed.
        """
        super().__init__(*args, **kwargs)

        # Validate element_id
        assert (
            element_id is not None
        ), "TraceEdit requires an element_id to be initialized."

        # Validate controller
        assert isinstance(
            controller, Controller
        ), f"TraceEdit requires a Controller instance to be initialized. Controller argument is type {type(controller)}"

        assert isinstance(
            accepted_targets, list
        ), f"TraceEdit requires a list of ProteusClassTag as accepted targets. Accepted targets argument is type {type(accepted_targets)}"

        assert isinstance(
            limit, int
        ), f"TraceEdit requires an integer as limit. Limit argument is type {type(limit)}"

        # Arguments initialization
        self.element_id: ProteusID = element_id
        self.controller: Controller = controller
        self.accepted_targets: List[ProteusClassTag] = accepted_targets
        self.limit: int = limit

        # Initialize widgets
        self.list_widget: QListWidget = None
        self.add_button: QPushButton = None
        self.remove_button: QPushButton = None

        # Create input widget
        self.create_input()

        self.tracesChanged.connect(self.update_add_button)
        self.tracesChanged.connect(self.update_remove_button)

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

        # Allow trace movement using InternalMove and not Movement.Free because
        # Free duplicates the item when dragging and dropping.
        self.list_widget.setMovement(QListWidget.Movement.Static)
        self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        self.list_widget.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )

        # Reimplement sizeHint to set a minimun height of 80px
        # NOTE: Recomended in https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qwidget.html
        self.list_widget.sizeHint = lambda: QSize(0, 80)

        # Create QPushButtons
        self.add_button = QPushButton()
        add_button_icon = Icons().icon(ProteusIconType.App, "add_trace_icon")
        self.add_button.setIcon(add_button_icon)

        self.remove_button = QPushButton()
        self.remove_button.setEnabled(False)
        remove_button_icon = Icons().icon(ProteusIconType.App, "remove_trace_icon")
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
        self.list_widget.itemClicked.connect(self.update_remove_button)

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
            try:
                object: Object = self.controller.get_element(element_id=trace)
            except Exception as e:
                log.error(
                    f"Consistency error, could not find traced object with id '{trace}', the trace will be ignored."
                    "If the user saves the form, the trace will be deleted."
                    f"Error message: {e}"
                )
                continue

            # Validate object type
            assert isinstance(
                object, Object
            ), f"Trace must be a reference to an object, id '{trace}' is not a reference to an object but to a '{type(object)}' type."

            # Create QListWidgetItem
            trace_item: QListWidgetItem = QListWidgetItem(parent=self.list_widget)
            _list_item_setup(trace_item, object)

            self.list_widget.addItem(trace_item)

        self.tracesChanged.emit()

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
            element_id=self.element_id,
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

        self.tracesChanged.emit()

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

        self.tracesChanged.emit()

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

    # ----------------------------------------------------------------------
    # Method: update_add_button
    # Description: Updates the add button status.
    # Date: 19/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_add_button(self):
        """
        Updates the add button status. Called when a trace is added, removed
        or the traces are set for the first time.
        """
        traces = self.traces()
        if self.limit > 0 and len(traces) >= self.limit:
            self.add_button.setEnabled(False)
        else:
            self.add_button.setEnabled(True)


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
        element_id: ProteusID,
        controller: Controller,
        accepted_classes: List[ProteusClassTag],
        targets: List[ProteusID] = [],
        *args,
        **kwargs,
    ):
        """
        Dialog initialization.

        :param element_id: ProteusID of the element that is being edited.
        :param controller: Controller instance to get the objects.
        :param accepted_classes: List of ProteusClassTag as accepted classes.
        :param targets: List of ProteusID as targets to discard.
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
        self.error_label: QLabel = None

        self.list_widget: QListWidget = None
        self.button_box: QDialogButtonBox = None
        self.name_filter_widget: QLineEdit = None
        self.class_selector_combo: CheckComboBox = None

        # Initialize variables
        self.edited_element_id: ProteusID = element_id
        self.selected_object: ProteusID = None

        # Create component
        self.create_component()

    # ======================================================================
    # Dialog methods
    # ======================================================================

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
        # -----------------------
        # Dialog general config
        # -----------------------

        # Set dialog title
        title: str = _("trace_edit_dialog.title")
        self.setWindowTitle(title)

        # Set window icon
        proteus_icon = Icons().icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(proteus_icon)

        # -----------------------
        # Error label
        # -----------------------
        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        self.error_label.setHidden(True)
        self.error_label.setObjectName("error_label")

        # -----------------------
        # List widget setup
        # -----------------------

        # Create QListWidget to display selectable objects
        self.list_widget = QListWidget(self)
        self.list_widget.setMovement(QListWidget.Movement.Static)
        self.list_widget.setMinimumHeight(100)
        self.list_widget.setMinimumWidth(400)

        # Get list of project objects
        objects: List[Object] = self.controller.get_objects(
            classes=self.accepted_classes
        )

        # Populate the QListWidget and store found object classes
        classes_set = set()
        object: Object
        for object in objects:
            # Skip objects that are already traced or the object itself
            if object.id in self.targets or object.id == self.edited_element_id:
                continue

            # Create QListWidgetItem
            object_item: QListWidgetItem = QListWidgetItem(parent=self.list_widget)
            _list_item_setup(object_item, object)

            # Add item to the QListWidget
            self.list_widget.addItem(object_item)

            # Add object classes to the set
            classes_set.update(object.classes)

        # -----------------------
        # Document filter
        # -----------------------

        # Get project documents
        documents: List[Object] = self.controller.get_current_project().documents

        # Create combocheckbox filter
        self.document_selector_combo: CheckComboBox = CheckComboBox()

        self.document_selector_combo.addItem(
            _("trace_edit_dialog.any_document"),
            ANY_DOCUMENT,
            True,
            Icons().icon(ProteusIconType.Document, ANY_DOCUMENT),
        )

        for document in documents:
            # Document acronym
            document_acronym = document.get_property(PROTEUS_ACRONYM).value

            document_icon = Icons().icon(ProteusIconType.Document, document_acronym)

            # Add item
            self.document_selector_combo.addItem(
                document_acronym, document.id, False, document_icon
            )

        # Connect activated signal
        self.document_selector_combo.activated.connect(self.update_list_widget)

        # -----------------------
        # Class filter
        # -----------------------

        # Create a class list ordered alphabetically and insert :Proteus-any first
        classes_list: List[ProteusClassTag] = list(classes_set)
        classes_list.sort()

        # Create combocheckbox filter
        self.class_selector_combo: CheckComboBox = CheckComboBox()
        self.class_selector_combo.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
        self.class_selector_combo.setMaximumWidth(170)

        self.class_selector_combo.addItem(
            _(f"archetype.class.{PROTEUS_ANY}"),
            PROTEUS_ANY,
            True,
            Icons().icon(ProteusIconType.Archetype),
        )

        for _class in classes_list:
            class_name_tr = _(f"archetype.class.{_class}", alternative_text=_class)

            # Class icon
            class_icon = Icons().icon(ProteusIconType.Archetype, _class)

            # Add item
            self.class_selector_combo.addItem(class_name_tr, _class, False, class_icon)

        # Connect activated signal
        self.class_selector_combo.activated.connect(self.update_list_widget)

        # -----------------------
        # Name filter
        # -----------------------

        self.name_filter_widget = QLineEdit()
        self.name_filter_widget.setPlaceholderText(
            _("trace_edit_dialog.name_filter_widget.placeholder_text")
        )

        # Connect textChanged signal
        self.name_filter_widget.textChanged.connect(self.update_list_widget)

        # -----------------------
        # Buttonbox and layout
        # -----------------------

        # Create accept and reject buttons
        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText(
            _("dialog.save_button")
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(
            _("dialog.reject_button")
        )

        # Filter layout
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.document_selector_combo)
        filter_layout.addWidget(self.class_selector_combo)
        filter_layout.addWidget(self.name_filter_widget)

        # Create a layout for the QListWidget
        main_layout = QVBoxLayout()
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.button_box)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(main_layout)

        # -----------------------
        # Final setup
        # -----------------------

        # Connect signals
        self.list_widget.currentItemChanged.connect(self.enable_accept_button)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.enable_accept_button()

        # If no objects are found perform required actions
        if self.list_widget.count() == 0:
            self.list_widget.setDisabled(True)

            classes_translations = [
                _(f"archetype.class.{_class}") for _class in self.accepted_classes
            ]
            self.error_label.setText(
                _("trace_edit_dialog.error_label.no_objects", classes_translations)
            )
            self.error_label.setHidden(False)

            self.name_filter_widget.setDisabled(True)
            self.class_selector_combo.setDisabled(True)
            self.document_selector_combo.setDisabled(True)

    # ======================================================================
    # Dialog slots methods (connected to the component signals and helpers)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_list_widget
    # Description: Updates the QListWidget items.
    # Date       : 01/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_list_widget(self) -> None:
        """
        Updates the QListWidget items.
        """
        # Unselect the current item
        self.list_widget.setCurrentItem(None)

        # Selected classes, documents and the name filter
        selected_documents = self.document_selector_combo.checkedItemsData()
        selected_classes = self.class_selector_combo.checkedItemsData()
        name_filter_text = self.name_filter_widget.text().lower()

        # Iterate over the QListWidget items and hide the ones
        # that do not match the class filter
        for i in range(self.list_widget.count()):
            # Get the item
            item: QListWidgetItem = self.list_widget.item(i)

            # Get the object to compare classes
            object: Object = self.controller.get_element(
                element_id=item.data(Qt.ItemDataRole.UserRole)
            )

            # Get list widget item text lowercased to compare with the name filter
            object_name: str = item.text().lower()

            # Check conditions one by one, they are ordered by computation cost
            # Condition 1: Name filter -----------------
            if name_filter_text != "":
                if not name_filter_text in object_name:
                    item.setHidden(True)
                    continue

            # Condition 2: Class filter ----------------
            if not PROTEUS_ANY in selected_classes:
                if not any(
                    object_class in selected_classes for object_class in object.classes
                ):
                    item.setHidden(True)
                    continue

            # Condition 3: Document filter -------------
            if not ANY_DOCUMENT in selected_documents:
                if not object.get_document().id in selected_documents:
                    item.setHidden(True)
                    continue

            # If the object passes all the conditions, show it
            item.setHidden(False)

            

    # ----------------------------------------------------------------------
    # Method     : enable_accept_button
    # Description: Enables the accept button.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def enable_accept_button(self) -> None:
        """
        Enables the accept button when an item is selected. If the item is
        deselected, the accept button is disabled.
        """
        index: QListWidgetItem = self.list_widget.currentItem()
        if index is None:
            self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(
                False
            )
        else:
            self.button_box.button(QDialogButtonBox.StandardButton.Save).setEnabled(
                True
            )

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

        assert isinstance(
            current_item, QListWidgetItem
        ), f"Current item must be a QListWidgetItem, current return type is {type(current_item)}"

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

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog
    # Description: Creates and executes the dialog.
    # Date       : 25/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(
        element_id: ProteusID,
        controller: Controller,
        accepted_classes: List[ProteusClassTag],
        targets: List[ProteusID] = [],
    ) -> ProteusID:
        """
        Creates and executes the dialog.
        """
        # Create dialog
        dialog = TraceEditDialog(element_id, controller, accepted_classes, targets)

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
    icon = Icons().icon(ProteusIconType.Archetype, object_class)
    list_item.setIcon(icon)
