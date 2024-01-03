# ==========================================================================
# File: app.py
# Description: the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from pathlib import Path
import sys
import logging
import traceback
import shutil

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QApplication, QMessageBox

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_LOGGING_DIR
from proteus.utils.config import Config
from proteus.utils.plugin_manager import PluginManager
from proteus.views.components.main_window import MainWindow
from proteus.utils.translator import Translator
from proteus.controller.command_stack import Controller

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: ProteusApplication
# Description: Class for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------


class ProteusApplication:
    def __init__(self):
        """
        It initializes the PROTEUS application.
        """
        self.config: Config = Config()
        self.plugin_manager: PluginManager = PluginManager()
        self.app: QApplication = None
        self.main_window: MainWindow = None

    def run(self) -> int:
        """
        PROTEUS application main method.
        """

        log.info(f"Current working directory: {Path.cwd()}")
        log.info(f"Home directory: {Path.home()}")
        log.info(f"{Path(__file__) = }")

        log.info(f"{self.config.resources_directory = }")
        log.info(f"{self.config.icons_directory = }")
        log.info(f"{self.config.archetypes_directory = }")

        # Load plugins
        self.plugin_manager.load_plugins()

        # Create the application instance
        sys.excepthook = self.excepthook
        self.app = QApplication(sys.argv)

        with open(
            self.config.resources_directory / "stylesheets" / "proteus.qss", "r"
        ) as f:
            _stylesheet = f.read()
            self.app.setStyleSheet(_stylesheet)

        # Create the main window
        self.main_window = MainWindow(parent=None, controller=Controller())
        self.main_window.show()

        # Execute the application
        sys.exit(self.app.exec())

    # NOTE: Exception handling for QApplication must be done overriding the
    # excepthook method. Otherwise, it will depend on the thread where the
    # exception is raised.
    # https://stackoverflow.com/questions/55819330/catching-exceptions-raised-in-qapplication
    def excepthook(self, exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        log.critical("Uncaught exception:\n" + tb)

        # Show the exception and its traceback in a message box
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle(Translator().text("app.critical_error.title"))
        error_dialog.setText(Translator().text("app.critical_error.text"))
        error_dialog.setInformativeText(tb)
        error_dialog.exec()

        # Override closeEvent in main window to avoid asking for confirmation
        # when closing the application
        self.main_window.closeEvent = lambda event: event.accept()

        self.handle_critical_error()

    # TODO: Find a way to store application state before quitting
    # and restore it when the application is restarted.
    def handle_critical_error(self):
        """
        Handle a critical error in the application quitting the application.
        """
        # Before quitting, try to disconnect signals
        try:
            self.main_window._controller.stack.canRedoChanged.disconnect()
            self.main_window._controller.stack.canUndoChanged.disconnect()
            self.main_window._controller.stack.cleanChanged.disconnect()
            self.main_window._controller.stack.clear()
            self.main_window._controller.stack.deleteLater()
        except Exception as e:
            log.critical(f"Error clearing the undo stack: {e}")

        # Select last log file
        log_files = sorted(PROTEUS_LOGGING_DIR.glob("*.log"))
        log_file = log_files[-1]

        # Build new crash report file name
        log_file_name = log_file.name
        crash_report_file_name = f"proteus_crash_report-{log_file_name}"
        
        # Copy log file to cwd with new name
        crash_report_file = Path.cwd() / crash_report_file_name
        shutil.copy(log_file, crash_report_file)

        # Quit the application
        self.app.quit()
