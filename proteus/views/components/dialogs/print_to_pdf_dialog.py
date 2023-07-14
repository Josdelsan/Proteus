# ==========================================================================
# File: print_to_pdf_dialog.py
# Description: PyQT6 print to pdf dialog component.
# Date: 14/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Union, List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import QByteArray, QMarginsF
from PyQt6.QtGui import QPageLayout, QPageSize
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QDialogButtonBox,
    QFormLayout,
    QDialog,
    QLineEdit,
    QDateEdit,
    QTextEdit,
    QCheckBox,
    QLabel,
    QFileDialog,
    QMessageBox,
    QPushButton,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.properties import Property
from proteus.views.utils.input_factory import PropertyInputFactory
from proteus.controller.command_stack import Controller
from proteus.views.utils.translator import Translator
from proteus.views.utils.state_manager import StateManager


# --------------------------------------------------------------------------
# Class: PrintToPdfDialog
# Description: Class for the PROTEUS application print to pdf dialog form.
# Date: 14/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class PrintToPdfDialog(QDialog):
    """
    Class for the PROTEUS application print to pdf dialog form. It is used
    to display a dialog form with the print to pdf options.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, controller: Controller = None, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the page object and the controller instance.
        """
        super().__init__(*args, **kwargs)
        # Controller instance
        assert isinstance(
            controller, Controller
        ), "Must provide a controller instance to the properties form dialog"
        self._controller: Controller = controller

        # Page object
        self._page: QWebEnginePage = None

        self.translator = Translator()

        self.create_page()
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
        # Helper function to select the file path
        def select_file_path():
            file_dialog: QFileDialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
            file_dialog.setDefaultSuffix("pdf")
            file_dialog.setNameFilter("PDF files (*.pdf)")
            file_dialog.selectFile(default_file_name)
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                path: str = file_dialog.selectedFiles()[0]
                if not path.endswith(".pdf"):
                    path += ".pdf"
                self.filename_input.setText(path)

        # Set the dialog title and width
        self.setWindowTitle(self.translator.text("print_to_pdf_dialog.title"))
        self.setFixedWidth(400)

        # Build default file name
        current_document = StateManager().get_current_document()
        current_view = StateManager().get_current_view()
        document: Object = self._controller.get_element(current_document)
        default_file_name: str = f"{document.get_property('name').value}-{current_view}.pdf"

        # Ask for filename and path
        filename_label = QLabel(self.translator.text("print_to_pdf_dialog.filename.label"))
        self.filename_input: QLineEdit = QLineEdit()
        self.filename_input.setEnabled(False)
        browse_button = QPushButton(
            self.translator.text("print_to_pdf_dialog.filename.browser")
        )
        browse_button.clicked.connect(select_file_path)

        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")

        # Create the buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)

        # Create the main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(filename_label)
        self.main_layout.addWidget(self.filename_input)
        self.main_layout.addWidget(self.error_label)
        self.main_layout.addWidget(browse_button)
        self.main_layout.addWidget(self.button_box)

    # ----------------------------------------------------------------------
    # Method     : create_page
    # Description: Create the page object.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_page(self) -> None:
        """
        Create the page object.
        """
        # Create the page object
        self._page = QWebEnginePage()

        # Get current application state
        current_document = StateManager().get_current_document()
        current_view = StateManager().get_current_view()

        # Generate html view
        html_view: str = self._controller.get_document_view(
            document_id=current_document, xslt_name=current_view
        )

        # Convert html to QByteArray
        # NOTE: This is done to avoid 2mb limit on setHtml method
        # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwebenginewidgets/qwebengineview.html#setHtml
        html_array: QByteArray = QByteArray(html_view.encode(encoding="utf-8"))
        self._page.setContent(html_array, "text/html")


    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Handle the cancel button clicked signal.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def cancel_button_clicked(self) -> None:
        """
        Handle the cancel button clicked signal.
        """
        # Close the dialog
        self.close()

    # ----------------------------------------------------------------------
    # Method     : accept_button_clicked
    # Description: Handle the accept button clicked signal.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def accept_button_clicked(self) -> None:
        """
        Print to pdf when the accept button is clicked.
        """
        # Validate the filename
        if self.filename_input.text() == "" or self.filename_input.text() is None:
            self.error_label.setText(
                self.translator.text("print_to_pdf_dialog.filename.error")
            )
            return

        # Define the margin values (in millimeters)
        margins: QMarginsF = QMarginsF(30, 20, 30, 20)

        # Create a QPageLayout object from the options dictionary
        page_layout = QPageLayout(QPageSize(QPageSize.PageSizeId.A4), QPageLayout.Orientation.Portrait, margins)

        # Print to pdf the current view with margins
        self._page.printToPdf(self.filename_input.text(), page_layout)

        # Show a dialog when the pdf printing is finished
        self._page.pdfPrintingFinished.connect(self.print_pdf_finished_dialog)

        # Close the dialog
        self.close()

    # ----------------------------------------------------------------------
    # Method     : print_pdf_finished_dialog
    # Description: Show a dialog when the pdf printing is finished.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def print_pdf_finished_dialog(self, filePath: str, success: bool) -> None:
        """
        Show a dialog when the pdf printing is finished.
        """
        if success:
            QMessageBox.information(
                self,
                self.translator.text("print_to_pdf_dialog.finished.dialog.title"),
                self.translator.text(
                    "print_to_pdf_dialog.finished.dialog.text", filePath
                ),
            )
        else:
            QMessageBox.critical(
                self,
                self.translator.text("print_to_pdf_dialog.finished.dialog.error.title"),
                self.translator.text("print_to_pdf_dialog.finished.dialog.error.text"),
            )

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : object_property_dialog (static)
    # Description: Handle the creation and display of the form window.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(controller: Controller):
        """
        Handle the creation and display of the form window.

        :param page: The QWebEnginePage object.
        """
        # Create the form window
        form_window = PrintToPdfDialog(controller)

        # Show the form window
        form_window.exec()
