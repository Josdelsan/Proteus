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

from typing import Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.object import Object
from proteus.model.abstract_object import ProteusState
from proteus.views.utils.decorators import subscribe_to
from proteus.views.utils.event_manager import Event
from proteus.views.components.property_form import PropertyForm
from proteus.controller.command_stack import Command

# --------------------------------------------------------------------------
# Class: DocumentTree
# Description: PyQT6 document structure tree component class for the PROTEUS
#              application
# Date: 25/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@subscribe_to([Event.MODIFY_OBJECT])
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

        # Form window widget
        # NOTE: This is used to avoid memory leaks
        self.form_window = None

        # Tree items dictionary used to make easier the access to the tree
        # items on update events. Access by object id
        self.tree_items = {}

        # Create the component
        self.create_component()
        

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
        tree_widget = QTreeWidget()
        tree_widget.header().setVisible(False)

        # Get document structure and top level items
        structure : Dict = Command.get_object_structure(self.element_id)

        # Populate tree widget
        self.populate_tree(tree_widget, [structure])

        # Connect double click to object properties form
        tree_widget.itemDoubleClicked.connect(self.object_properties_form)

        # Expand all items and disable double click expand
        tree_widget.expandAll()
        tree_widget.setExpandsOnDoubleClick(False)

        layout.addWidget(tree_widget)
        self.setLayout(layout)


    # ----------------------------------------------------------------------
    # Method     : update_component
    # Description: Update the document tree for each document in the project
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_component(self, event, *args, **kwargs) -> None:
        """
        Update the document tree component depending on the event received.
        """
        # Handle events
        match event:
            case Event.MODIFY_OBJECT:
                # Get the modifies element id
                element_id = kwargs.get("element_id")

                # Check if the element id is in the tree items dictionary
                if element_id in self.tree_items:
                    # Get the tree item
                    tree_item = self.tree_items[element_id]

                    # Get the object
                    object : Object = Command.get_element(element_id)

                    # Update the tree item
                    tree_item.setText(0, object.get_property("name").value)
                    
                    if object.state is ProteusState.DIRTY:
                        tree_item.setForeground(0, Qt.GlobalColor.darkGreen)
                    else:
                        tree_item.setForeground(0, Qt.GlobalColor.black)


        

    # ----------------------------------------------------------------------
    # Method     : populate_tree
    # Description: Populate document tree given the document structure
    # Date       : 25/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def populate_tree(self, parent_item, children):
        for child_dict in children:
            # Get child object and its name
            child = list(child_dict.keys())[0]
            child_name = child.get_property("name").value

            # Create child item
            child_item = QTreeWidgetItem(parent_item, [child_name])

            # Store child id in the item data column 1 role 0
            child_item.setData(1, 0, child.id)

            # Add child item to tree items dictionary
            self.tree_items[child.id] = child_item

            # Populate child item
            self.populate_tree(child_item, child_dict[child]) 


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
        def form_window_cleanup():
            # Cleanup the reference to the form window
            self.form_window = None
            self.parent().setEnabled(True)


        if self.form_window is None:

            # Get item id
            item_id = item.data(1, 0)

            # Create the properties form window
            self.form_window = PropertyForm(element_id=item_id)

            # Set the widget to be deleted on close and to stay on top
            self.form_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  
            self.form_window.setWindowFlags(self.form_window.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

            # Show the form window
            self.form_window.show()

            # Connect the form window's `destroyed` signal to cleanup
            self.form_window.destroyed.connect(form_window_cleanup)

            # Disable the main application window
            self.parent().setEnabled(False)
        else:
            # If the window is already open, activate it, raise it, and play a system alert sound
            self.form_window.activateWindow()
            self.form_window.raise_()
            QApplication.beep()

