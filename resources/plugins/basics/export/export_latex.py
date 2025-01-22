# ==========================================================================
# File: export_latex.py
# Description: PyQT6 print latex to pdf dialog component.
# Date: 20/01/2025
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from pathlib import Path
import subprocess
import re

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import (
    QWidget,
    QDialog,
    QTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
)


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_TEMP_DIR
from proteus.application.resources.translator import translate as _
from proteus.application.state.manager import StateManager
from proteus.controller.command_stack import Controller
from proteus.application.export_strategy import ExportStrategy
from proteus.views.forms.directory_edit import DirectoryEdit


# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
FILE_EXTENSION_LATEX: str = "tex"
FILE_EXTENSION_PDF: str = "pdf"
LATEX_HTML_TAG: str = "latex"  # Defined by convention in the XSLT
LATEX_TEMP_DIR: Path = PROTEUS_TEMP_DIR / "latex"


# --------------------------------------------------------------------------
# Class: ExportLaTeX
# Description: Class for the PROTEUS application export to pdflatex strategy.
# Date: 20/01/2025
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ExportLaTeX(ExportStrategy):
    """
    Class for the PROTEUS application export to pdflatex strategy.

    It uses local installed LaTeX features to invoke pdflatex command
    and generate a PDF file from the LaTeX code.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Date       : 20/01/2025
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, controller: Controller) -> None:
        super().__init__(controller)

        self._export_widget: QWidget = None
        self._input: DirectoryEdit = None
        self._error_label: QLabel = None

    # ----------------------------------------------------------------------
    # Method     : export
    # Date       : 20/01/2025
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def export(self):
        # Generate html view
        current_view = StateManager().get_current_view()
        html_view_path: str = self._controller.get_html_view_path(
            xslt_name=current_view
        )

        # Extract LaTeX code from the html view
        html_str = Path(html_view_path).read_text(encoding="utf-8")
        latex_code: str = (
            re.search(r"<latex>(.*?)<\/latex>", html_str, re.DOTALL).group(1).strip()
        )

        self.exportProgressSignal.emit(15)

        # Create latex temp directory if it does not exist
        if not LATEX_TEMP_DIR.exists():
            LATEX_TEMP_DIR.mkdir(parents=True)

        # Create a temporary file with the LaTeX code
        temp_file_path: Path = LATEX_TEMP_DIR / f"{current_view}.{FILE_EXTENSION_LATEX}"
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(latex_code)

        self.exportProgressSignal.emit(25)

        # Call pdflatex command
        output_dir = self._input.directory()
        try:
            subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-output-directory={output_dir}",
                    temp_file_path,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            self.exportFinishedSignal.emit(f"{output_dir}/{current_view}.{FILE_EXTENSION_PDF}", True)
        except subprocess.CalledProcessError as e:
            log_content = e.stdout.decode("utf-8") + e.stderr.decode("utf-8")
            # Create a new window with the log content
            log_window = QDialog()
            log_window.setWindowTitle(_("export_dialog.export_latex.error.log.title"))
            log_window.setModal(True)
            log_window.resize(800, 600)

            log_text = QTextEdit()
            log_text.setPlainText(log_content)
            log_text.setReadOnly(True)

            layout = QVBoxLayout()
            layout.addWidget(log_text)
            log_window.setLayout(layout)
            log_window.exec()

            self.exportFinishedSignal.emit(e.stderr.decode(), False)

    # ----------------------------------------------------------------------
    # Method     : exportFormWidget
    # Date       : 20/01/2025
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def exportFormWidget(self):
        """
        Creates the export form widget for the export latex strategy.

        The latex export widget is a simple line edit with a browse button.
        User may browse the file system and select the path/name of the
        exported file. The widget also provides a error message label.
        """
        self._export_widget = QWidget()

        # Widget creation --------------------------------------------------
        # Directory edit
        self._input = DirectoryEdit()

        # Information label
        info_label = QLabel()
        info_label.setText(_("export_dialog.export_latex.dir.label"))

        # Error label
        self._error_label = QLabel()
        self._error_label.setObjectName("error_label")
        self._error_label.setWordWrap(True)
        self._error_label.setHidden(True)

        # Layout setup -----------------------------------------------------
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        input_layout.addWidget(self._input)
        input_layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(info_label)
        layout.addLayout(input_layout)
        layout.addWidget(self._error_label)
        layout.setContentsMargins(0, 0, 0, 0)

        self._export_widget.setLayout(layout)

        # Signals and slots ------------------------------------------------
        self._input.directoryChanged.connect(self._validate_dir_path)

        return self._export_widget


    # ======================================================================
    # Private methods
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : _validate_dir_path
    # Date       : 20/01/2025
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _validate_dir_path(self) -> None:
        """
        Validates the directory path.

        The path must exist and be a directory.
        """
        path = self._input.directory()

        if not path:
            self._error_label.setText(_("export_dialog.export_latex.error.empty"))
            self._error_label.setHidden(False)
            self.readyToExportSignal.emit(False)

        if not Path(path).exists():
            self._error_label.setText(_("export_dialog.export_latex.error.not_exist"))
            self._error_label.setHidden(False)
            self.readyToExportSignal.emit(False)

        if not Path(path).is_dir():
            self._error_label.setText(_("export_dialog.export_latex.error.not_dir"))
            self._error_label.setHidden(False)
            self.readyToExportSignal.emit(False)

        self._error_label.setHidden(True)
        self.readyToExportSignal.emit(True)