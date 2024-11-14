# ==========================================================================
# File: impact_analysis.py
# Description: PyQT6 impact analysis window component for the PROTEUS application
# Date: 31/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Set
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QSplitter,
    QLabel,
    QPushButton,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import (
    PROTEUS_DEPENDENCY,
    ProteusID,
)
from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.views.forms.items.objects_list_edit import ImpactAnalysisObjectsListEdit
from proteus.views.components.dialogs.base_dialogs import ProteusDialog
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.controller.command_stack import Controller
from proteus.application.resources.translator import translate as _
from proteus.application.resources.icons import Icons, ProteusIconType
from proteus.application.events import (
    AddDocumentEvent,
    DeleteDocumentEvent,
    AddObjectEvent,
    DeleteObjectEvent,
    ModifyObjectEvent,
)


# Module configuration
log = logging.getLogger(__name__)  # Logger


# --------------------------------------------------------------------------
# Class: ImpactAnalysisWindow
# Description: PyQT6 impact analysis window component for the PROTEUS application
# Date: 31/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ImpactAnalysisWindow(ProteusDialog):

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Class constructor
    # Date: 11/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kargs):
        super(ImpactAnalysisWindow, self).__init__(*args, **kargs)

        # Variables
        self.analyzed_objects: ImpactAnalysisObjectsListEdit
        self.affected_objects: QListWidget
        self.navigate_button: QPushButton

        self.create_component()
        self.subscribe()

    # --------------------------------------------------------------------------
    # Method: create_component
    # Description: Create the impact analysis window component
    # Date: 11/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def create_component(self):
        self.setWindowTitle("Impact Analysis")
        self.resize(500, 400)

        # Create the object picker ----------------------------------------------------------
        self.analyzed_objects = ImpactAnalysisObjectsListEdit(
            self._controller, candidates=self._calculate_candidates()
        )

        # Create the list widget to show the impact analysis --------------------------------
        self.affected_objects = QListWidget()
        self.affected_objects.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.navigate_button: QPushButton = QPushButton()
        navigate_button_icon = Icons().icon(ProteusIconType.App, "navigate-to-object")
        self.navigate_button.setIcon(navigate_button_icon)
        self.navigate_button.setEnabled(False)

        self.edit_button: QPushButton = QPushButton()
        edit_button_icon = Icons().icon(ProteusIconType.App, "context-menu-edit")
        self.edit_button.setIcon(edit_button_icon)
        self.edit_button.setEnabled(False)

        # Create a layout for the buttons (vertically stacked)
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(self.navigate_button)
        button_layout.addWidget(self.edit_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        affected_objects_layout = QHBoxLayout()
        affected_objects_layout.setContentsMargins(0, 0, 0, 0)
        affected_objects_layout.addWidget(self.affected_objects)
        affected_objects_layout.addLayout(button_layout)
        affected_objects_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create the splitter ----------------------------------------------------------------
        analyzed_objects_label: QLabel = QLabel(_("Analyzed objects:"))
        affected_objects_label: QLabel = QLabel(_("Affected objects:"))

        analyzed_objects_widget: QWidget = QWidget()
        analyzed_objects_widget_layout: QVBoxLayout = QVBoxLayout()
        analyzed_objects_widget_layout.addWidget(analyzed_objects_label)
        analyzed_objects_widget_layout.addWidget(self.analyzed_objects)
        analyzed_objects_widget.setLayout(analyzed_objects_widget_layout)

        affected_objects_widget: QWidget = QWidget()
        affected_objects_widget_layout: QVBoxLayout = QVBoxLayout()
        affected_objects_widget_layout.addWidget(affected_objects_label)
        affected_objects_widget_layout.addLayout(affected_objects_layout)
        affected_objects_widget.setLayout(affected_objects_widget_layout)

        splitter = QSplitter()
        splitter.setChildrenCollapsible(False)
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        splitter.addWidget(analyzed_objects_widget)
        splitter.addWidget(affected_objects_widget)
        splitter.setSizes([200, 400])

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(splitter)

        self.set_content_layout(layout)

        # Set the buttons
        self.reject_button.setText(_("dialog.close_button"))
        self.accept_button.setHidden(True)

        # Connect signals --------------------------------------------------------------------
        self.analyzed_objects.itemsChanged.connect(self.update_affected_objects)

        # Double-click navigation and button navigation
        self.analyzed_objects.item_list.itemDoubleClicked.connect(self.select_object_on_double_click)
        self.affected_objects.itemDoubleClicked.connect(self.select_object_on_double_click)

        # Buttons
        self.navigate_button.clicked.connect(self.navigate_to_current_affected_object)
        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.affected_objects.currentItemChanged.connect(self.update_affected_objects_buttons)

    # --------------------------------------------------------------------------
    # Method: subscribe
    # Date: 11/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def subscribe(self) -> None:
        """
        Subscribe to the PROTEUS application events.

        ImpactAnalysisWindow is subscribed to the following events:
            - ADD OBJECT -> update_on_add_document_or_object
            - DELETE OBJECT -> update_on_delete_document_or_object
            - ADD DOCUMENT -> update_on_add_document_or_object
            - DELETE DOCUMENT -> update_on_delete_document_or_object
            - MODIFY OBJECT -> update_on_modify_object
        """
        AddDocumentEvent().connect(self.update_on_add_document_or_object)
        DeleteDocumentEvent().connect(self.update_on_delete_document_or_object)
        AddObjectEvent().connect(self.update_on_add_document_or_object)
        DeleteObjectEvent().connect(self.update_on_delete_document_or_object)
        ModifyObjectEvent().connect(self.update_on_modify_object)

    # --------------------------------------------------------------------------
    # Method: update_affected_objects
    # Date: 11/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_affected_objects(self) -> None:
        """
        Update the affected objects list when the analyzed objects list changes.
        """
        self.affected_objects.clear()
        analyzed_objects_ids = self.analyzed_objects.items()
        affected_objects: Set[Object] = set()

        for analyzed_object_id in analyzed_objects_ids:
            analyzed_object: Object = self._controller.get_element(analyzed_object_id)
            _affected_objects = self._calculate_affected_objects(
                analyzed_object_id, set([analyzed_object])
            )
            affected_objects.update(_affected_objects)

        for affected_object in affected_objects:
            # Skip the analyzed objects
            if affected_object.id in analyzed_objects_ids:
                continue

            item = QListWidgetItem()

            # Re-use the tree_item_setup function from the objects list edit
            self.analyzed_objects.list_item_setup(item, affected_object)
            self.affected_objects.addItem(item)

    # --------------------------------------------------------------------------
    # Method: _calculate_affected_objects
    # Date: 11/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _calculate_affected_objects(
        self, analyzed_object: ProteusID, affected_objects: Set[Object] = set()
    ) -> Set[Object]:
        """
        Calculate the affected objects in case of a change in the analyzed object.
        It only considers the PROTEUS_DEPENDENCY traces.

        :param ProteusID analyzed_object: ID of the object to analyze
        :param Set[Object] affected_objects: set of already affected objects, defaults to set()
        :return Set[Object]: set of affected objects
        """

        object_pointers = self._controller.get_objects_pointing_to(analyzed_object)
        for object_id in object_pointers:

            if object_id in [obj.id for obj in affected_objects]:
                continue

            object = self._controller.get_element(object_id)

            if object.state == ProteusState.DEAD:
                continue

            # Check if it is pointing from a PROTEUS_DEPENDENCY trace
            traces = object.get_traces()
            for trace in traces:
                if trace.type == PROTEUS_DEPENDENCY and analyzed_object in trace.value:
                    affected_objects.add(object)
                    new_affected_objects = self._calculate_affected_objects(
                        object.id, affected_objects
                    )

                    affected_objects.update(new_affected_objects)
                    break

        return affected_objects

    # --------------------------------------------------------------------------
    # Method: _calculate_candidates
    # Date: 12/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def _calculate_candidates(self) -> List[ProteusID]:
        """
        Calculate all candidate objects for the impact analysis. It returns
        all non-dead objects in the project. Include the documents (Object class).

        :return List[Object]: All candidate objects for the impact analysis
        """
        # Get all objects in the project
        project = self._controller.get_current_project()
        all_objects = project.get_descendants_recursively(ignore_dead_children=True)
        all_objects.remove(project)
        all_objects_ids = [obj.id for obj in all_objects]
        return all_objects_ids

    # ==========================================================================
    # Connected to signals
    # ==========================================================================

    def select_object_on_double_click(self, item: QListWidgetItem) -> None:
        """
        Select the object in the PROTEUS application when the user double-clicks
        on an object in the affected objects list.
        """
        object_id = item.data(Qt.ItemDataRole.UserRole)
        object: Object = self._controller.get_element(object_id)
        document: Object = object.get_document()
        if document.id != self._state_manager.get_current_document():
            self._state_manager.set_current_document(document.id)

        self._state_manager.set_current_object(object.id, document.id)

    def navigate_to_current_affected_object(self) -> None:
        """
        Get information from the current affected object and navigate to it.
        """
        current_item = self.affected_objects.currentItem()
        if current_item:
            self.select_object_on_double_click(current_item)

    def edit_button_clicked(self) -> None:
        """
        Open the property dialog for the selected object
        """
        current_item = self.affected_objects.currentItem()
        if current_item:
            object_id = current_item.data(Qt.ItemDataRole.UserRole)
            PropertyDialog.create_dialog(self._controller, object_id)

    def update_affected_objects_buttons(self) -> None:
        """
        Update the navigation button based on the current selection.
        """
        current_item = self.affected_objects.currentItem()
        enabled = current_item is not None

        self.navigate_button.setEnabled(enabled)
        self.edit_button.setEnabled(enabled)

    # ==========================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: update_on_add_document_or_object
    # Date: 12/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_on_add_document_or_object(self, _) -> None:
        """
        Update the affected objects and the candidates list when a document or
        object is added.
        """
        self.analyzed_objects.candidates = self._calculate_candidates()
        self.update_affected_objects()

    # --------------------------------------------------------------------------
    # Method: update_on_delete_document_or_object
    # Date: 12/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_on_delete_document_or_object(self, _) -> None:
        """
        Update the affected objects, the candidates list and the analyzed objects
        list when a document or object is deleted.
        """
        # Remove DEAD objects from the analyzed objects list
        elements: List[Object] = []
        for element_id in self.analyzed_objects.items():
            element = self._controller.get_element(element_id)
            if element.state == ProteusState.DEAD:
                continue

            elements.append(element)

        self.analyzed_objects.setItems(elements)

        # Update the candidates list and the affected objects
        self.analyzed_objects.candidates = self._calculate_candidates()
        self.update_affected_objects()

    # --------------------------------------------------------------------------
    # Method: update_on_modify_object
    # Date: 12/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_on_modify_object(self, _) -> None:
        """
        Update the affected objects when an object is modified and update the
        analyzed objects representation.
        """
        # Update the analyzed objects representation
        for i in range(self.analyzed_objects.item_list.count()):
            item: QListWidgetItem = self.analyzed_objects.item_list.item(i)
            object_id = item.data(Qt.ItemDataRole.UserRole)
            self.analyzed_objects.list_item_setup(item, object_id)

        self.affected_objects.setCurrentItem(None)

        # Update the affected objects
        self.update_affected_objects()

    # ==========================================================================
    # Static methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Method: show_dialog
    # Date: 11/11/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @staticmethod
    def show_dialog(parent: QObject, controller: Controller) -> "ImpactAnalysisWindow":
        """
        Show the impact analysis non-modal dialog.

        :param QObject parent: Necessary QObject parent for dialog life cycle management
        :param Controller controller: Controller instance
        :return ImpactAnalysisWindow: ImpactAnalysisWindow instance
        """
        dialog = ImpactAnalysisWindow(parent=parent, controller=controller)
        dialog.show()
        return dialog
