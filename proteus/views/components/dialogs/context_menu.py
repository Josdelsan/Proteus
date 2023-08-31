# ==========================================================================
# File: context_menu.py
# Description: PyQT6 context menu component.
# Date: 18/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMenu,
    QApplication,
    QTreeWidget,
    QTreeWidgetItem,
    QStyle,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.controller.command_stack import Controller
from proteus.views.utils.translator import Translator
from proteus.views.components.dialogs.property_dialog import PropertyDialog


# --------------------------------------------------------------------------
# Class: InformationDialog
# Description: Class for the PROTEUS application information dialog.
# Date: 09/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ContextMenu(QMenu):
    """
    Class for the PROTEUS application information dialog.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self, tree_widget: QTreeWidget, controller: Controller, *args, **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the page object and the controller instance.
        """
        super().__init__(*args, **kwargs)

        assert tree_widget is not None, "Tree widget cannot be None"
        assert controller is not None, "Controller cannot be None"

        # Dependencies
        self.tree_widget = tree_widget
        self._controller = controller
        self.translator = Translator()

        # Action buttons
        self.action_edit_object: QAction = None
        self.action_delete_object: QAction = None
        self.action_clone_object: QAction = None
        self.action_move_up_object: QAction = None

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the component.
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

        # Create the edit action --------------------------------------------
        self.action_edit_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.edit"), self
        )
        self.action_edit_object.triggered.connect(
            lambda: PropertyDialog.create_dialog(
                element_id=selected_item_id, controller=self._controller
            )
        )
        edit_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_FileDialogDetailedView
        )
        self.action_edit_object.setIcon(edit_icon)

        # Create the delete action ------------------------------------------
        self.action_delete_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.delete"), self
        )
        self.action_delete_object.triggered.connect(
            lambda: self._controller.delete_object(selected_item_id)
        )
        delete_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_TrashIcon
        )
        self.action_delete_object.setIcon(delete_icon)

        # Create clone action -----------------------------------------------
        self.action_clone_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.clone"), self
        )
        self.action_clone_object.triggered.connect(
            lambda: self._controller.clone_object(selected_item_id)
        )
        clone_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogApplyButton
        )
        self.action_clone_object.setIcon(clone_icon)

        # Create move up action ---------------------------------------------
        self.action_move_up_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.move_up"), self
        )
        self.action_move_up_object.triggered.connect(
            lambda: self._controller.change_object_position(
                selected_item_id, position_index - 1, parent_id
            )
        )
        move_up_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowUp
        )
        self.action_move_up_object.setIcon(move_up_icon)

        # Create move down action -------------------------------------------
        self.action_move_down_object: QAction = QAction(
            self.translator.text("document_tree.menu.action.move_down"), self
        )
        # TODO: Fix change position method to avoid using +2
        self.action_move_down_object.triggered.connect(
            lambda: self._controller.change_object_position(
                selected_item_id, position_index + 2, parent_id
            )
        )
        move_down_icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowDown
        )
        self.action_move_down_object.setIcon(move_down_icon)

        # Disable the move up action if the selected item is the first
        # item in the list
        if position_index == 0:
            self.action_move_up_object.setEnabled(False)

        # Disable the move down action if the selected item is the last
        # item in the list
        if position_index == selected_item.parent().childCount() - 1:
            self.action_move_down_object.setEnabled(False)

        # Add the actions to the context menu
        self.addAction(self.action_edit_object)
        self.addAction(self.action_delete_object)
        self.addAction(self.action_clone_object)
        self.addAction(self.action_move_up_object)
        self.addAction(self.action_move_down_object)

    # ======================================================================
    # Dialog slots methods (connected to the component signals and helpers)
    # ======================================================================

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog (static)
    # Description: Handle the creation and display of the form window.
    # Date       : 18/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(tree_widget: QTreeWidget, controller: Controller, position):
        """
        Handle the creation and display of the form window.
        """
        menu = ContextMenu(tree_widget=tree_widget, controller=controller)
        menu.exec(tree_widget.viewport().mapToGlobal(position))
