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

from PyQt6.QtWidgets import (
    QFileDialog,
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QFrame,
    QSizePolicy,
    QDialogButtonBox,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.project import Project
from proteus.views.utils.translator import Translator
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
        """
        Class constructor, invoke the parents class constructors and create
        the component. Create properties to store the new project data.
        """
        super().__init__(parent, *args, **kwargs)

        self.translator = Translator()

        # Properties for creating a new project
        self._name: str = None
        self._path: str = None
        self._archetype_id: ProteusID = None

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
        """
        Create the component to display the new project dialog form.
        """
        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        # Set the dialog title
        self.setWindowTitle(self.translator.text("new_project_dialog.title"))

        # Create a separator widget
        separator: QFrame = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Get project archetypes
        project_archetypes: List[Project] = Controller.get_project_archetypes()
        # Create a combo box with the project archetypes
        archetype_label: QLabel = QLabel(
            self.translator.text("new_project_dialog.combobox.label")
        )
        archetype_combo: QComboBox = QComboBox()

        archetype: Project = None
        for archetype in project_archetypes:
            archetype_combo.addItem(archetype.properties["name"].value)

        # Show the archetype description
        description_label: QLabel = QLabel(
            self.translator.text("new_project_dialog.archetype.description")
        )
        description_output: QLabel = QLabel()

        # Create the name input widget
        name_label = QLabel(self.translator.text("new_project_dialog.input.name"))
        # NOTE: Temporary solution to get the name of the project
        #       in save_button_clicked method
        self.name_input: QLineEdit = QLineEdit()

        # Create the path input widget
        path_label: QLabel = QLabel(
            self.translator.text("new_project_dialog.input.path")
        )
        path_input: QLabel = QLabel()
        browse_button = QPushButton("Browse")

        # Create Save and Cancel buttons
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_button_clicked)
        button_box.rejected.connect(self.cancel_button_clicked)

        # Error message label
        self.error_label: QLabel = QLabel()
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
        description_output.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # ---------------------------------------------
        # Actions
        # ---------------------------------------------

        # Update the description when the user selects an archetype
        def update_description():
            index = archetype_combo.currentIndex()
            if index >= 0:
                archetype: Project = project_archetypes[index]
                self._archetype_id = archetype.id
                description_output.setText(archetype.properties["description"].value)

        # Update the description when the user selects an archetype
        archetype_combo.currentIndexChanged.connect(update_description)
        # Update the description for the first archetype
        update_description()

        # Open a file dialog to select the project path
        def select_project_path():
            file_dialog: QFileDialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.Directory)
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                path: str = file_dialog.selectedFiles()[0]
                path_input.setText(path)
                self._path: str = path

        # Open a file dialog when the user clicks on the browse button
        browse_button.clicked.connect(select_project_path)

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

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
        self._name: str = self.name_input.text()

        # TODO: This is a temporal solution for testing purposes.
        #       Create a proper validator and
        if self._name is None or self._name == "":
            self.error_label.setText(
                self.translator.text("new_project_dialog.error.invalid_name")
            )
            return

        if self._path is None or self._path == "":
            self.error_label.setText(
                self.translator.text("new_project_dialog.error.invalid_path")
            )
            return

        if self._archetype_id is None:
            self.error_label.setText(
                self.translator.text("new_project_dialog.error.no_archetype_selected")
            )
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

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

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
