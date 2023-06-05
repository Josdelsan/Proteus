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


# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QMenu,
    QStyle,
    QApplication,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.model.abstract_object import ProteusState
from proteus.views.utils.decorators import subscribe_to, trigger_on
from proteus.views.utils.event_manager import Event, EventManager
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.controller.command_stack import Controller

# --------------------------------------------------------------------------
# Global variables and constants
# --------------------------------------------------------------------------

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
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent=None, element_id=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Set tree document id
        self.element_id = element_id

        # tree widget
        self.tree_widget = None

        # Tree items dictionary used to make easier the access to the tree
        # items on update events. Access by object id
        self.tree_items = {}

        # Create the component
        self.create_component()

        # Subscribe to events
        EventManager.attach(Event.MODIFY_OBJECT, self.update_on_modify_object, self)
        EventManager.attach(Event.SAVE_PROJECT, self.update_on_save_project, self)
        EventManager.attach(Event.ADD_OBJECT, self.update_on_add_object, self)
        EventManager.attach(Event.DELETE_OBJECT, self.update_on_delete_object, self)

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the document tree for each document in the project
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the document tree for each document in the project.
        """
        # Create vertical layout
        layout = QVBoxLayout(self)

        # Create tree widget and set header
        self.tree_widget = QTreeWidget()
        self.tree_widget.header().setVisible(False)

        # Get document structure and top level items
        top_level_object: Object = Controller.get_element(self.element_id)

        # Populate tree widget
        self.populate_tree(self.tree_widget, top_level_object)

        # Connect double click to object properties form
        self.tree_widget.itemDoubleClicked.connect(self.object_properties_form)
        self.tree_widget.itemClicked.connect(self.select_object)

        # Set context menu policy
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Expand all items and disable double click expand
        self.tree_widget.expandAll()
        self.tree_widget.setExpandsOnDoubleClick(False)

        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

    # ----------------------------------------------------------------------
    def update_on_modify_object(self, *args, **kwargs) -> None:
        # Get the modifies element id
        element_id = kwargs.get("element_id")

        # Check if the element id is in the tree items dictionary
        if element_id not in self.tree_items:
            return
        
        # Get the tree item
        tree_item = self.tree_items[element_id]

        # Get the object
        object: Object = Controller.get_element(element_id)

        # Update the tree item
        tree_item.setText(0, object.get_property("name").value)
        tree_item.setForeground(0, TREE_ITEM_COLOR[object.state])

    # ----------------------------------------------------------------------
    def update_on_save_project(self, *args, **kwargs) -> None:
        items = self.tree_items.values()
        for tree_item in items:
            tree_item.setForeground(0, Qt.GlobalColor.black)

    # ----------------------------------------------------------------------
    def update_on_add_object(self, *args, **kwargs) -> None:
        # Get the new object
        new_object = kwargs.get("object")

        # Check if the parent item is in the tree items dictionary
        if new_object.parent.id not in self.tree_items:
            return

        # Get the parent item
        parent_item = self.tree_items[new_object.parent.id]

        # Update the parent item color
        parent = Controller.get_element(new_object.parent.id)
        parent_item.setForeground(0, TREE_ITEM_COLOR[parent.state])

        # Create the new item
        self.populate_tree(parent_item, new_object)

    # ----------------------------------------------------------------------
    def update_on_delete_object(self, *args, **kwargs) -> None:
        # Get the deleted object id
        element_id = kwargs.get("element_id")

        # Check if the element id is in the tree items dictionary
        if element_id not in self.tree_items:
            return

        # Get the tree item
        tree_item = self.tree_items[element_id]

        # Get parent object to update the color
        parent_id: ProteusID = tree_item.parent().data(1, 0)
        parent_object = Controller.get_element(parent_id)
        tree_item.parent().setForeground(
            0, TREE_ITEM_COLOR[parent_object.state]
        )

        # Remove the item from the tree
        tree_item.parent().removeChild(tree_item)

        # Remove the item from the tree items dictionary
        self.tree_items.pop(element_id)

    # ----------------------------------------------------------------------
    # Method     : delete_component
    # Description: Delete the document render component.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_component(self, *args, **kwargs) -> None:
        """
        Delete the document render component.
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
    def populate_tree(self, parent_item, object):
        """
        Populate the document tree given an object. This method is recursive.
        Iterate over the object children and populate the tree with them.

        :param parent_item: The parent item of the object
        :param object: The object to populate the tree
        """
        # Create the new item
        new_item = QTreeWidgetItem(parent_item, [object.get_property("name").value])
        new_item.setForeground(0, TREE_ITEM_COLOR[object.state])
        new_item.setData(1, 0, object.id)

        # Add the new item to the tree items dictionary
        self.tree_items[object.id] = new_item

        # Check if the object has children
        for child in object.children:
            self.populate_tree(new_item, child)

    # ----------------------------------------------------------------------
    # Component action methods
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # Method     : object_properties_form
    # Description: Manage the itemDoubleClicked event. Display a form with
    #              the object properties separated by categories. Only one
    #              form can be opened at a time.
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def object_properties_form(self, item):
        """
        Manage the itemDoubleClicked event. Display a form with the object
        properties separated by categories. Only one form can be opened at a
        time.
        """
        # Get item id
        item_id = item.data(1, 0)

        # Create the properties form window
        form_window = PropertyDialog(element_id=item_id)
        form_window.exec()

    # ----------------------------------------------------------------------
    # Method     : select_object
    # Description: Manage the itemClicked event. Select the object in the
    #              view.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def select_object(self, item):
        """
        Manage the itemClicked event. Select the object in the view.
        """
        # Get item id
        item_id = item.data(1, 0)

        # Select object in the view
        Controller.select_object(item_id)

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
        selected_item = self.tree_widget.currentItem()

        # Check if the selected item is not None
        if selected_item is None:
            return

        # Get the selected item id
        selected_item_id = selected_item.data(1, 0)

        # Get the selected item object
        selected_item_object = Controller.get_element(selected_item_id)

        # Create the context menu
        context_menu = QMenu(self)

        # Create the delete action
        action_delete_object = QAction("Delete", self)
        action_delete_object.triggered.connect(
            lambda: Controller.delete_object(selected_item_id)
        )
        delete_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_TrashIcon
        )
        action_delete_object.setIcon(delete_icon)

        # Add the actions to the context menu
        context_menu.addAction(action_delete_object)

        # Show the context menu
        context_menu.exec(self.tree_widget.viewport().mapToGlobal(position))
