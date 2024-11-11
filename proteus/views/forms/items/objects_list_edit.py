# ==========================================================================
# File: objects_list_edit.py
# Description: objects list edit input for the PROTEUS application
# Date: 07/11/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import List, Callable

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QStandardItem
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import (
    QListWidgetItem,
    QSizePolicy,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import (
    ProteusClassTag,
    PROTEUS_CODE,
    PROTEUS_NAME,
    PROTEUS_ANY,
    PROTEUS_ACRONYM,
)
from proteus.model.properties import Property
from proteus.model.properties.code_property import ProteusCode
from proteus.model.object import Object
from proteus.controller.command_stack import Controller
from proteus.application.resources.icons import Icons, ProteusIconType
from proteus.application.resources.translator import translate as _
from proteus.views.forms.check_combo_box import CheckComboBox
from proteus.views.forms.items.item_list_edit import ItemListEdit, ItemListEditDialog


# Constants

ANY_DOCUMENT = ":Proteus-any-document"  # Used to filter documents

# Module configuration
log = logging.getLogger(__name__)  # Logger


# --------------------------------------------------------------------------
# Class: ObjectsListEdit
# Description: Objects list edit input for the PROTEUS application
# Date: 07/11/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ObjectsListEdit(ItemListEdit):
    """
    Inherit from ItemListEdit. Objects list edit input for the PROTEUS application.
    Let the user add, remove and change the order of the objects in the list.
    """

    def __init__(
        self,
        controler: Controller,
        candidates: List[Object],
        item_limit: int = -1,
        *args,
        **kargs,
    ):
        super().__init__(candidates, item_limit, *args, **kargs)

        assert isinstance(controler, Controller), "A Controller instance is required"

        self.controller = controler
        self.candidates: List[Object] = candidates

    # --------------------------------------------------------------------------
    # Method: list_item_setup (override)
    # Description: Setup list item
    # Date: 07/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def list_item_setup(self, list_item: QListWidgetItem, object: Object) -> None:
        """
        Setup list item with object's information (name, code, icon).

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

    # ----------------------------------------------------------------------
    # Method: add_item (override)
    # Description: Adds an item to the list widget.
    # Date: 06/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_item(self):
        """
        Adds an item to the list widget.
        """
        # Make the intersection between the candidates and the current items
        current_items = self.items()
        candidates = [item for item in self.candidates if item.id not in current_items]

        # Get the selected item
        dialog: ObjectsListEditDialog = ObjectsListEditDialog.create_dialog(
            self.controller, candidates, self.list_item_setup
        )

        select_item_data = dialog.selected_item_data

        # Add the item to the list
        if select_item_data is not None:
            list_item = QListWidgetItem(self.item_list)
            _object: Object = self.controller.get_element(select_item_data)
            self.list_item_setup(list_item, _object)
            self.item_list.addItem(list_item)

            self.itemsChanged.emit()


# --------------------------------------------------------------------------
# Class: ObjectsListEditDialog
# Description: Objects list edit dialog for the PROTEUS application
# Date: 07/11/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ObjectsListEditDialog(ItemListEditDialog):
    """
    Inherit from ItemListEditDialog. Objects list edit dialog for the PROTEUS application.
    Adds document and class filters to the generic item list edit dialog.
    """

    def __init__(
        self,
        controller: Controller,
        candidates: List[Object],
        setup_method: Callable,
        *args,
        **kargs,
    ):
        super().__init__(candidates, setup_method, *args, **kargs)

        self.controller = controller
        self.candidates: List[Object] = candidates

        self.class_selector_combo: CheckComboBox = None
        self.document_selector_combo: CheckComboBox = None

        # Add filters
        self.document_filter()
        self.class_filter()
        
        # Remove the name filter and add it again to the layout
        name_filter = self.filters_layout.takeAt(0)
        self.filters_layout.addWidget(name_filter.widget())

    # ==========================================================================
    # Specific filters
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: class_filter
    # Description: Create class filter
    # Date: 07/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def class_filter(self) -> None:
        """
        Creates a class filter and adds it to the filters layout. Iterates over
        the candidates in order to get all the available classes.
        """
        # Get all classes from candidates
        classes_set: set = set()
        # object: Object
        for object in self.candidates:
            classes_set.update(object.classes)

        classes_list = list(classes_set)
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
        self.class_selector_combo.view().pressed.connect(
            self.selector_class_filter_pressed
        )

        # Add to layout
        self.filters_layout.addWidget(self.class_selector_combo)

    # --------------------------------------------------------------------------
    # Method: document_filter
    # Description: Create document filter
    # Date: 07/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def document_filter(self) -> None:
        """
        Creates a document filter and adds it to the filters layout. Iterates over
        the candidates in order to get all the available documents.
        """
        # Get project documents
        documents: List[Object] = self.controller.get_current_project().documents

        # Create combocheckbox filter
        self.document_selector_combo: CheckComboBox = CheckComboBox()

        self.document_selector_combo.addItem(
            _("items_edit_dialog.any_document"),
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
        self.document_selector_combo.view().pressed.connect(
            self.selector_document_filter_pressed
        )

        # Add to layout
        self.filters_layout.addWidget(self.document_selector_combo)

    # ----------------------------------------------------------------------
    # Method     : selector_filter_pressed
    # Description: Handle the filter pressed signal.
    # Date       : 21/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def selector_document_filter_pressed(self, index: QModelIndex) -> None:
        self._selector_filter_pressed(self.document_selector_combo, index)

    def selector_class_filter_pressed(self, index: QModelIndex) -> None:
        self._selector_filter_pressed(self.class_selector_combo, index)

    def _selector_filter_pressed(
        self, combo_item: CheckComboBox, index: QModelIndex
    ) -> None:
        """
        Handle the filter pressed signal to change the check state of the
        selector items. We assume that the first item is the 'any' option.

        Calls update_list_widget to update the QListWidget items.
        """
        item: QStandardItem = combo_item.model().itemFromIndex(index)

        # If first item is pressed, deselect any other items
        if item.index().row() == 0:
            for i in range(1, combo_item.count()):
                item = combo_item.model().item(i)
                item.setCheckState(Qt.CheckState.Unchecked)
        else:
            # Deselect any document item
            item = combo_item.model().item(0)
            item.setCheckState(Qt.CheckState.Unchecked)

        # Update the list widget
        self.update_item_list()

    # --------------------------------------------------------------------------
    # Method: update_item_list (override)
    # Description: Update the item list
    # Date: 08/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_item_list(self):
        """
        Override update_item_list to filter the objects by class, document and
        the search text.
        """
        # Selected classes, documents and the name filter
        selected_documents = self.document_selector_combo.checkedItemsData()
        selected_classes = self.class_selector_combo.checkedItemsData()
        name_filter_text = self.name_filter_widget.text().lower()

        # Iterate over the QListWidget items and hide the ones
        # that do not match the class filter
        for i in range(self.item_list.count()):
            # Get the item
            item: QListWidgetItem = self.item_list.item(i)

            # Get the object to compare classes
            object: Object = self.controller.get_element(
                element_id=item.data(Qt.ItemDataRole.UserRole)
            )

            # Get list widget item text lowercased to compare with the name filter
            object_name: str = item.text().lower()

            # Check conditions one by one, they are ordered by computation cost
            # Condition 1: Name filter -----------------
            if name_filter_text != "":
                if name_filter_text not in object_name:
                    item.setHidden(True)
                    continue

            # Condition 2: Class filter ----------------
            if PROTEUS_ANY not in selected_classes:
                if not any(
                    object_class in selected_classes for object_class in object.classes
                ):
                    item.setHidden(True)
                    continue

            # Condition 3: Document filter -------------
            if ANY_DOCUMENT not in selected_documents:
                if object.get_document().id not in selected_documents:
                    item.setHidden(True)
                    continue

            # If the object passes all the conditions, show it
            item.setHidden(False)

        current_item = self.item_list.currentItem()
        if current_item:
            if current_item.isHidden():
                self.item_list.setCurrentItem(None)

    @staticmethod
    def create_dialog(
        controller: Controller, candidates: List[Object], setup_method: Callable
    ) -> "ObjectsListEditDialog":
        """
        Create a dialog instance with the given parameters.

        :param controller: Controller instance.
        :param candidates: List of objects to select from.
        :param setup_method: Method to setup the list item.
        :return: ObjectsListEditDialog instance.
        """
        dialog = ObjectsListEditDialog(controller, candidates, setup_method)
        dialog.exec()

        return dialog
