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

from typing import Dict, Union

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
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

from proteus.model import ProteusClassTag, ProteusID, PROTEUS_NAME
from proteus.model.object import Object
from proteus.application.configuration.config import Config
from proteus.application.resources.translator import translate as _
from proteus.application.resources.icons import Icons, ProteusIconType
from proteus.views.components.dialogs.base_dialogs import ProteusDialog
from proteus.controller.command_stack import Controller


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
        self.setMinimumWidth(800)

        # Dialog layout and main widget
        layout: QVBoxLayout = QVBoxLayout()
        tab_widget: QTabWidget = QTabWidget(self)

        # Object's attributes tab ---------------------------------------------
        attributes_tab: QWidget = QWidget()
        attributes_tab_layout: QFormLayout = QFormLayout(attributes_tab)

        attributes_tab_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        attributes_tab_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Attributes inputs
        self.id_input: QLineEdit = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setText(str(self.object.id))

        self.classes_input: QLineEdit = QLineEdit()
        self.classes_input.setText(str(" ".join(self.object.classes)))

        self.acceptedChildren_input: QLineEdit = QLineEdit()
        self.acceptedChildren_input.setText(str(" ".join(self.object.acceptedChildren)))

        self.acceptedParents_input: QLineEdit = QLineEdit()
        self.acceptedParents_input.setText(str(" ".join(self.object.acceptedParents)))

        self.selectedCategory_input: QLineEdit = QLineEdit()
        selected_category: str = (
            str(self.object.selectedCategory) if self.object.selectedCategory else ""
        )
        self.selectedCategory_input.setText(selected_category)

        # Add attributes to the layout
        attributes_tab_layout.addRow(_("object.id"), self.id_input)
        attributes_tab_layout.addRow(_("object.classes"), self.classes_input)
        attributes_tab_layout.addRow(
            _("object.acceptedChildren"), self.acceptedChildren_input
        )
        attributes_tab_layout.addRow(
            _("object.acceptedParents"), self.acceptedParents_input
        )
        attributes_tab_layout.addRow(
            _("object.selectedCategory"), self.selectedCategory_input
        )

        # Direct links to objects relevant files

        self.object_file_button = QPushButton(_("object's XML file"))
        self.object_file_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(self.object.path))
        )

        self.translations_directory_button = QPushButton(
            _("Profile's translations directory")
        )
        self.translations_directory_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl.fromLocalFile(Config().profile_settings.i18n_directory.as_posix())
            )
        )

        self.icons_directory_button = QPushButton(_("Profile's icons directory"))
        self.icons_directory_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl.fromLocalFile(Config().profile_settings.icons_directory.as_posix())
            )
        )

        # Add buttons to the layout
        attributes_tab_layout.addRow(self.object_file_button)
        attributes_tab_layout.addRow(self.translations_directory_button)
        attributes_tab_layout.addRow(self.icons_directory_button)

        # Object's properties tab ---------------------------------------------
        properties_tab: QWidget = QWidget()
        properties_tab_layout: QHBoxLayout = QHBoxLayout(properties_tab)

        # Properties list
        properties_list: QTreeWidget = QTreeWidget()
        properties_list.setColumnCount(7)
        properties_list.setRootIsDecorated(False)
        properties_list.setAlternatingRowColors(True)
        properties_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Set header label
        properties_list.setHeaderLabels(
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
        for property in self.object.properties.values():
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
            properties_list.addTopLevelItem(property_list_item)

        # Create QPushButtons
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
        properties_tab_layout.addWidget(properties_list)
        properties_tab_layout.addLayout(button_layout)
        properties_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add the tabs to the tab widget -------------------------------------
        tab_widget.addTab(properties_tab, _("object.properties"))
        tab_widget.addTab(attributes_tab, _("object.attributes"))

        # Set content layout
        layout.addWidget(tab_widget)
        self.set_content_layout(layout)

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
