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
from typing import List
import sys
import logging
import traceback
import shutil

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtWebEngineCore import QWebEngineProfile

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_LOGGING_DIR
from proteus.utils.config import Config
from proteus.utils.plugin_manager import PluginManager
from proteus.utils.translator import Translator
from proteus.utils.request_interceptor import WebEngineUrlRequestInterceptor
from proteus.controller.command_stack import Controller
from proteus.views.components.main_window import MainWindow

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
        self.request_interceptor: WebEngineUrlRequestInterceptor = (
            WebEngineUrlRequestInterceptor()
        )
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

        # Setup the request interceptor
        profile = QWebEngineProfile.defaultProfile()
        profile.setUrlRequestInterceptor(self.request_interceptor)
        self.app.aboutToQuit.connect(self.request_interceptor.stop_server)

        # Set application style sheet
        with open(
            self.config.resources_directory / "stylesheets" / "proteus.qss", "r"
        ) as f:
            _stylesheet = f.read()
            self.app.setStyleSheet(_stylesheet)

        # Create the main window
        self.main_window = MainWindow(parent=None, controller=Controller())
        self.main_window.show()

        # Check plugins dependencies
        self.check_plugins_dependencies()

        # Load proteus components from plugins
        self.load_plugin_components()

        # Execute the application
        sys.exit(self.app.exec())

    # --------------------------------------------------------------------------
    # Method: check_plugins_dependencies
    # Description: Check if all the plugins dependencies are satisfied.
    # Date: 08/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def check_plugins_dependencies(self) -> None:
        """
        Check if all the plugins dependencies are satisfied. Do not return
        anything. If there is a dependency that is not satisfied, the
        application will crash.
        """
        loaded_plugins: List[str] = self.plugin_manager.get_plugins()

        for template, plugins in self.config.xslt_dependencies.items():
            for plugin in plugins:
                if plugin not in loaded_plugins:
                    raise Exception(
                        f"Plugin dependency not satisfied: '{plugin}' for template {template}. Current loaded plugins: {loaded_plugins}"
                    )

    # --------------------------------------------------------------------------
    # Method: load_plugin_components
    # Description: Load the ProteusComponents from the plugins.
    # Date: 09/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    # NOTE: This is done in app module to keep the main window clean. These are
    # components that will be not displayed but need access to the backend to
    # perform complex operations.
    def load_plugin_components(self) -> None:
        """
        Load the ProteusComponents from the plugins. It uses MainWindow instance
        as parent for the components.
        """
        for component in self.plugin_manager.get_proteus_components().values():
            try:
                component(self.main_window)
            except Exception as e:
                log.critical(f"Error loading proteus component from plugin: {e}")

    # --------------------------------------------------------------------------
    # Method: excepthook
    # Description: Handle uncaught exceptions in the application.
    # Date: 01/12/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
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

    # --------------------------------------------------------------------------
    # Method: handle_critical_error
    # Description: Handle a critical error in the application quitting the
    # application.
    # Date: 01/12/2023
    # Version: 0.1
    # --------------------------------------------------------------------------
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
