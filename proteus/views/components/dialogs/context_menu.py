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

from typing import List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QMenu,
    QTreeWidget,
    QTreeWidgetItem,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.controller.command_stack import Controller
from proteus.utils import ProteusIconType
from proteus.utils.translator import Translator
from proteus.utils.dynamic_icons import DynamicIcons
from proteus.views.components.abstract_component import ProteusComponent
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.views.components.dialogs.delete_dialog import DeleteDialog

# Module configuration
_ = Translator().text  # Translator

# --------------------------------------------------------------------------
# Class: ContextMenu
# Description: Class for the PROTEUS application context menu.
# Date: 09/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ContextMenu(QMenu, ProteusComponent):
    """
    Class for the PROTEUS application objects context menu. The menu shows
    the available actions for the selected object. It also shows a submenu
    with the available archetypes to clone in the selected object if needed.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, tree_widget: QTreeWidget, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the tree widget and initialize all the action
        buttons.

        :param tree_widget: QTreeWidget instance.
        """
        super(ContextMenu, self).__init__(*args, **kwargs)

        assert isinstance(
            tree_widget, QTreeWidget
        ), f"tree_widget must be a QTreeWidget instance, not {type(tree_widget)}"

        # Dependencies
        self.tree_widget = tree_widget

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
        selected_item_id: ProteusID = selected_item.data(1, Qt.ItemDataRole.UserRole)

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
        parent_id: ProteusID = selected_item.parent().data(1, Qt.ItemDataRole.UserRole)

        # Create the edit action --------------------------------------------
        self.action_edit_object: QAction = QAction(
            _("document_tree.menu.action.edit"), self
        )
        self.action_edit_object.triggered.connect(
            lambda: PropertyDialog.create_dialog(
                element_id=selected_item_id, controller=self._controller
            )
        )
        edit_icon = DynamicIcons().icon(ProteusIconType.App, "context-menu-edit")
        self.action_edit_object.setIcon(edit_icon)

        # Create the delete action ------------------------------------------
        self.action_delete_object: QAction = QAction(
            _("document_tree.menu.action.delete"), self
        )
        self.action_delete_object.triggered.connect(
            lambda: DeleteDialog.create_dialog(
                element_id=selected_item_id, controller=self._controller
            )
        )
        delete_icon = DynamicIcons().icon(ProteusIconType.App, "context-menu-delete")
        self.action_delete_object.setIcon(delete_icon)

        # Create clone action -----------------------------------------------
        self.action_clone_object: QAction = QAction(
            _("document_tree.menu.action.clone"), self
        )
        self.action_clone_object.triggered.connect(
            lambda: self._controller.clone_object(selected_item_id)
        )
        clone_icon = DynamicIcons().icon(ProteusIconType.App, "context-menu-clone")
        self.action_clone_object.setIcon(clone_icon)

        # Create move up action ---------------------------------------------
        self.action_move_up_object: QAction = QAction(
            _("document_tree.menu.action.move_up"), self
        )
        self.action_move_up_object.triggered.connect(
            lambda: self._controller.change_object_position(
                selected_item_id, position_index - 1, parent_id
            )
        )
        move_up_icon = DynamicIcons().icon(ProteusIconType.App, "context-menu-up")
        self.action_move_up_object.setIcon(move_up_icon)

        # Create move down action -------------------------------------------
        self.action_move_down_object: QAction = QAction(
            _("document_tree.menu.action.move_down"), self
        )
        self.action_move_down_object.triggered.connect(
            lambda: self._controller.change_object_position(
                selected_item_id, position_index + 2, parent_id
            )
        )
        move_down_icon = DynamicIcons().icon(ProteusIconType.App, "context-menu-down")
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
        self.addSeparator()
        # Insert the accepted archetypes clone menus
        accepted_archetypes: Dict[str, List[Object]] = (
            self._controller.get_accepted_object_archetypes(selected_item_id)
        )
        for archetype_class in accepted_archetypes.keys():
            # Create the archetype menu
            archetype_menu: AvailableArchetypesMenu = AvailableArchetypesMenu(
                parent_id=selected_item_id,
                class_name=archetype_class,
                archetype_list=accepted_archetypes[archetype_class],
                parent=self,
            )
            # Add the archetype menu to the context menu
            self.addMenu(archetype_menu)

        self.addSeparator()
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
    def create_dialog(
        controller: Controller, tree_widget: QTreeWidget, position: QPoint
    ) -> "ContextMenu":
        """
        Handle the creation and display of the form window.
        """
        menu = ContextMenu(tree_widget=tree_widget, controller=controller)
        menu.exec(tree_widget.viewport().mapToGlobal(position))
        return menu


# --------------------------------------------------------------------------
# Class: AvailableArchetypesMenu
# Description: Class for the PROTEUS application context menu.
# Date: 31/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class AvailableArchetypesMenu(QMenu, ProteusComponent):
    """
    Class for the PROTEUS application archetypes context menu. The menu
    shows available archetypes to clone in the selected object. Do not
    show all the posible archetypes, only the explicitly accepted by the
    selected object.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 31/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        parent_id: ProteusID,
        class_name: str,
        archetype_list: List[Object],
        *args,
        **kwargs,
    ) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the page object and the controller instance.

        :param parent_id: Parent object id.
        :param class_name: Class name.
        :param archetype_list: List of available archetypes.
        """
        super(AvailableArchetypesMenu, self).__init__(*args, **kwargs)

        # Dependencies
        self.archetype_list = archetype_list
        self.parent_id = parent_id
        self.class_name = class_name

        # Action buttons
        self.action_buttons: Dict[ProteusID, QAction] = {}

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component.
    # Date       : 31/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the component.
        """
        icon = DynamicIcons().icon(ProteusIconType.Archetype, self.class_name)

        self.setIcon(icon)
        translated_class_name: str = _(
            f"archetype.class.{self.class_name}", alternative_text=self.class_name
        )
        self.setTitle(
            _("document_tree.menu.action.add_archetype", translated_class_name)
        )

        # Create the actions
        for archetype in self.archetype_list:
            action: QAction = QAction(
                _(archetype.get_property(PROTEUS_NAME).value), self
            )
            icon = DynamicIcons().icon(ProteusIconType.Archetype, archetype.classes[-1])
            action.setIcon(icon)
            action.triggered.connect(
                lambda: self._controller.create_object(archetype.id, self.parent_id)
            )

            # Store the action button
            self.action_buttons[archetype.id] = action

        # Add the actions to the context menu
        for action in self.action_buttons.values():
            self.addAction(action)
