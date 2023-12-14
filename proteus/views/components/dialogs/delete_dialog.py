# ==========================================================================
# File: delete_dialog.py
# Description: PyQT6 delete dialog component for the PROTEUS application
# Date: 30/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from pathlib import Path
from typing import Dict, Union

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QStyle,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox,
    QTreeWidget,
    QTreeWidgetItem,
    QSizePolicy,
)

# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusClassTag, ProteusID, PROTEUS_NAME
from proteus.model.object import Object
from proteus.views import TREE_MENU_ICON_TYPE
from proteus.views.components.abstract_component import ProteusComponent
from proteus.controller.command_stack import Controller


# --------------------------------------------------------------------------
# Class: DeleteDialog
# Description: PyQT6 delete dialog component for the PROTEUS application
# Date: 30/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class DeleteDialog(QDialog, ProteusComponent):
    """
    Delete dialog component for the PROTEUS application. It provides a
    confirmation dialog to delete an object. It shows the object traces
    dependencies and ask the user to confirm the deletion.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 30/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        controller: Controller = None,
        element_id: ProteusID = None,
        is_document: bool = False,
        *args,
        **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Create properties to store the new document data.

        NOTE: Optional ProteusComponent parameters are omitted in the constructor,
        they can still be passed as keyword arguments.

        :param controller: Controller instance.
        :param element_id: Element id to delete.
        :param is_document: True if the element is a document.
        """
        super(DeleteDialog, self).__init__(controller, *args, **kwargs)

        self.element_id: ProteusID = element_id
        self.is_document: bool = is_document

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component
    # Date       : 30/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        # Set the dialog title
        self.setWindowTitle(self._translator.text("delete_dialog.title"))

        # Set warning system icon
        warning_icon: QIcon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MessageBoxWarning
        )
        self.setWindowIcon(warning_icon)


        # Get object name
        object: Object = self._controller.get_element(self.element_id)
        object_name: str = object.get_property(PROTEUS_NAME).value

        # Create confirmation message
        message: str = self._translator.text("delete_dialog.message", object_name)
        message_label: QLabel = QLabel(message)
        layout.addWidget(message_label)

        # Show all the object traces dependencies, it is shown in a QTreeWidget.
        # Each object pointed by another object is shown as a parent item and
        # its dependencies are shown as children items.
        traces_dependencies: Dict[
            ProteusID, set
        ] = self._controller.get_traces_dependencies(self.element_id)

        # Skipped if the object has no traces dependencies
        if traces_dependencies:
        
            # Explanation message
            message_traces: str = self._translator.text(
                "delete_dialog.traces_explanation"
            )
            message_traces_label: QLabel = QLabel(message_traces)
            message_traces_label.setWordWrap(True)
            message_traces_label.setStyleSheet("font-weight: bold; background: #eee;")
            layout.addWidget(message_traces_label)

            # Create the tree widget and set expand policy
            tree: QTreeWidget = QTreeWidget()
            tree.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            # Set header label
            header_message: str = self._translator.text("delete_dialog.tree.header")
            tree.setHeaderLabel(header_message)
            # Disable selection
            tree.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)

            # Add object item
            for object_id in traces_dependencies.keys():
                # Create tree item
                item: QTreeWidgetItem = self.create_tree_item(object_id, tree)
                # Add children items
                for child_object_id in traces_dependencies[object_id]:
                    self.create_tree_item(child_object_id, item)

            layout.addWidget(tree)

        # Create the button box -------------------------------------------------
        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )

        # Connect the button box signals to the slots
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)

        layout.addWidget(self.button_box)


    def create_tree_item(
        self, object_id: ProteusID, parent: Union[QTreeWidget, QTreeWidgetItem]
    ) -> QTreeWidgetItem:
        """
        Create a tree item for the given object id. Sets the object name
        and icon.

        :param object_id: Object id
        :param parent: Parent tree item
        :return: Tree item
        """
        # Get object instance
        object: Object = self._controller.get_element(object_id)

        # Create tree item
        item: QTreeWidgetItem = QTreeWidgetItem(parent)

        # Set object name
        object_name: str = object.get_property(PROTEUS_NAME).value
        item.setText(0, object_name)

        # Set icon
        object_class: ProteusClassTag = object.classes[-1]
        icon_path: Path = self._config.get_icon(TREE_MENU_ICON_TYPE, object_class)
        item.setIcon(0, QIcon(icon_path.as_posix()))
        return item

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Save button clicked event handler
    # Date       : 30/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_button_clicked(self) -> None:
        """
        Manage the save button clicked event. It deletes the element and
        also the references to it and its children from other objects.
        """
        # Check if the object is a document
        if self.is_document:
            self._controller.delete_document(self.element_id)
        else:
            self._controller.delete_object(self.element_id)

        # Close the form window
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Cancel button clicked event handler
    # Date       : 30/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def cancel_button_clicked(self) -> None:
        """
        Manage the cancel button clicked event. It closes the form window
        without deleting the element.
        """
        # Close the form window without saving any changes
        self.close()
        self.deleteLater()

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog
    # Description: Create a new document dialog and show it
    # Date       : 30/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(
        controller: Controller,
        element_id: ProteusID,
        is_document: bool = False,
    ) -> "DeleteDialog":
        """
        Create a delete dialog dialog and show it
        """
        dialog = DeleteDialog(
            element_id=element_id, is_document=is_document, controller=controller
        )
        dialog.exec()
        return dialog
