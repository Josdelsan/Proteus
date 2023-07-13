# ==========================================================================
# File: document_tree.py
# Description: PyQT6 document structure tree component for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import Dict, List
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction, QDropEvent, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QMenu,
    QStyle,
    QApplication,
    QMessageBox,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.config import Config
from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.model.abstract_object import ProteusState
from proteus.views.utils.event_manager import Event, EventManager
from proteus.views.utils.state_manager import StateManager
from proteus.views.utils.translator import Translator
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.controller.command_stack import Controller

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Global variables and constants
# --------------------------------------------------------------------------

# TODO: Avoid hardcoding paths
# Tree icons
TREE_ICONS = {
    "section": "tree_icons/section.svg",
    "paragraph": "tree_icons/paragraph.svg",
    ":Proteus-document": "tree_icons/document.svg",
    "actor": "tree_icons/actor.svg",
}

# Tree item color
TREE_ITEM_COLOR = {
    ProteusState.FRESH: Qt.GlobalColor.darkGreen,
    ProteusState.DIRTY: Qt.GlobalColor.darkYellow,
    ProteusState.DEAD: Qt.GlobalColor.darkRed,
    ProteusState.CLEAN: Qt.GlobalColor.black,
}


# --------------------------------------------------------------------------
# Class: DocumentTree
# Description: PyQT6 document structure tree component class for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DocumentTree(QWidget):
    """
    Document structure tree component for the PROTEUS application. It is used
    to manage the creation of the document structure tree and its actions.
    Display the document structure like a file system tree.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        parent=None,
        element_id=None,
        controller: Controller = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.

        Store the document id reference. Create the tree widget and the
        tree items dictionary to make easier the access to the tree items
        on update events using the element id.
        """
        super().__init__(parent, *args, **kwargs)
        # Controller instance
        assert isinstance(
            controller, Controller
        ), "Must provide a controller instance to the document tree component"
        self._controller: Controller = controller

        # Translator instance
        self.translator = Translator()

        # Set tree document id
        self.element_id: ProteusID = element_id

        # tree widget
        self.tree_widget: QTreeWidget = None

        # Tree items dictionary used to make easier the access to the tree
        # items on update events. Access by object id.
        self.tree_items: Dict[ProteusID, QTreeWidgetItem] = {}

        # Create the component
        self.create_component()

        # Subscribe to events
        EventManager.attach(Event.MODIFY_OBJECT, self.update_on_modify_object, self)
        EventManager.attach(Event.SAVE_PROJECT, self.update_on_save_project, self)
        EventManager.attach(Event.ADD_OBJECT, self.update_on_add_object, self)
        EventManager.attach(Event.DELETE_OBJECT, self.update_on_delete_object, self)

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the document tree for the document referenced by
    #              the element id.
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the document tree for the document referenced by the element
        id.
        """
        # Create vertical layout
        layout: QVBoxLayout = QVBoxLayout(self)

        # Create tree widget and set header
        self.tree_widget = QTreeWidget()
        self.tree_widget.header().setVisible(False)

        # Set drag and drop properties
        self.tree_widget.setDragEnabled(True)
        self.tree_widget.setAcceptDrops(True)
        self.tree_widget.setDropIndicatorShown(True)
        self.tree_widget.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)

        # Connect drag and drop events
        # TODO: Drag must show if drop is allowed for different objects types
        self.tree_widget.dropEvent = self.drop_event

        # Get document structure and top level items
        top_level_object: Object = self._controller.get_element(self.element_id)

        # Populate tree widget
        self.populate_tree(self.tree_widget, top_level_object)

        # Connect double click to object properties form
        self.tree_widget.itemDoubleClicked.connect(
            lambda item: PropertyDialog.create_dialog(
                element_id=item.data(1, 0), controller=self._controller
            )
        )

        # Connect click to object selection
        self.tree_widget.itemClicked.connect(
            lambda item: StateManager.set_current_object(
                object_id=item.data(1, 0), document_id=self.element_id
            )
        )

        # Set context menu policy
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Expand all items and disable double click expand
        self.tree_widget.expandAll()
        self.tree_widget.setExpandsOnDoubleClick(False)

        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

    # ----------------------------------------------------------------------
    # Method     : delete_component
    # Description: Delete the document tree component.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_component(self, *args, **kwargs) -> None:
        """
        Manage the deletion of the document tree component. Detach from
        events and delete the component.

        This method must be called by the parent component in order to
        delete the document tree before deleting the parent (document tab)
        """
        # Detach from events
        EventManager.detach(self)

        # Delete the component
        self.parent = None
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : populate_tree
    # Description: Populate document tree given the document structure
    # Date       : 04/06/2023
    # Version    : 0.2
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def populate_tree(
        self, parent_item: QTreeWidgetItem, object: Object, position=None
    ):
        """
        Populate the document tree given an object. This method is recursive.
        Iterate over the object children and populate the tree with them.

        :param parent_item: The parent item of the object
        :param object: The object to populate the tree
        """
        # If object is DEAD do not add it to the tree
        if object.state == ProteusState.DEAD:
            return

        # Create the new item, if position is not None insert the item in
        # the given position
        if position is not None:
            new_item = QTreeWidgetItem(None, [object.get_property("name").value])
            parent_item.insertChild(position, new_item)
        else:
            new_item = QTreeWidgetItem(parent_item, [object.get_property("name").value])

        # Set the item color based on the object ProteusState
        new_item.setForeground(0, TREE_ITEM_COLOR[object.state])

        # Set the icon based on the object last class
        object_class: str = object.classes.split()[-1]
        try:
            icon_path: Path = Config().icons_directory / TREE_ICONS[object_class]
            new_item.setIcon(0, QIcon(icon_path.as_posix()))
        except KeyError:
            icon_path: Path = Config().icons_directory / TREE_ICONS["paragraph"]
            new_item.setIcon(0, QIcon(icon_path.as_posix()))

        # Set the item data to store the object id
        new_item.setData(1, 0, object.id)

        # Add the new item to the tree items dictionary
        self.tree_items[object.id] = new_item

        # Check if the object has children
        for child in object.children:
            self.populate_tree(new_item, child)

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_on_modify_object
    # Description: Update the document tree when an object is modified.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_modify_object(self, *args, **kwargs) -> None:
        """
        Update the document tree when an object is modified. Look for the
        object in the tree items dictionary and update the tree item properties.

        Triggered by: Event.MODIFY_OBJECT
        """
        # Get the modifies element id
        element_id: ProteusID = kwargs.get("element_id")

        # Check the element id is not None
        assert element_id is not None, "Element id is None on MODIFY_OBJECT event"

        # Check if the element id is in the tree items dictionary
        if element_id not in self.tree_items:
            return

        # Get the tree item
        tree_item: QTreeWidgetItem = self.tree_items[element_id]

        # Get the object
        object: Object = self._controller.get_element(element_id)

        # Update the tree item
        tree_item.setText(0, object.get_property("name").value)
        tree_item.setForeground(0, TREE_ITEM_COLOR[object.state])

    # ----------------------------------------------------------------------
    # Method     : update_on_save_project
    # Description: Update the document tree when a project is saved.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_save_project(self, *args, **kwargs) -> None:
        """
        Update the document tree when a project is saved. Iterate over the
        tree items and set the color to black (no changes).

        Triggered by: Event.SAVE_PROJECT
        """
        items = self.tree_items.values()
        for tree_item in items:
            tree_item.setForeground(0, Qt.GlobalColor.black)

    # ----------------------------------------------------------------------
    # Method     : update_on_add_object
    # Description: Update the document tree when an object is added.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_add_object(self, *args, **kwargs) -> None:
        """
        Update the document tree when an object is added. Look for the
        parent item in the tree items dictionary and add the new item to
        the parent item including the new object children. Update the parent
        item color based on the parent object ProteusState.

        Triggered by: Event.ADD_OBJECT
        """
        # Get the new object
        new_object: Object = kwargs.get("object")

        # Check the object is instance of Object
        assert isinstance(
            new_object, Object
        ), "Object is not instance of Object on ADD_OBJECT event"

        # Check if the parent item is in the tree items dictionary
        if new_object.parent.id not in self.tree_items:
            return

        # Get the parent item
        parent_item: QTreeWidgetItem = self.tree_items[new_object.parent.id]

        # Update the parent item color
        # NOTE: Parent will always be an Object. Project cannot be selected
        #       as parent to trigger ADD_OBJECT event. When adding an object
        #       with Project as parent ADD_DOCUMENT event is triggered.
        parent: Object = self._controller.get_element(new_object.parent.id)
        parent_item.setForeground(0, TREE_ITEM_COLOR[parent.state])

        # Calculate item position relative to its siblings omits DEAD objects
        siblings: List[Object] = [
            s
            for s in new_object.parent.get_descendants()
            if s.state != ProteusState.DEAD
        ]
        position: int = siblings.index(new_object)

        # Create the new item
        self.populate_tree(parent_item, new_object, position=position)

    # ----------------------------------------------------------------------
    # Method     : update_on_delete_object
    # Description: Update the document tree when an object is deleted.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_delete_object(self, *args, **kwargs) -> None:
        """
        Update the document tree when an object is deleted. Look for the
        object in the tree items dictionary and remove the item from its
        parent item and tree items dictionary. Update the parent item color
        based on the parent object ProteusState.

        Triggered by: Event.DELETE_OBJECT
        """

        def delete_item(item: QTreeWidgetItem) -> None:
            """
            Helper method to delete item widget and its children recursively.
            """
            # Get the children widgets
            children_widgets: List[QTreeWidgetItem] = [
                item.child(i) for i in range(item.childCount())
            ]

            # Iterate over the children widgets
            for child_widget in children_widgets:
                delete_item(child_widget)

            # Remove the item from its parent
            item.parent().removeChild(item)

            # Remove the item from the tree items dictionary
            self.tree_items.pop(item.data(1, 0))

        # Get the deleted object id
        element_id: ProteusID = kwargs.get("element_id")

        # Check the element id is not None
        assert element_id is not None, "Element id is None on DELETE_OBJECT event"

        # Check if the element id is in the tree items dictionary
        if element_id not in self.tree_items:
            return

        # Get the tree item
        tree_item: QTreeWidgetItem = self.tree_items[element_id]

        # Get parent object to update the color
        # NOTE: Parent will always be an Object. Project cannot be selected
        #       as parent to trigger DELETE_OBJECT event. When deleting object
        #       with Project parent DELETE_DOCUMENT event is triggered.
        parent_id: ProteusID = tree_item.parent().data(1, 0)
        parent_object: Object = self._controller.get_element(parent_id)
        tree_item.parent().setForeground(0, TREE_ITEM_COLOR[parent_object.state])

        # Remove the item from the tree including its children
        delete_item(tree_item)

    # ======================================================================
    # Component slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : show_context_menu
    # Description: Manage the context menu event. Display a context menu
    #              with the available actions for the selected object.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def show_context_menu(self, position):
        """
        Manage the context menu event. Display a context menu with the
        available actions for the selected object.
        """
        # Get the selected item
        selected_item: QTreeWidgetItem = self.tree_widget.currentItem()

        # Check if the selected item is not None
        if selected_item is None:
            return

        # Get the selected item id
        selected_item_id: ProteusID = selected_item.data(1, 0)

        # Do not show context menu for document root item
        # NOTE: Elements stored in the tree items dictionary are always
        #       Objects.
        element: Object = self._controller.get_element(selected_item_id)
        is_document: bool = isinstance(element.parent, Project)
        if is_document:
            return

        # Get selected item index and parent item id to handle object
        # position changes.
        position_index: int = self.tree_widget.indexFromItem(selected_item).row()
        parent_id: ProteusID = selected_item.parent().data(1, 0)

        # Create the context menu
        context_menu: QMenu = QMenu(self)

        # Create the edit action --------------------------------------------
        action_edit_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.edit"), self
        )
        action_edit_object.triggered.connect(
            lambda: PropertyDialog.create_dialog(
                element_id=selected_item_id, controller=self._controller
            )
        )
        edit_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_FileDialogDetailedView
        )
        action_edit_object.setIcon(edit_icon)

        # Create the delete action ------------------------------------------
        action_delete_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.delete"), self
        )
        action_delete_object.triggered.connect(
            lambda: self.delete_object(selected_item_id)
        )
        delete_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_TrashIcon
        )
        action_delete_object.setIcon(delete_icon)

        # Create clone action -----------------------------------------------
        action_clone_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.clone"), self
        )
        action_clone_object.triggered.connect(
            lambda: self._controller.clone_object(selected_item_id)
        )
        clone_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogApplyButton
        )
        action_clone_object.setIcon(clone_icon)

        # Create move up action ---------------------------------------------
        action_move_up_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.move_up"), self
        )
        action_move_up_object.triggered.connect(
            lambda: self._controller.change_object_position(
                selected_item_id, position_index - 1, parent_id
            )
        )
        move_up_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowUp
        )
        action_move_up_object.setIcon(move_up_icon)

        # Create move down action -------------------------------------------
        action_move_down_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.move_down"), self
        )
        # TODO: Fix change position method to avoid using +2
        action_move_down_object.triggered.connect(
            lambda: self._controller.change_object_position(
                selected_item_id, position_index + 2, parent_id
            )
        )
        move_down_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowDown
        )
        action_move_down_object.setIcon(move_down_icon)

        # Disable the move up action if the selected item is the first
        # item in the list
        if position_index == 0:
            action_move_up_object.setEnabled(False)

        # Disable the move down action if the selected item is the last
        # item in the list
        if position_index == selected_item.parent().childCount() - 1:
            action_move_down_object.setEnabled(False)

        # Add the actions to the context menu
        context_menu.addAction(action_edit_object)
        context_menu.addAction(action_delete_object)
        context_menu.addAction(action_clone_object)
        context_menu.addAction(action_move_up_object)
        context_menu.addAction(action_move_down_object)

        # Show the context menu
        context_menu.exec(self.tree_widget.viewport().mapToGlobal(position))

    # ----------------------------------------------------------------------
    # Method     : delete_object
    # Description: Manage the delete key pressed event. Delete the selected
    #              object.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    # TODO: Consider connecting this method directly to the delete key
    #       pressed event.
    def delete_object(self, element_id: ProteusID) -> None:
        """
        Manage the delete key pressed event. Delete the selected object.
        """
        # Delete the object
        self._controller.delete_object(element_id)

    # ----------------------------------------------------------------------
    # Method     : drop_event
    # Description: Manage the drop event. Move the dropped object to the
    #              target position.
    # Date       : 14/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def drop_event(self, event: QDropEvent):
        # Get dropped element_id
        dropped_item = self.tree_widget.currentItem()
        dropped_element_id: ProteusID = dropped_item.data(1, 0)

        # Drop position
        point: QPoint = event.position().toPoint()

        # Get target element_id
        target_item = self.tree_widget.itemAt(point)
        try:
            target_element_id: ProteusID = target_item.data(1, 0)
        except AttributeError:
            log.warning(f"Target item not found at position {point}.")
            return

        # Check if dropped item and target item are not None
        if dropped_item and target_item:
            # Determine the drop behavior based on the drop position.
            # If drop position is in the middle of the target item (50% height
            # centered at the target item), then the dropped item will
            # be added as a child of the target item. Otherwise, the dropped
            # item will be added as a sibling of the target item depending on
            # the drop position (above or below the target item).
            target_rect = self.tree_widget.visualItemRect(target_item)
            rect_center = target_rect.center()
            rect_height = target_rect.height()

            # Get the index of the target item
            target_index: int = self.tree_widget.indexFromItem(target_item).row()

            # Get the parent id
            try:
                parent_id: ProteusID = target_item.parent().data(1, 0)
            except AttributeError:
                log.warning(
                    "Failed to get the parent id of the target item. The target item is a root item."
                )
                return

            try:
                # If in the 25% of the bottom of the target item, then add the
                # dropped item as a sibling above the target item
                if event.position().y() > rect_center.y() + rect_height / 4:
                    log.info(
                        f"Tree element with id {dropped_element_id} dropped below {target_index} insert in {target_index + 1}."
                    )
                    self._controller.change_object_position(
                        dropped_element_id, target_index + 1, parent_id
                    )

                # If in the 25% of the top of the target item, then add the
                # dropped item as a sibling below the target item
                elif event.position().y() < rect_center.y() - rect_height / 4:
                    log.info(
                        f"Tree element with id {dropped_element_id} dropped above {target_index} insert in {target_index}."
                    )
                    self._controller.change_object_position(
                        dropped_element_id, target_index, parent_id
                    )

                # If in the middle of the target item, then add the dropped item
                # as a child of the target item. Position as None means that the
                # dropped item will be added as the last child of the target item.
                else:
                    log.info(
                        f"Tree element with id {dropped_element_id} dropped inside {target_index} insert at the end of the children list."
                    )
                    self._controller.change_object_position(
                        dropped_element_id, None, target_element_id
                    )
            # Catch exception in case the operation is forbidden
            except AssertionError as e:
                log.warning(
                    f"{e}"
                )

                # Show a message box to the user
                QMessageBox.warning(
                    self,
                    self.translator.text("document_tree.drop_action.message_box.error.title"),
                    self.translator.text("document_tree.drop_action.message_box.error.text"),
                )

