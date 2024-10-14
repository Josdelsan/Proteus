# ==========================================================================
# File: model_editor.py
# Description: module for the PROTEUS raw model editor dialog
# Date: 10/10/2024
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

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QLineEdit,
    QSizePolicy,
)

# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.model.properties import Property
from proteus.application.configuration.config import Config
from proteus.application.resources.translator import translate as _
from proteus.application.resources.icons import Icons, ProteusIconType
from proteus.application.events import ModifyObjectEvent, RequiredSaveActionEvent
from proteus.views.components.dialogs.base_dialogs import ProteusDialog, MessageBox
from proteus.controller.command_stack import Controller

# Constants

XML_PROBLEMATIC_CHARS = ["&", '"', "<", ">"]


# --------------------------------------------------------------------------
# Class: RawObjectEditor
# Description: PyQT6 raw model editor dialog component for the PROTEUS application
# Date: 10/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class RawObjectEditor(ProteusDialog):
    """
    The raw object editor dialog component for the PROTEUS application. It provides an
    interface to directly edit an object's properties and attributed without the need
    of manually editing its XML file.

    This feature is intended for advanced users (mostly developers) who need just in-time
    model editing capabilities. This class is located in the front-end side of the application
    but it performs some python Object instance manipulation in order to update the object
    during application runtime.

    WARNING:

    Due to runtime model manipulation, data consistency is not guaranteed. The user should
    be aware of data integrity issues (modifying accepted parents, children, classes, etc.).

    Modifying an object's properties and/or attributes will clear the command stack. These
    modifications are not undoable. It is assumed this is a developer's tool and the application
    will not be used in a production environment if this dialog is used.

    This class is hidden by default and can be enabled by setting the 'raw_model_editor' flag
    in the application configuration file.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 10/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, object_id: ProteusID, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component.
        """
        super(RawObjectEditor, self).__init__(*args, **kwargs)

        self.object: Object = self._controller.get_element(object_id)

        # Copy the object properties to avoid modifying the original object until
        # the user confirms the changes
        self.properties: Dict[str, Property] = self.object.properties.copy()

        # Input widgets and its error labels
        self.id_input: QLineEdit
        self.id_input_error_label: QLabel

        self.classes_input: QLineEdit
        self.classes_input_error_label: QLabel

        self.acceptedChildren_input: QLineEdit
        self.acceptedChildren_input_error_label: QLabel

        self.acceptedParents_input: QLineEdit
        self.acceptedParents_input_error_label: QLabel

        # Properties list and buttons
        self.properties_list: QTreeWidget
        self.properties_list_error_label: QLabel

        self.edit_button: QPushButton
        self.add_button: QPushButton
        self.remove_button: QPushButton
        self.move_up_button: QPushButton
        self.move_down_button: QPushButton

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component
    # Date       : 10/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the component
        """

        # Dialog size
        self.setMinimumWidth(900)

        # Dialog layout and main widget
        layout: QVBoxLayout = QVBoxLayout()
        tab_widget: QTabWidget = QTabWidget(self)

        # Create the tabs ----------------------------------------------------
        attributes_tab: QWidget = self._create_attributes_tab()
        properties_tab: QWidget = self._create_properties_tab()

        # Add the tabs to the tab widget -------------------------------------
        tab_widget.addTab(properties_tab, _("object.properties"))
        tab_widget.addTab(attributes_tab, _("object.attributes"))

        # Set content layout
        layout.addWidget(tab_widget)
        self.set_content_layout(layout)

        # Connect signals and slots ------------------------------------------
        self.properties_list.itemPressed.connect(self.item_pressed_event)
        self.item_pressed_event(None, 0)

        self.move_up_button.clicked.connect(lambda: self.move_button_clicked(True))
        self.move_down_button.clicked.connect(lambda: self.move_button_clicked(False))
        self.remove_button.clicked.connect(self.remove_button_clicked)

        self.accept_button.setText(_("dialog.save_button"))
        self.accept_button.clicked.connect(self.save_button_clicked)
        self.reject_button.clicked.connect(self.cancel_button_clicked)

    # ----------------------------------------------------------------------
    # Method     : _create_properties_tab
    # Description: Create the properties tab
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _create_properties_tab(self) -> QWidget:
        """
        Create the properties tab
        """
        properties_tab: QWidget = QWidget()
        properties_tab_layout: QHBoxLayout = QHBoxLayout(properties_tab)

        # Properties list ----------------------------------------------------
        self.properties_list: QTreeWidget = QTreeWidget()
        self.properties_list.setColumnCount(7)
        self.properties_list.setRootIsDecorated(False)
        self.properties_list.setAlternatingRowColors(True)
        self.properties_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.properties_list_error_label: QLabel = create_error_label()

        # Set header label
        self.properties_list.setHeaderLabels(
            [
                _("name"),
                _("type"),
                _("category"),
                _("required"),
                _("inmutable"),
                _("tooltip"),
                _("value"),
            ]
        )

        # Add properties to the list
        self._update_properties_list()

        # Create QPushButtons ------------------------------------------------
        self.edit_button = QPushButton()
        edit_button_icon = Icons().icon(ProteusIconType.App, "context-menu-edit")
        self.edit_button.setIcon(edit_button_icon)

        self.add_button = QPushButton()
        add_button_icon = Icons().icon(ProteusIconType.App, "add_trace_icon")
        self.add_button.setIcon(add_button_icon)

        self.remove_button = QPushButton()
        self.remove_button.setEnabled(False)
        remove_button_icon = Icons().icon(ProteusIconType.App, "remove_trace_icon")
        self.remove_button.setIcon(remove_button_icon)

        self.move_up_button = QPushButton()
        move_up_button_icon = Icons().icon(ProteusIconType.App, "context-menu-up")
        self.move_up_button.setIcon(move_up_button_icon)

        self.move_down_button = QPushButton()
        move_down_button_icon = Icons().icon(ProteusIconType.App, "context-menu-down")
        self.move_down_button.setIcon(move_down_button_icon)

        # Create a layout for the buttons (vertically stacked)
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.move_up_button)
        button_layout.addWidget(self.move_down_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Configure layout for the QTreeWidget and button layout (horizontally arranged)
        properties_tab_layout.setContentsMargins(0, 0, 0, 0)
        properties_tab_layout.addWidget(self.properties_list)
        properties_tab_layout.addLayout(button_layout)
        properties_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return properties_tab

    # ----------------------------------------------------------------------
    # Method     : _update_properties_list
    # Description: Populate the properties list with the object properties
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _update_properties_list(self) -> None:
        self.properties_list.clear()

        for property in self.properties.values():
            property_list_item: QTreeWidgetItem = QTreeWidgetItem(
                [
                    property.name,
                    str(type(property).__name__),
                    property.category,
                    str(property.required),
                    str(property.inmutable),
                    property.tooltip,
                    str(property.value) if property.value else "",
                ]
            )
            property_list_item.setData(0, Qt.ItemDataRole.UserRole, property.name)
            self.properties_list.addTopLevelItem(property_list_item)

    # ----------------------------------------------------------------------
    # Method     : create_attributes_tab
    # Description: Create the attributes tab
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _create_attributes_tab(self) -> QWidget:
        """
        Create the attributes tab
        """
        attributes_tab: QWidget = QWidget()
        attributes_tab_layout: QFormLayout = QFormLayout(attributes_tab)

        attributes_tab_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        attributes_tab_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Attributes inputs --------------------------------------------------
        self.id_input: QLineEdit = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setText(str(self.object.id))
        self.id_input_error_label: QLabel = create_error_label()

        self.classes_input: QLineEdit = QLineEdit()
        self.classes_input.setText(str(" ".join(self.object.classes)))
        self.classes_input_error_label: QLabel = create_error_label()

        self.acceptedChildren_input: QLineEdit = QLineEdit()
        self.acceptedChildren_input.setText(str(" ".join(self.object.acceptedChildren)))
        self.acceptedChildren_input_error_label: QLabel = create_error_label()

        self.acceptedParents_input: QLineEdit = QLineEdit()
        self.acceptedParents_input.setText(str(" ".join(self.object.acceptedParents)))
        self.acceptedParents_input_error_label: QLabel = create_error_label()

        self.selectedCategory_input: QLineEdit = QLineEdit()
        selected_category: str = (
            str(self.object.selectedCategory) if self.object.selectedCategory else ""
        )
        self.selectedCategory_input.setText(selected_category)
        self.selectedCategory_input_error_label: QLabel = create_error_label()

        # Add attributes to the layout
        attributes_tab_layout.addRow(_("object.id"), self.id_input)
        attributes_tab_layout.addWidget(self.id_input_error_label)

        attributes_tab_layout.addRow(_("object.classes"), self.classes_input)
        attributes_tab_layout.addWidget(self.classes_input_error_label)

        attributes_tab_layout.addRow(
            _("object.acceptedChildren"), self.acceptedChildren_input
        )
        attributes_tab_layout.addWidget(self.acceptedChildren_input_error_label)

        attributes_tab_layout.addRow(
            _("object.acceptedParents"), self.acceptedParents_input
        )
        attributes_tab_layout.addWidget(self.acceptedParents_input_error_label)

        attributes_tab_layout.addRow(
            _("object.selectedCategory"), self.selectedCategory_input
        )
        attributes_tab_layout.addWidget(self.selectedCategory_input_error_label)

        # Direct links to objects relevant files -----------------------------

        object_file_button = QPushButton(_("object's XML file"))
        object_file_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(self.object.path))
        )

        translations_directory_button = QPushButton(
            _("Profile's translations directory")
        )
        translations_directory_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl.fromLocalFile(Config().profile_settings.i18n_directory.as_posix())
            )
        )

        icons_directory_button = QPushButton(_("Profile's icons directory"))
        icons_directory_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl.fromLocalFile(Config().profile_settings.icons_directory.as_posix())
            )
        )

        # Add buttons to the layout
        attributes_tab_layout.addRow(object_file_button)
        attributes_tab_layout.addRow(translations_directory_button)
        attributes_tab_layout.addRow(icons_directory_button)

        return attributes_tab

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : item_pressed_event
    # Description: Manage the item pressed event. It enables or disables
    #              the remove button, move up and move down buttons.
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def item_pressed_event(self, item: QTreeWidgetItem, column: int) -> None:
        """
        Manage the item pressed event. It enables or disables the remove
        button, move up and move down buttons.
        """
        # If no item is selected, disable all buttons but the add button
        if item is None:
            self.properties_list.setCurrentItem(None)
            self.remove_button.setEnabled(False)
            self.move_up_button.setEnabled(False)
            self.move_down_button.setEnabled(False)
            self.edit_button.setEnabled(False)
            return

        property_name: str = item.data(0, Qt.ItemDataRole.UserRole)
        property_index: int = self.properties_list.indexOfTopLevelItem(item)

        # Disable the remove button if is a PROTEUS_NAME property
        self.remove_button.setEnabled(property_name != PROTEUS_NAME)

        # Disable the move up button if is the first item
        self.move_up_button.setEnabled(property_index > 0)

        # Disable the move down button if is the last item
        self.move_down_button.setEnabled(property_index < self.properties_list.topLevelItemCount() - 1)

        # Enable the edit button
        self.edit_button.setEnabled(True)

    # ----------------------------------------------------------------------
    # Method     : move_up_button_clicked
    # Description: Manage the move up button clicked event. It moves the
    #              selected property up in the list.
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def move_button_clicked(self, move_up: bool):
        """
        Manage the move up button clicked event. It moves the selected
        property up in the list.
        """
        offset: int = -1 if move_up else 1

        item: QTreeWidgetItem = self.properties_list.currentItem()
        item_index: int = self.properties_list.indexOfTopLevelItem(item)

        # Update the properties dictionary ----------------------------------
        property_name: str = item.data(0, Qt.ItemDataRole.UserRole)

        # Remove from current dictionary
        dictionary_positions = list(self.properties.keys())
        dictionary_positions.remove(property_name)
        dictionary_positions.insert(item_index + offset, property_name)

        # Create a new dictionary with the new order
        self.properties = {
            key: self.properties[key] for key in dictionary_positions
        }

        # Update the properties list based on the new dictionary order
        self._update_properties_list()

        # Item pressed event to update the buttons state
        new_item = self.properties_list.topLevelItem(item_index + offset)
        self.properties_list.setCurrentItem(new_item)
        self.item_pressed_event(new_item, 0)

    # ----------------------------------------------------------------------
    # Method     : remove_button_clicked
    # Description: Manage the delete button clicked event. It removes the
    #              selected property from the list.
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def remove_button_clicked(self):
        """
        Manage the delete button clicked event. It removes the selected
        property from the list.
        """
        item: QTreeWidgetItem = self.properties_list.currentItem()
        property_name: str = item.data(0, Qt.ItemDataRole.UserRole)

        if property_name == PROTEUS_NAME:
            MessageBox.critical(
                _("error.cannot_delete_name_property"),
                _("error.cannot_delete_name_property_message"),
            )
            return
        
        confirmation_dialog = MessageBox.question(
            _("dialog.delete_property"),
            _("dialog.delete_property_message", property_name),
        )

        if confirmation_dialog == MessageBox.StandardButton.Yes:
            # Remove the property from the dictionary
            self.properties.pop(property_name)

            # Update the properties list
            self._update_properties_list()

            # Item pressed event to update the buttons state
            self.item_pressed_event(None, 0)

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Manage the save button clicked event. It saves the
    #              changes made to the object properties and attributes.
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_button_clicked(self):
        """
        Manage the save button clicked event. It saves the changes made to
        the object properties and attributes.
        """
        form_has_errors: bool = False

        # Attributes validation ---------------------------------------------
        def attribute_input_has_errors(input: QLineEdit, error_lable: QLabel) -> bool:
            if not input.text() or any(
                char in input.text() for char in XML_PROBLEMATIC_CHARS
            ):
                error_lable.setText(_("error.required_field"))
                error_lable.show()
                return True
            else:
                error_lable.hide()
                return False

        form_has_errors = (
            attribute_input_has_errors(
                self.classes_input, self.classes_input_error_label
            )
            or attribute_input_has_errors(
                self.acceptedChildren_input, self.acceptedChildren_input_error_label
            )
            or attribute_input_has_errors(
                self.acceptedParents_input, self.acceptedParents_input_error_label
            )
        )

        # Selected category cannot include spaces but may be empty
        selected_category: str = self.selectedCategory_input.text()
        if " " in selected_category or any(
            char in selected_category for char in XML_PROBLEMATIC_CHARS
        ):
            self.selectedCategory_input_error_label.setText(_("error.invalid_category"))
            self.selectedCategory_input_error_label.show()
            form_has_errors = True

        # Properties validation ---------------------------------------------
        # Properties are validated in their own dialog so we just check if
        # PROTEUS_NAME property is present
        if PROTEUS_NAME not in self.properties:
            self.properties_list_error_label.setText(_("error.missing_name_property"))
            self.properties_list_error_label.show()
            form_has_errors = True
        else:
            self.properties_list_error_label.hide()

        # Final handling and object update ----------------------------------
        if form_has_errors:
            return

        # Update the object attributes
        self.object.classes = self.classes_input.text().split()
        self.object.acceptedChildren = self.acceptedChildren_input.text().split()
        self.object.acceptedParents = self.acceptedParents_input.text().split()
        self.object.selectedCategory = self.selectedCategory_input.text()

        # Update the object properties
        self.object.properties = self.properties

        # Mark the object as modified
        self.object.state = ProteusState.DIRTY

        # NOTE: It is neccesary to clear the command stack to avoid inconsistencies
        # since the object model is being modified directly.
        self._controller.stack.clear()

        # Call modify object event to update the object in the front-end
        # and force a save action
        ModifyObjectEvent().notify(object_id=self.object.id)
        RequiredSaveActionEvent().notify(save_required=True)

        # Close the form window
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Manage the cancel button clicked event. It closes the
    #              form window without saving any changes.
    # Date       : 11/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def cancel_button_clicked(self):
        """
        Manage the cancel button clicked event. It closes the form window
        without saving any changes.
        """
        # Close the form window without saving any changes
        self.close()
        self.deleteLater()

    # ======================================================================
    # Dialog static methods (create and show)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog (static)
    # Description: Handle the creation and display of the window.
    # Date       : 10/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(
        controller: Controller, object_id: ProteusID
    ) -> "RawObjectEditor":
        """
        Handle the creation and display of the form window.

        :param controller: A Controller instance.
        :param object_id: The object's identifier.
        """
        dialog = RawObjectEditor(object_id=object_id, controller=controller)
        dialog.exec()
        return dialog


def create_error_label() -> QLabel:
    """
    Create an error label
    """
    error_label: QLabel = QLabel()
    error_label.setObjectName("error_label")
    error_label.setWordWrap(True)
    error_label.hide()
    return error_label
