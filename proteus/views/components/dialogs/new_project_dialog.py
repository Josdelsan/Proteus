# ==========================================================================
# File: new_project_dialog.py
# Description: PyQT6 new project component for the PROTEUS application
# Date: 28/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QLabel, \
                            QComboBox, QLineEdit, QPushButton, QFrame, \
                            QSizePolicy, QDialogButtonBox


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.project import Project
from proteus.controller.command_stack import Controller

# --------------------------------------------------------------------------
# Class: NewProject
# Description: PyQT6 new project component for the PROTEUS application
# Date: 28/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class NewProjectDialog(QDialog):
    """
    New project component class for the PROTEUS application. It provides a
    dialog form to create new projects from project archetypes.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Properties for creating a new project
        self._name = None
        self._path = None
        self._archetype_id = None

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component
    # Date       : 28/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a separator widget
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Get project archetypes
        project_archetypes : List[Project] = Controller.get_project_archetypes()
        # Create a combo box with the project archetypes
        archetype_label = QLabel("Select Project Archetype:")
        archetype_combo = QComboBox()
        for archetype in project_archetypes:
            archetype_combo.addItem(archetype.properties["name"].value)
        

        # Show the archetype description
        description_label = QLabel("Project Description:")
        description_output = QLabel()

        # Create the name input widget
        name_label = QLabel("Enter Project Name:")
        # NOTE: Temporary solution to get the name of the project
        #       in save_button_clicked method
        self.name_input = QLineEdit()

        # Create the path input widget
        path_label = QLabel("Select Project Path:")
        path_input = QLabel()
        browse_button = QPushButton("Browse")

        # Create Save and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.save_button_clicked)
        button_box.rejected.connect(self.cancel_button_clicked)

        # Error message label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        # Add the widgets to the layout
        layout.addWidget(archetype_label)
        layout.addWidget(archetype_combo)
        layout.addWidget(description_label)
        layout.addWidget(description_output)
        layout.addWidget(separator)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(path_label)
        layout.addWidget(path_input)
        layout.addWidget(browse_button)
        layout.addWidget(self.error_label)

        layout.addWidget(button_box)

        # Set fixed width for the window
        self.setFixedWidth(400)
        # Allow vertical expansion for the description
        description_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # ---------------------------------------------
        # Actions
        # ---------------------------------------------

        # Update the description when the user selects an archetype
        def update_description():
            index = archetype_combo.currentIndex()
            if index >= 0:
                archetype = project_archetypes[index]
                self._archetype_id = archetype.id
                description_output.setText(archetype.properties["description"].value)

        # Update the description when the user selects an archetype
        archetype_combo.currentIndexChanged.connect(update_description)
        # Update the description for the first archetype
        update_description()

        # Open a file dialog to select the project path
        def select_project_path():
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.Directory)
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                path = file_dialog.selectedFiles()[0]
                path_input.setText(path)
                self._path = path

        # Open a file dialog when the user clicks on the browse button
        browse_button.clicked.connect(select_project_path)

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Save button clicked event handler
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    # TODO: Validate if path exists before creating the project
    def save_button_clicked(self):
         
        # Get the project name
        self._name = self.name_input.text()

        # TODO: This is a temporal solution for testing purposes.
        #       Create a proper validator and
        if self._name is None or self._name == "":
            self.error_label.setText("Please enter a valid project name")
            return
        
        if self._path is None or self._path == "":
            self.error_label.setText("Please select a valid project path")
            return
        
        if self._archetype_id is None:
            self.error_label.setText("Please select a valid project archetype")
            return
        
        # Create the project
        Controller.create_project(self._archetype_id, self._name, self._path)

        # Close the form window
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Cancel button clicked event handler
    # Date       : 29/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def cancel_button_clicked(self):
        """
        Manage the cancel button clicked event. It closes the form window
        without creating any project.
        """
        # Close the form window without saving any changes
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : create_dialog (static)
    # Description: Create a new project dialog and show it
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog() -> None:
        """
        Create a new project dialog and show it
        """
        dialog = NewProjectDialog()
        dialog.exec()