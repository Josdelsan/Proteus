# ==========================================================================
# File: new_view_dialog.py
# Description: PyQT6 new view dialog component for the PROTEUS application
# Date: 23/06/2023
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
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QDialogButtonBox,
)


# --------------------------------------------------------------------------
# document specific imports
# --------------------------------------------------------------------------

from proteus.views.utils.translator import Translator
from proteus.controller.command_stack import Controller


# --------------------------------------------------------------------------
# Class: NewViewDialog
# Description: PyQT6 new view dialog component for the PROTEUS application
# Date: 23/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class NewViewDialog(QDialog):
    """
    New view dialog component class for the PROTEUS application. It provides a
    dialog form to create new views from xsl templates.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 23/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self, parent=None, controller: Controller = None, *args, **kwargs
    ) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Create properties to store the new document data.
        """
        super().__init__(parent, *args, **kwargs)
        # Controller instance
        assert isinstance(
            controller, Controller
        ), "Must provide a controller instance to the new view dialog"
        self._controller: Controller = controller

        self.translator = Translator()

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
        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        # Set the dialog title
        self.setWindowTitle(self.translator.text("new_view_dialog.title"))

        # Get available xls templates to create a new view
        xls_templates: List[str] = self._controller.get_available_xslt()

        # Create a combo box with the available views
        view_label: QLabel = QLabel(
            self.translator.text("new_view_dialog.combobox.label")
        )
        view_combo: QComboBox = QComboBox()

        # Add the view names to the combo box
        view_combo.addItems(xls_templates)

        # Create view message label
        info_label: QLabel = QLabel(self.translator.text("new_view_dialog.info_text"))

        # Create Save and Cancel buttons
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Open
            | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect the buttons to the slots, combo current text is the view name
        button_box.accepted.connect(
            lambda: self.save_button_clicked(view_combo.currentText())
        )
        button_box.rejected.connect(self.cancel_button_clicked)

        # Error message label
        self.error_label: QLabel = QLabel()
        self.error_label.setObjectName("error_label")

        # Add the widgets to the layout
        layout.addWidget(view_label)
        layout.addWidget(view_combo)
        layout.addWidget(info_label)
        layout.addWidget(self.error_label)

        layout.addWidget(button_box)

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
    def save_button_clicked(self, combo_text: str) -> None:
        """
        Manage the save button clicked event. It creates a new view from the
        selected xslt template.
        """
        if combo_text is None:
            self.error_label.setText(
                self.translator.text("new_view_dialog.error.no_view_selected")
            )
            return

        if combo_text in self._controller.get_project_templates():
            self.error_label.setText(
                self.translator.text("new_view_dialog.error.duplicated_view")
            )
            return

        # Add the new template to the project and call the event
        self._controller.add_project_template(combo_text)

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
    def cancel_button_clicked(self) -> None:
        """
        Manage the cancel button clicked event. It closes the form window
        without creating any document.
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
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(controller: Controller) -> None:
        """
        Create a new document dialog and show it
        """
        dialog = NewViewDialog(controller=controller)
        dialog.exec()
