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
from PyQt6.QtWebEngineCore import QWebEngineProfile

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus import PROTEUS_LOGGING_DIR
from proteus.application.spellcheck import SpellCheckerWrapper
from proteus.application.configuration.config import Config
from proteus.application.resources.plugins import Plugins
from proteus.application.resources.translator import Translator
from proteus.application.resources.icons import Icons
from proteus.application.state_manager import StateManager
from proteus.application.state_restorer import read_state_from_file
from proteus.application.request_interceptor import WebEngineUrlRequestInterceptor
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
        self.plugin_manager: Plugins = Plugins()
        self.translator: Translator = Translator()
        self.dynamic_icons: Icons = Icons()
        self.spellchecker = SpellCheckerWrapper()

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

        # Create the application instance and set the excepthook
        # to handle uncaught exceptions in every thread.
        sys.excepthook = self.excepthook
        self.app = QApplication(sys.argv)

        # Increase the font size of the application
        # app_font = self.app.font()
        # app_font.setPointSize(app_font.pointSize() + 2)
        # self.app.setFont(app_font)

        # Initial setup
        self.initial_setup()

        # Create the main window
        controller = Controller()
        self.main_window = MainWindow(parent=None, controller=controller)
        self.main_window.show()

        # Load plugin components
        self.load_plugin_components()

        if self.project_path:
            controller.load_project(self.project_path.as_posix())
            read_state_from_file(self.project_path, controller, StateManager())

        # Execute the application
        sys.exit(self.app.exec())

    # --------------------------------------------------------------------------
    # Method: initial_setup
    # Description: Initial configuration of the application.
    # Date: 12/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def initial_setup(self) -> None:
        """
        Initial configuration that must be done before the app start.

        It handles initialization of translator, icons, plugins,
        request interceptor and stylesheet
        """
        # App settings resources ------------------------------
        self.translator.set_language(self.config.app_settings.language)
        self.translator.set_proteus_i18n_directory(
            self.config.app_settings.i18n_directory
        )
        self.translator.load_translations(self.config.app_settings.i18n_directory)
        self.dynamic_icons.load_icons(self.config.app_settings.icons_directory)

        # Profile resources -----------------------------------
        self.translator.load_translations(self.config.profile_settings.i18n_directory)
        self.dynamic_icons.load_icons(self.config.profile_settings.icons_directory)
        self.plugin_manager.load_plugins(self.config.profile_settings.plugins_directory)

        # SpellCheckerWrapper ----------------------
        spellchecker_language = self.config.app_settings.spellchecker_language
        if spellchecker_language is not None:
            self.spellchecker.set_language(spellchecker_language)


        # Setup the request interceptor -----------------------
        profile = QWebEngineProfile.defaultProfile()
        profile.setUrlRequestInterceptor(self.request_interceptor)
        self.app.aboutToQuit.connect(self.request_interceptor.stop_server)

        # Set application style sheet -------------------------
        with open(
            self.config.app_settings.resources_directory
            / "stylesheets"
            / "proteus.qss",
            "r",
        ) as f:
            _stylesheet = f.read()
            self.app.setStyleSheet(_stylesheet)
            del _stylesheet

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
