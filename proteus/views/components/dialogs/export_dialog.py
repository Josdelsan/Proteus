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

from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QDialog,
    QLabel,
    QMessageBox,
    QComboBox,
    QSizePolicy,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.controller.command_stack import Controller
from proteus.utils import ProteusIconType
from proteus.utils.translator import Translator
from proteus.views.components.abstract_component import ProteusComponent
from proteus.views.export import ExportFormat, ExportStrategy, ExportPDF, ExportHTML

# Module configuration
_ = Translator().text  # Translator


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
    def __init__(self, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component. Store the page object and the controller instance.
        """
        super(ExportDialog, self).__init__(*args, **kwargs)

        # Export strategy
        self._export_strategy: ExportStrategy = None

        # Widgets
        self.export_format_selector: QComboBox = None
        self.export_button: QPushButton = None  # Accept and cancel buttons
        self.export_widget_holder: QVBoxLayout = None

        # Create the component
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

        # Windows general settings ---------------------------------
        # Set the dialog title and width
        self.setWindowTitle(_("export_dialog.title"))
        self.sizeHint = lambda: QSize(400, 0)

        # Set window icon
        proteus_icon: Path = self._config.get_icon(ProteusIconType.App, "proteus_icon")
        self.setWindowIcon(QIcon(proteus_icon.as_posix()))

        # Expand policy
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )

        # Export format selector ---------------------------------
        export_format_label = QLabel(_("export_dialog.export_format.label"))
        self.export_format_selector = QComboBox()
        self.export_format_selector.addItem(
            _("export_dialog.export_format.pdf"), ExportFormat.PDF
        )
        self.export_format_selector.addItem(
            _("export_dialog.export_format.html"), ExportFormat.HTML
        )
        self.export_format_selector.currentIndexChanged.connect(
            self.update_export_strategy
        )

        # Specific export widget holder -----------------------------
        self.export_widget_holder = QVBoxLayout()
        self.export_widget_holder.setContentsMargins(0, 0, 0, 0)

        # Accept and cancel buttons ---------------------------------
        self.export_button = QPushButton(_("export_dialog.export_button.text"))
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_button_clicked)

        # Main layout setup ---------------------------------
        main_layout = QVBoxLayout()
        main_layout.addWidget(export_format_label)
        main_layout.addWidget(self.export_format_selector)
        main_layout.addLayout(self.export_widget_holder)
        main_layout.addStretch(1)
        main_layout.addWidget(self.export_button)

        self.setLayout(main_layout)

        # First export strategy setup ---------------------------------
        self.export_format_selector.setCurrentIndex(0)
        self.export_format_selector.currentIndexChanged.emit(0)

    # ======================================================================
    # Dialog slots methods (connected to the component signals and helpers)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : update_export_strategy
    # Description: Update the export strategy when the export format is
    #              changed.
    # Date       : 22/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def update_export_strategy(self, index: int) -> None:
        """
        Update the export strategy when the export format is changed.
        The export strategy widget is replaced by the new one.

        Old export strategy must be deleted to disconnect the signals.
        """
        # Get the selected export format
        export_format: str = self.export_format_selector.currentData()

        # Update button box
        self.export_button.setEnabled(False)

        # Delete the current export strategy
        # This is neccessary to disconnect the signals
        if self._export_strategy is not None:
            self._export_strategy.deleteLater()
            self._export_strategy = None

        # Clear the export widget holder
        for i in reversed(range(self.export_widget_holder.count())):
            self.export_widget_holder.itemAt(i).widget().setParent(None)

        # Update the export strategy ---------------------------------
        if export_format == ExportFormat.PDF:
            self._export_strategy = ExportPDF(self._controller)
        elif export_format == ExportFormat.HTML:
            self._export_strategy = ExportHTML(self._controller)
        else:
            raise ValueError("Invalid export format")

        # Setup new export strategy ---------------------------------
        # Strategy export widget
        export_widget: QWidget = self._export_strategy.exportFormWidget()
        self.export_widget_holder.addWidget(export_widget)

        # TODO: Find a way to resize the dialog to fit the export widget,
        #       resize() method does not work.

        # Connect strategy signals
        self._export_strategy.readyToExportSignal.connect(self.export_button.setEnabled)
        self._export_strategy.exportFinishedSignal.connect(self.export_finished_dialog)

    # ----------------------------------------------------------------------
    # Method     : export_button_clicked
    # Description: Handle the export button click.
    # Date       : 22/01/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def export_button_clicked(self) -> None:
        """
        Handle the export button click. Call the export strategy export
        method and disable the button box to avoid multiple exports.
        """
        self._export_strategy.export()
        self.export_button.setEnabled(False)

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

        :param filePath: The path to the exported file.
        :param success: True if the export was successful, False otherwise.
        """
        if success:
            QMessageBox.information(
                self,
                _("export_dialog.finished.dialog.title"),
                _("export_dialog.finished.dialog.text", filePath),
            )
            self.close()
        else:
            QMessageBox.critical(
                self,
                _("export_dialog.finished.dialog.error.title"),
                _("export_dialog.finished.dialog.error.text"),
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
        form_window = ExportDialog(controller=controller)
        form_window.exec()
        return form_window
