# ==========================================================================
# File: main_menu.py
# Description: PyQT6 main menubar for the PROTEUS application
# Date: 01/06/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict
import logging
import traceback
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QTabWidget,
    QDockWidget,
    QToolButton,
    QFileDialog,
    QMessageBox,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_ANY
from proteus.model.object import Object
from proteus.views.components.abstract_component import ProteusComponent
from proteus.views.components.dialogs.new_project_dialog import NewProjectDialog
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.views.components.dialogs.new_document_dialog import NewDocumentDialog
from proteus.views.components.dialogs.settings_dialog import SettingsDialog
from proteus.views.components.dialogs.export_dialog import ExportDialog
from proteus.views.components.dialogs.information_dialog import InformationDialog
from proteus.views.components.dialogs.delete_dialog import DeleteDialog
from proteus.views.components.archetypes_menu_dropdown import (
    ArchetypesMenuDropdown,
)
from proteus.views import buttons
from proteus.views.buttons import ArchetypeMenuButton
from proteus.utils.state_restorer import read_state_from_file, write_state_to_file
from proteus.utils.events import (
    SelectObjectEvent,
    OpenProjectEvent,
    SaveProjectEvent,
    CurrentDocumentChangedEvent,
    RequiredSaveActionEvent,
    StackChangedEvent,
)

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: MainMenu
# Description: PyQT6 main menu class for the PROTEUS application
# Date: 01/06/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class MainMenu(QDockWidget, ProteusComponent):
    """
    Main menu component for the PROTEUS application. It is used to
    display the main option tab and object archetypes separated by
    classes separated by tabs.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent: QWidget, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors, create
        the component and connect update methods to the events.

        Manage the creation of the instace variables to store updatable
        buttons (save, undo, redo, etc.) and the tab widget to display the
        different menus.

        :param parent: Parent widget.
        """
        super(MainMenu, self).__init__(parent, *args, **kwargs)

        # Main menu buttons
        self.new_button: QToolButton = None
        self.open_button: QToolButton = None
        self.save_button: QToolButton = None
        self.undo_button: QToolButton = None
        self.redo_button: QToolButton = None
        self.project_properties_button: QToolButton = None
        self.add_document_button: QToolButton = None
        self.delete_document_button: QToolButton = None
        self.settings_button: QToolButton = None
        self.export_document_button: QToolButton = None
        self.information_button: QToolButton = None

        # Store archetype buttons by object class
        self.archetype_buttons: Dict[str, ArchetypeMenuButton] = {}

        # Tab widget to display app menus in different tabs
        self.tab_widget: QTabWidget = QTabWidget()

        # Create the component
        self.create_component()

        # Subscribe to events
        self.subscribe()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the object main tab menu component
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the object archetype tab menu component. It creates a tab for
        each class of object archetypes and a main tab for the main menu.
        """

        # ------------------
        # Component settings
        # ------------------
        # Remove the tittle bar and set fixed height to prevent resizing
        self.setTitleBarWidget(QWidget())
        self.setFixedHeight(125)

        # --------------------
        # Create the component
        # --------------------
        # Add the main tab
        self.add_main_tab(self._translator.text("main_menu.tab.home.name"))

        # Get the object archetypes
        object_archetypes_dict: Dict[
            str, Dict[str, List[Object]]
        ] = self._controller.get_first_level_object_archetypes()
        # Create a tab for each type of object archetypes
        for type_name in object_archetypes_dict.keys():
            self.add_archetype_tab(type_name, object_archetypes_dict[type_name])

        # Set the tab widget as the main widget of the component
        self.setWidget(self.tab_widget)

        log.info("Main menu component created")

    # ----------------------------------------------------------------------
    # Method     : add_main_tab
    # Description: Add the main tab to the tab widget.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_main_tab(self, tab_name: str) -> None:
        """
        Create the main menu tab and add it to the tab widget. It displays
        the main menu buttons of the PROTEUS application.

        :param tab_name: Name of the tab.
        """
        # Create the tab widget with a horizontal layout
        main_tab: QWidget = QWidget()
        tab_layout: QHBoxLayout = QHBoxLayout()

        # ---------
        # Project menu
        # ---------
        # New action
        self.new_button: QToolButton = buttons.new_project_button(self)
        self.new_button.clicked.connect(
            lambda: NewProjectDialog.create_dialog(self._controller)
        )

        # Open action
        self.open_button: QToolButton = buttons.open_project_button(self)
        self.open_button.clicked.connect(self.open_project)

        # Save action
        self.save_button: QToolButton = buttons.save_project_button(self)
        self.save_button.clicked.connect(self.save_project)

        # Project properties action
        self.project_properties_button: QToolButton = buttons.project_properties_button(
            self
        )
        self.project_properties_button.clicked.connect(
            lambda: PropertyDialog.create_dialog(
                element_id=self._controller.get_current_project().id,
                controller=self._controller,
            )
        )

        # Add the buttons to the project menu widget
        project_menu: QWidget = buttons.button_group(
            "main_menu.button_group.project",
            [
                self.new_button,
                self.open_button,
                self.save_button,
                self.project_properties_button,
            ],
        )
        tab_layout.addWidget(project_menu)

        # ---------
        # Document menu
        # ---------
        # Add document action
        self.add_document_button: QToolButton = buttons.add_document_button(self)
        self.add_document_button.clicked.connect(
            lambda: NewDocumentDialog.create_dialog(self._controller)
        )

        # Delete document action
        self.delete_document_button: QToolButton = buttons.delete_document_button(self)
        self.delete_document_button.clicked.connect(self.delete_current_document)

        # Export document action
        self.export_document_button: QToolButton = buttons.export_button(self)
        self.export_document_button.clicked.connect(
            lambda: ExportDialog.create_dialog(self._controller)
        )

        # Add the buttons to the document menu widget
        document_menu: QWidget = buttons.button_group(
            "main_menu.button_group.document",
            [
                self.add_document_button,
                self.delete_document_button,
                self.export_document_button,
            ],
        )
        tab_layout.addWidget(document_menu)

        # ---------
        # Action menu
        # ---------
        # Undo action
        self.undo_button: QToolButton = buttons.undo_button(self)
        self.undo_button.clicked.connect(self._controller.undo)

        # Redo action
        self.redo_button: QToolButton = buttons.redo_button(self)
        self.redo_button.clicked.connect(self._controller.redo)

        # Add the buttons to the action menu widget
        action_menu: QWidget = buttons.button_group(
            "main_menu.button_group.action",
            [self.undo_button, self.redo_button],
        )
        tab_layout.addWidget(action_menu)

        # ---------
        # aplication
        # ---------
        # Settings action
        self.settings_button: QToolButton = buttons.settings_button(self)
        self.settings_button.clicked.connect(
            lambda: SettingsDialog.create_dialog(self._controller)
        )

        # Information action
        self.information_button: QToolButton = buttons.info_button(self)
        self.information_button.clicked.connect(
            lambda: InformationDialog.create_dialog(controller=self._controller)
        )

        # Add the buttons to the aplication menu widget
        aplication_menu: QWidget = buttons.button_group(
            "main_menu.button_group.application",
            [self.settings_button, self.information_button],
        )

        tab_layout.addWidget(aplication_menu)

        # ---------------------------------------------

        # Spacer to justify content left
        tab_layout.addStretch()

        # Add the main tab widget to the tab widget
        main_tab.setLayout(tab_layout)
        self.tab_widget.addTab(main_tab, tab_name)

    # ----------------------------------------------------------------------
    # Method     : add_archetype_tab
    # Description: Add a tab to the tab widget for a given class of object
    #              archetypes.
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_archetype_tab(
        self, type_name: str, object_archetypes_by_class: Dict[str, List[Object]]
    ) -> None:
        """
        Add a tab to the tab widget for a given type of object archetypes.

        :param type_name: Name of the type of object archetypes.
        :param object_archetypes_by_class: Dictionary with the object
            archetypes separated by class.
        """
        # Create the tab widget with a horizontal layout
        tab_widget: QWidget = QWidget()
        tab_layout: QHBoxLayout = QHBoxLayout()

        # Create a list to store archetype buttons to create the group
        buttons_list: List[ArchetypeMenuButton] = []

        # Add the archetype widgets to the tab widget
        for object_class in object_archetypes_by_class.keys():
            # Create the archetype button
            archetype_button: ArchetypeMenuButton = ArchetypeMenuButton(
                self, object_class
            )
            # NOTE: This could be achieved using 'InstantPopup' mode, but it
            #       is a visual design decision
            archetype_button.setPopupMode(
                QToolButton.ToolButtonPopupMode.MenuButtonPopup
            )
            archetype_button.setMenu(
                ArchetypesMenuDropdown(
                    controller=self._controller,
                    archetype_list=object_archetypes_by_class[object_class],
                )
            )
            archetype_button.clicked.connect(archetype_button.showMenu)

            # Add the archetype button to the archetype buttons dictionary
            self.archetype_buttons[object_class] = archetype_button

            # Add the archetype button to the buttons list
            buttons_list.append(archetype_button)

        # Create text code for button group and bar names
        # NOTE: This is part of the internationalization system. The text
        #       code is used to retrieve the text from the translation files.
        #       This has to be dynamic because archetype tabs are created
        #       dynamically.
        tab_name_code: str = f"main_menu.tab.{type_name}.name"
        group_name_code: str = f"main_menu.button_group.archetypes.{type_name}"

        # Create the archetype button group
        archetype_menu: QWidget = buttons.button_group(group_name_code, buttons_list)
        tab_layout.addWidget(archetype_menu)

        # Spacer to justify content left
        tab_layout.addStretch()

        # Set the tab widget layout as the main widget of the tab widget
        tab_widget.setLayout(tab_layout)
        self.tab_widget.addTab(tab_widget, self._translator.text(tab_name_code))

    # ---------------------------------------------------------------------
    # Method     : subscribe
    # Description: Subscribe the component to the events.
    # Date       : 15/11/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ---------------------------------------------------------------------
    def subscribe(self) -> None:
        """
        Subscribe the component to the events.

        MainMenu component subscribes to the following events:
            - SAVE PROJECT -> update_on_save_project
            - OPEN PROJECT -> update_on_open_project
            - SELECT OBJECT -> update_on_select_object
            - STACK CHANGED -> update_on_stack_changed
            - CURRENT DOCUMENT CHANGED -> update_on_select_object
            - REQUIRED SAVE ACTION -> update_on_required_save_action
            - CURRENT DOCUMENT CHANGED -> update_on_current_document_changed
        """
        SaveProjectEvent().connect(self.update_on_save_project)
        OpenProjectEvent().connect(self.update_on_open_project)
        SelectObjectEvent().connect(self.update_on_select_object)
        StackChangedEvent().connect(self.update_on_stack_changed)
        RequiredSaveActionEvent().connect(self.update_on_required_save_action)
        CurrentDocumentChangedEvent().connect(self.update_on_current_document_changed)

    # ======================================================================
    # Component update methods (triggered by PROTEUS application events)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_on_stack_changed
    # Description: Update the state of save, undo and redo buttons when the
    #              command stack changes.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_stack_changed(self) -> None:
        """
        Update the state of save, undo and redo buttons when the command
        stack changes, enabling or disabling them depending on the state.

        Triggered by: StackChangedEvent
        """
        can_undo: bool = self._controller.stack.canUndo()
        can_redo: bool = self._controller.stack.canRedo()

        self.undo_button.setEnabled(can_undo)
        self.redo_button.setEnabled(can_redo)


    # ----------------------------------------------------------------------
    # Method     : update_on_required_save_action
    # Description: Update the state of save button when a save action is
    #              required.
    # Date       : 09/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_required_save_action(self, unsaved_changes: bool) -> None:
        """
        Update the state of save button if save action is required.

        Triggered by: RequiredSaveActionEvent
        """
        self.save_button.setEnabled(unsaved_changes)


    # ----------------------------------------------------------------------
    # Method     : update_on_save_project
    # Description: Update the state of save button when a project is saved.
    # Date       : 09/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_save_project(self) -> None:
        """
        Update the state of save button when a project is saved.

        Triggered by: SaveProjectEvent
        """
        self.save_button.setEnabled(False)


    # ----------------------------------------------------------------------
    # Method     : update_on_select_object
    # Description: Update the state of the archetype buttons when an object
    #              is selected.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_select_object(self, selected_object_id: ProteusID) -> None:
        """
        Update the state of the archetype buttons when an object is
        selected, enabling or disabling them depending on the accepted
        children of the selected object.

        Triggered by: SelectObjectEvent

        :param selected_object_id: ID of the selected object.
        """
        # If the selected object is None, disable all the archetype buttons
        if selected_object_id is None or selected_object_id == "":
            button: ArchetypeMenuButton = None
            for button in self.archetype_buttons.values():
                button.setEnabled(False)

        # If the selected object is not None, enable the archetype buttons
        # that are accepted children of the selected object
        else:
            # Get the selected object and its accepted children
            selected_object: Object = self._controller.get_element(selected_object_id)

            # Iterate over the archetype buttons
            for archetype_class in self.archetype_buttons.keys():
                # Get the archetype button
                archetype_button: ArchetypeMenuButton = self.archetype_buttons[
                    archetype_class
                ]

                enable: bool = (
                    archetype_class in selected_object.acceptedChildren
                    or PROTEUS_ANY in selected_object.acceptedChildren
                )

                # Enable or disable the archetype button
                archetype_button.setEnabled(enable)


    # ----------------------------------------------------------------------
    # Method     : update_on_open_project
    # Description: Enable the project properties and add document buttons
    #              when a project is opened.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_open_project(self) -> None:
        """
        Enable the project properties and add document buttons when a
        project is opened.

        Triggered by: OpenProjectEvent
        """
        self.project_properties_button.setEnabled(True)
        self.add_document_button.setEnabled(True)


    # ----------------------------------------------------------------------
    # Method     : update_on_current_document_changed
    # Description: Update the state of the document buttons when the
    #              current document changes.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_on_current_document_changed(self, document_id: ProteusID) -> None:
        """
        Update the state of the document buttons when the current document
        changes, enabling or disabling them depending on the state.

        Triggered by: CurrentDocumentChangedEvent

        :param document_id: ID of the current document.
        """
        # Store if there is a document open
        is_document_open: bool = document_id is not None and document_id != ""

        self.delete_document_button.setEnabled(is_document_open)
        self.export_document_button.setEnabled(is_document_open)

        # Call update_on_select_object to update the archetype buttons
        if document_id == self._state_manager.get_current_document():
            current_object_id = self._state_manager.get_current_object()
            self.update_on_select_object(current_object_id)


    # ======================================================================
    # Component slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : open_project
    # Description: Manage the open project action, open a project using a
    #              file dialog and loads it.
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def open_project(self) -> None:
        """
        Manage the open project action, open a project using a file dialog
        and loads it. If there is already a project open with unsaved
        changes, ask the user if he wants to save them before opening the
        new project.
        """
        # Open the file dialog
        directory_path: str = QFileDialog.getExistingDirectory(
            None, self._translator.text("main_menu.open_project.caption"), ""
        )

        # If a directory was selected, check if there is already a project
        # open with unsaved changes and ask the user if he wants to save
        # them before opening the new project
        if directory_path:
            # Check unsaved changes ---------------------
            # Check if the project has unsaved changes
            unsaved_changes: bool = not self._controller.stack.isClean()

            # Workaround to check when non undoable actions were not saved
            save_button_enabled: bool = False
            try:
                save_button_enabled = self.save_button.isEnabled()
            except AttributeError:
                pass

            # Unsaved changes confirmation dialog ---------------------
            if unsaved_changes or save_button_enabled:
                # Show a confirmation dialog
                confirmation_dialog = QMessageBox()
                confirmation_dialog.setIcon(QMessageBox.Icon.Warning)
                confirmation_dialog.setWindowTitle(
                    self._translator.text("main_menu.open_project.save.title")
                )
                confirmation_dialog.setText(
                    self._translator.text("main_menu.open_project.save.text")
                )
                confirmation_dialog.setStandardButtons(
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                confirmation_dialog.setDefaultButton(QMessageBox.StandardButton.No)
                # Connect save_project method to the yes button
                confirmation_dialog.button(
                    QMessageBox.StandardButton.Yes
                ).clicked.connect(self.save_project)
                confirmation_dialog.exec()

            # Project load ---------------------
            try:
                self._controller.load_project(project_path=directory_path)
                read_state_from_file(
                    Path(directory_path), self._controller, self._state_manager
                )
            except Exception as e:
                log.error(e)

                # Show an error message dialog
                error_dialog = QMessageBox()
                error_dialog.setIcon(QMessageBox.Icon.Critical)
                error_dialog.setWindowTitle(
                    self._translator.text("main_menu.open_project.error.title")
                )
                error_dialog.setText(
                    self._translator.text("main_menu.open_project.error.text")
                )

                informative_text: str = str(e)

                tb: str = "".join(traceback.format_tb(e.__traceback__))
                log.error(tb)

                error_dialog.setInformativeText(informative_text)
                error_dialog.exec()


    # ----------------------------------------------------------------------
    # Method     : save_project
    # Description: Manage the save project action, save the current project.
    # Date       : 02/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_project(self) -> None:
        """
        Manage the save project action, save the current project.
        """
        self._controller.save_project()

        # Write the state to a file
        project_path: str = self._controller.get_current_project().path
        write_state_to_file(Path(project_path).parent, self._state_manager)


    # ----------------------------------------------------------------------
    # Method     : delete_current_document
    # Description: Manage the delete current document action, delete the
    #              current document.
    # Date       : 06/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def delete_current_document(self) -> None:
        """
        Manage the delete current document action, delete the current
        document. Use a confirmation dialog to confirm the action.
        """
        # Get the current document
        document_id: ProteusID = self._state_manager.get_current_document()

        # Assert that the current document is not None
        assert (
            document_id is not None and document_id != ""
        ), "Current document is None or empty"

        # Create the delete dialog
        DeleteDialog.create_dialog(
            element_id=document_id,
            is_document=True,
            controller=self._controller,
        )
