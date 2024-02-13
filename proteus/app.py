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
from proteus.utils.dynamic_icons import DynamicIcons
from proteus.utils.state_manager import StateManager
from proteus.utils.state_restorer import read_state_from_file
from proteus.utils.request_interceptor import WebEngineUrlRequestInterceptor
from proteus.controller.command_stack import Controller
from proteus.views.components.main_window import MainWindow

# Module configuration
log = logging.getLogger(__name__)  # Logger
_ = Translator().text  # Translator


# --------------------------------------------------------------------------
# Class: ProteusApplication
# Description: Class for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------


class ProteusApplication:
    def __init__(self, project_path: Path = None):
        """
        It initializes the PROTEUS application.
        """
        # General configuration
        self.config: Config = Config()
        self.plugin_manager: PluginManager = PluginManager()
        self.translator: Translator = Translator()
        self.dynamic_icons: DynamicIcons = DynamicIcons()

        # Request interceptor
        self.request_interceptor: WebEngineUrlRequestInterceptor = (
            WebEngineUrlRequestInterceptor()
        )

        # PyQt6 application and main window
        self.app: QApplication = None
        self.main_window: MainWindow = None

        # Optional params
        self.project_path = project_path

    def run(self) -> int:
        """
        PROTEUS application main method.
        """

        # Log initial information
        log.info(f"Current working directory: {Path.cwd()}")
        log.info(f"Home directory: {Path.home()}")
        log.info(f"{Path(__file__) = }")

        log.info(f"{self.config.resources_directory = }")
        log.info(f"{self.config.icons_directory = }")
        log.info(f"{self.config.archetypes_directory = }")

        # Create the application instance and set the excepthook
        # to handle uncaught exceptions in every thread.
        sys.excepthook = self.excepthook
        self.app = QApplication(sys.argv)

        # Initial configuration
        self.initial_configuration()

        # Create the main window
        controller = Controller()
        self.main_window = MainWindow(parent=None, controller=controller)
        self.main_window.show()

        # Plugin dependencies check and load plugin components
        self.check_plugins_dependencies()
        self.load_plugin_components()

        if self.project_path:
            controller.load_project(self.project_path.as_posix())
            read_state_from_file(self.project_path, controller, StateManager())

        # Execute the application
        sys.exit(self.app.exec())

    # --------------------------------------------------------------------------
    # Method: initial_configuration
    # Description: Initial configuration of the application.
    # Date: 12/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def initial_configuration(self) -> None:
        """
        Initial configuration that must be done before the app start.

        It handles initialization of translator, dynamic icons, plugins,
        request interceptor and stylesheet
        """
        # Set translator configuration and load translations
        self.translator.set_language(self.config.language)
        self.translator.set_i18n_directory(self.config.i18n_directory)
        self.translator.set_archetypes_directory(self.config.archetypes_directory)
        self.translator.load_system_translations()

        # Set dynamic icons configuration and load icons
        self.dynamic_icons.set_icons_directory(self.config.icons_directory)
        self.dynamic_icons.set_archetypes_directory(self.config.archetypes_directory)
        self.dynamic_icons.load_system_icons()

        # Load plugins
        self.plugin_manager.load_plugins()

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
            del _stylesheet

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
        error_dialog.setWindowTitle(_("app.critical_error.title"))
        error_dialog.setText(_("app.critical_error.text"))
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
