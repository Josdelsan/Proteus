# ==========================================================================
# File: export_dialog.py
# Description: PyQT6 print to pdf dialog component.
# Date: 14/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import QByteArray, QMarginsF, QSize
from PyQt6.QtGui import QPageLayout, QPageSize, QIcon
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialogButtonBox,
    QDialog,
    QLineEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
    QPushButton,
    QComboBox,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import PROTEUS_NAME
from proteus.model.object import Object
from proteus.controller.command_stack import Controller
from proteus.views import APP_ICON_TYPE
from proteus.views.components.abstract_component import ProteusComponent


# --------------------------------------------------------------------------
# Class: ExportDialog
# Description: Class for the PROTEUS application print to pdf dialog form.
# Date: 14/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ExportDialog(QDialog, ProteusComponent):
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
    def __init__(self, controller: Controller, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the page object and the controller instance.

        NOTE: Optional ProteusComponent parameters are omitted in the constructor,
        they can still be passed as keyword arguments.

        :param controller: Controller instance.
        """
        super(ExportDialog, self).__init__(controller, *args, **kwargs)
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
            # File format variable
            file_format: str = self.export_format_selector.currentText()

            # Build default file name
            current_document = self._state_manager.get_current_document()
            current_view = self._state_manager.get_current_view()
            document: Object = self._controller.get_element(current_document)
            default_file_name: str = f"{document.get_property(PROTEUS_NAME).value}-{current_view}.{file_format}"

            # Open the file dialog and set the default file name
            file_dialog: QFileDialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
            file_dialog.setDefaultSuffix(file_format)
            file_dialog.setNameFilter(f"{file_format} files (*.{file_format})")
            file_dialog.selectFile(default_file_name)
            file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

            # Get the selected file path and fix the extension if needed
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                path: str = file_dialog.selectedFiles()[0]
                if not path.endswith(f".{file_format}"):
                    path += f".{file_format}"
                # Check if the file already exists and ask for overwrite
                if os.path.exists(path):
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setText(
                        self._translator.text(
                            "export_dialog.filename.warning.text", path
                        )
                    )
                    msg_box.setWindowTitle(
                        self._translator.text("export_dialog.filename.warning.title")
                    )
                    msg_box.setStandardButtons(
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if msg_box.exec() == QMessageBox.StandardButton.Yes:
                        self.filename_input.setText(path)
                else:
                    self.filename_input.setText(path)

        # Set the dialog title and width
        self.setWindowTitle(self._translator.text("export_dialog.title"))
        self.sizeHint = lambda: QSize(400, 0)

        # Set window icon
        proteus_icon: Path = self._config.get_icon(APP_ICON_TYPE, "proteus_icon")
        self.setWindowIcon(QIcon(proteus_icon.as_posix()))

        # Export format selector
        export_format_label = QLabel(
            self._translator.text("export_dialog.export_format.label")
        )
        self.export_format_selector = QComboBox()
        # NOTE: This is done manually because there is no plan to support more formats
        self.export_format_selector.addItem("pdf")
        self.export_format_selector.addItem("html")

        # Ask for filename and path
        filename_label = QLabel(self._translator.text("export_dialog.filename.label"))
        self.filename_input: QLineEdit = QLineEdit()
        self.filename_input.setEnabled(False)
        browse_button = QPushButton(
            self._translator.text("export_dialog.filename.browser")
        )
        browse_button.clicked.connect(select_file_path)

        # Error label
        self.error_label = QLabel()
        self.error_label.setObjectName("error_label")
        self.error_label.setWordWrap(True)

        # Create the buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)

        # Create the main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Add the components to the main layout
        self.main_layout.addWidget(export_format_label)
        self.main_layout.addWidget(self.export_format_selector)
        self.main_layout.addWidget(filename_label)
        self.main_layout.addWidget(self.filename_input)
        self.main_layout.addWidget(self.error_label)
        self.main_layout.addWidget(browse_button)
        self.main_layout.addWidget(self.button_box)

    # ======================================================================
    # Export methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : export_to_pdf
    # Description: Export the current document to pdf.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def export_to_pdf(self, file_path: str) -> None:
        """
        Export the current document to pdf.
        """
        # NOTE: Page loading and pdf printing are asynchronous, so we need to
        # wait until the page is loaded to print the pdf and the variable page
        # must be a class attribute to avoid garbage collection.
        # To solve this problem, helper functions are used to ensure that they
        # are executed in the correct order.

        def create_page() -> None:
            # Create the page object
            self.page: QWebEnginePage = QWebEnginePage()

            # Get current application state
            current_document = self._state_manager.get_current_document()
            current_view = self._state_manager.get_current_view()

            # Generate html view
            html_view: str = self._controller.get_document_view(
                document_id=current_document, xslt_name=current_view
            )

            # Convert html to QByteArray
            # NOTE: This is done to avoid 2mb limit on setHtml method
            # https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwebenginewidgets/qwebengineview.html#setHtml
            html_array: QByteArray = QByteArray(html_view.encode(encoding="utf-8"))
            self.page.setContent(html_array, "text/html")

        def print_page() -> None:
            # Define the margin values (in millimeters)
            margins: QMarginsF = QMarginsF(30, 20, 30, 20)

            # Create a QPageLayout object from the options dictionary
            page_layout = QPageLayout(
                QPageSize(QPageSize.PageSizeId.A4),
                QPageLayout.Orientation.Portrait,
                margins,
            )

            # Print to pdf the current view with margins
            self.page.printToPdf(file_path, page_layout)

        # Create the page and print it to pdf
        create_page()
        self.page.loadFinished.connect(print_page)
        # Show a dialog when the pdf printing is finished
        self.page.pdfPrintingFinished.connect(self.export_finished_dialog)

    # ----------------------------------------------------------------------
    # Method     : export_to_html
    # Description: Export the current document to html.
    # Date       : 08/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def export_to_html(self, file_path: str) -> None:
        """
        Export the current document to html.
        """
        # Get current application state
        current_document = self._state_manager.get_current_document()
        current_view = self._state_manager.get_current_view()

        # Generate html view
        html_view: str = self._controller.get_document_view(
            document_id=current_document, xslt_name=current_view
        )

        # Write the html to a file
        success = True
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_view)
        except Exception as e:
            success = False

        # Show a dialog when the html file is created
        self.export_finished_dialog(file_path, success)

    # ======================================================================
    # Dialog slots methods (connected to the component signals and helpers)
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
        Export when the accept button is clicked.
        """
        # Get the filename + path
        file_path: str = self.filename_input.text()

        # Validate the filename
        if file_path == "" or file_path is None:
            self.error_label.setText(
                self._translator.text("export_dialog.error.invalid_filename")
            )
            return

        # Get the selected export format
        export_format: str = self.export_format_selector.currentText()

        # Check the export format and the filename extension match
        if not file_path.endswith(export_format):
            self.error_label.setText(
                self._translator.text("export_dialog.error.invalid_extension")
            )
            return

        # Export depending on the selected format
        if export_format == "pdf":
            self.export_to_pdf(file_path)
        elif export_format == "html":
            self.export_to_html(file_path)

        # Close the dialog when the export is finished in export_finished_dialog method

    # ----------------------------------------------------------------------
    # Method     : print_pdf_finished_dialog
    # Description: Show a dialog when the export is finished.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def export_finished_dialog(self, filePath: str, success: bool) -> None:
        """
        Show a dialog when the export is finished.
        """
        if success:
            QMessageBox.information(
                self,
                self._translator.text("export_dialog.finished.dialog.title"),
                self._translator.text("export_dialog.finished.dialog.text", filePath),
            )
            self.close()
        else:
            QMessageBox.critical(
                self,
                self._translator.text("export_dialog.finished.dialog.error.title"),
                self._translator.text("export_dialog.finished.dialog.error.text"),
            )
            self.close()

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog (static)
    # Description: Handle the creation and display of the form window.
    # Date       : 14/07/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(controller: Controller) -> "ExportDialog":
        """
        Handle the creation and display of the form window.

        :param controller: The application controller.
        """
        form_window = ExportDialog(controller)
        form_window.exec()
        return form_window
