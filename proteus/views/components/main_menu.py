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

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QDockWidget, \
                            QToolButton, QStyle, QApplication, QSizePolicy,\
                            QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model import PROTEUS_ANY
from proteus.model.object import Object
from proteus.views.utils.decorators import subscribe_to
from proteus.controller.command_stack import Controller
from proteus.views.components.dialogs.new_project_dialog import NewProjectDialog
from proteus.views.components.dialogs.property_dialog import PropertyDialog
from proteus.views.components.dialogs.new_document_dialog import NewDocumentDialog
from proteus.views.utils import buttons
from proteus.views.utils.buttons import ArchetypeMenuButton
from proteus.views.utils.event_manager import Event


# --------------------------------------------------------------------------
# Class: MainMenu
# Description: PyQT6 main menu class for the PROTEUS application
# Date: 01/06/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
@subscribe_to([Event.STACK_CHANGED, Event.SELECT_OBJECT, Event.OPEN_PROJECT])
class MainMenu(QDockWidget):
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
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Main menu buttons that are updated
        self.save_button: QToolButton = None
        self.undo_button: QToolButton = None
        self.redo_button: QToolButton = None

        # Archetype menu buttons that are updated
        self.archetype_buttons: Dict[ArchetypeMenuButton] = {}

        # Tab widget to display app menus in different tabs
        self.tab_widget = QTabWidget()

        # Create the component
        self.create_component()

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
        # Set tittle
        self.setWindowTitle("Top menu")

        # Remove the tittle bar and set the size policy
        self.setTitleBarWidget(QWidget())
        self.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        self.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Fixed)

        # --------------------
        # Create the component
        # --------------------
        # Add the main tab
        self.add_main_tab("Project")

        # Get the object archetypes
        object_archetypes_dict: Dict[
            str, List[Object]
        ] = Controller.get_object_archetypes()
        # Create a tab for each class of object archetypes
        for class_name in object_archetypes_dict.keys():
            self.add_archetype_tab(class_name, object_archetypes_dict[class_name])

        # Set the tab widget as the main widget of the component
        self.setWidget(self.tab_widget)

    # ----------------------------------------------------------------------
    # Method     : add_main_tab
    # Description: Add the main tab to the tab widget.
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_main_tab(self, tab_name: str) -> None:
        """ """
        # Create the tab widget with a horizontal layout
        main_tab = QWidget()
        tab_layout = QHBoxLayout()

        # ---------
        # File menu
        # ---------
        # New action
        new_button = buttons.new_project_button(self)
        new_button.clicked.connect(self.new_project)
        tab_layout.addWidget(new_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Open action
        open_button = buttons.open_project_button(self)
        open_button.clicked.connect(self.open_project)
        tab_layout.addWidget(open_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Save action
        self.save_button = buttons.save_project_button(self)
        self.save_button.clicked.connect(Controller.save_project)
        tab_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Project properties action
        self.project_properties_button = buttons.project_properties_button(self)
        self.project_properties_button.clicked.connect(self.project_properties)
        tab_layout.addWidget(self.project_properties_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add document action
        self.add_document_button = buttons.add_document_button(self)
        self.add_document_button.clicked.connect(self.add_document)
        tab_layout.addWidget(self.add_document_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # ---------
        # Edit menu
        # ---------
        # Undo action
        self.undo_button = buttons.undo_button(self)
        self.undo_button.clicked.connect(Controller.undo)
        tab_layout.addWidget(self.undo_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Redo action
        self.redo_button = buttons.redo_button(self)
        self.redo_button.clicked.connect(Controller.redo)
        tab_layout.addWidget(self.redo_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # ---------------------------------------------

        # Add the main tab widget to the tab widget
        main_tab.setLayout(tab_layout)
        self.tab_widget.addTab(main_tab, tab_name)


    # ----------------------------------------------------------------------
    # Method     : add_archetype_tab
    # Description: Add a tab to the tab widget for each class of object
    #              archetypes.
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_archetype_tab(self, class_name: str, object_archetypes: List[Object]) -> None:
        """ """
        # Create the archetype tab widget with a horizontal layout
        archetypes_widget = QWidget()
        archetypes_layout = QHBoxLayout()

        # Add the archetype widgets to the tab widget
        for archetype in object_archetypes:
            # Create the archetype button
            archetype_button = ArchetypeMenuButton(archetypes_widget, archetype)

            # Add the archetype button to the archetype buttons dictionary
            self.archetype_buttons[archetype.id] = archetype_button

            # Connect the clicked signal to the clone archetype method
            archetype_button.clicked.connect(
                lambda checked, arg=archetype.id: self.clone_archetype(arg)
            )

            # Add the archetype widget to the tab widget layout
            archetypes_layout.addWidget(archetype_button)

        # Set the tab widget layout as the main widget of the tab widget
        archetypes_widget.setLayout(archetypes_layout)
        self.tab_widget.addTab(archetypes_widget, class_name)
        

    def update_component(self, event, *args, **kwargs) -> None:
        
        # Handle events
        match event:
            # ------------------------------------------------
            # Event: STACK_CHANGED
            # Description: Disable or enable main menu buttons
            # ------------------------------------------------
            case Event.STACK_CHANGED:
                can_undo = Controller._get_instance().canUndo()
                can_redo = Controller._get_instance().canRedo()
                unsaved_changes = not Controller._get_instance().isClean()

                self.undo_button.setEnabled(can_undo)
                self.redo_button.setEnabled(can_redo)
                self.save_button.setEnabled(unsaved_changes)

            # ------------------------------------------------
            # Event: SELECT_OBJECT
            # Description: Enable or disable archetype buttons
            # ------------------------------------------------
            case Event.SELECT_OBJECT:
                # Get the selected object and its accepted children
                selected_object = Controller.get_selected_object()
                accepted_children = selected_object.acceptedChildren.split()

                # Iterate over the archetype buttons
                for archetype_id in self.archetype_buttons.keys():
                    # Get the archetype button
                    archetype_button = self.archetype_buttons[archetype_id]

                    # Get the archetype
                    archetype = Controller.get_archetype_by_id(archetype_id)

                    assert type(archetype) is Object, \
                        f"Archetype {archetype_id} is not an object"
                    
                    # Get the archetype class (last class in the class hierarchy)
                    archetype_class = archetype.classes.split()[-1]

                    # Enable or disable the archetype button
                    archetype_button.setEnabled(
                        archetype_class in accepted_children
                        or PROTEUS_ANY in accepted_children
                    )
            
            # ------------------------------------------------
            # Event: OPEN_PROJECT
            # Description: Enable project properties button
            # ------------------------------------------------
            case Event.OPEN_PROJECT:
                self.project_properties_button.setEnabled(True)
                self.add_document_button.setEnabled(True)


    # ----------------------------------------------------------------------
    # Component action methods
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # Method     : new_project
    # Description: Manage the new project action, open a window to select
    #              project archetype, name and path and creates a new
    #              project.
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def new_project(self):
        """
        Manage the new project action, open a window to select project
        archetype, name and path and creates a new project.
        """
        # Create the properties form window
        new_project_window = NewProjectDialog()
        new_project_window.exec()

    # ----------------------------------------------------------------------
    # Method     : open_project
    # Description: Manage the open project action, open a project using a
    #              file dialog and loads it.
    # Date       : 16/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def open_project(self):
        """
        Manage the open project action, open a project using a file dialog
        and loads it.
        """
        # Open the file dialog
        directory_dialog = QFileDialog(self)
        directory_path = directory_dialog.getExistingDirectory(
            None, "Open Directory", ""
        )

        # Load the project from the selected directory
        if directory_path:
            try:
                Controller.load_project(project_path=directory_path)
            except Exception as e:
                proteus.logger.error(e)

                # Show an error message dialog
                error_dialog = QMessageBox()
                error_dialog.setIcon(QMessageBox.Icon.Critical)
                error_dialog.setWindowTitle("Error")
                error_dialog.setText("Error loading the project.")
                error_dialog.setInformativeText(str(e))
                error_dialog.exec()
                
    # ----------------------------------------------------------------------
    # Method     : clone_archetype
    # Description: Clone the selected archetype
    # Date       : 01/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def clone_archetype(self, archetype_id: str) -> None:
        """ """
        Controller.create_object(archetype_id=archetype_id)

    # ----------------------------------------------------------------------
    # Method     : project_properties
    # Description: Manage the project properties action, open a window to
    #              edit the project properties.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def project_properties(self):
        """
        Manage the project properties action, open a window to edit the
        project properties.
        """
        # Create the properties form window
        project = Controller.get_current_project()
        project_properties_window = PropertyDialog(project.id)
        project_properties_window.exec()

    # ----------------------------------------------------------------------
    # Method     : add_document
    # Description: Manage the add document action, open a window to select
    #              document archetype.
    # Date       : 03/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def add_document(self):
        """
        Manage the add document action, open a window to select document
        archetype.
        """
        # Create the properties form window
        add_document_window = NewDocumentDialog()
        add_document_window.exec()