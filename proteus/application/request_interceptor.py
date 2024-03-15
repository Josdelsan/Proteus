# ==========================================================================
# File: request_interceptor.py
# Description: module for the PROTEUS request interceptor mechanism
# Date: 16/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import threading
import logging
import os
import socket
from socketserver import ThreadingMixIn
from http.server import HTTPServer, SimpleHTTPRequestHandler

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWebEngineCore import (
    QWebEngineUrlRequestInterceptor,
    QWebEngineUrlRequestInfo,
)
from PyQt6.QtCore import QUrl

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ASSETS_REPOSITORY
from proteus.application import TEMPLATE_DUMMY_SEARCH_PATH, ASSETS_DUMMY_SEARCH_PATH
from proteus.application.config import Config

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: ThreadingHTTPServer
# Description: Threaded HTTPServer
# Date: 16/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Threaded HTTPServer to handle resources requests."""

    # TODO: Daemon threads flag allows to delete the server threads when the server
    # shutdown method is called. This is a workaround to avoid application not closing
    # when the server is shutdown due to alive threads. Find a better solution.
    # https://stackoverflow.com/a/48283153
    daemon_threads = True


# --------------------------------------------------------------------------
# Class: CustomRequestHandler
# Description: Custom request handler to handle resources requests.
# Date: 16/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class CustomRequestHandler(SimpleHTTPRequestHandler):
    """
    Custom request handler to handle resources requests.

    It loads the resources from disk and sends them to the client (view).
    It can handle template resources and assets requests. Requests must be
    sent to the following endpoints:
        - /templates/<resource_path>
        - /assets/<resource_path>

    If the resource is not found, it sends a 500 response with the error message.
    """

    # --------------------------------------------------------------------------
    # Method: do_GET
    # Description: Handles GET requests.
    # Date: 16/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def do_GET(self):
        """
        Handles GET requests. Evaluates the request path to check if it is a
        template resource or an asset request. Build the file path and send
        the file content to the client.
        """
        try:
            # Separate the search path and the resource path
            search_path: str = self.path[1:].split("/")[0]
            resource_path: str = self.path[1:].replace(search_path, "", 1)

            # Based on the search path, get the resource directory
            resource_directory: str = None
            if TEMPLATE_DUMMY_SEARCH_PATH == search_path:
                resource_directory = Config().xslt_directory.as_posix()
            elif ASSETS_DUMMY_SEARCH_PATH == search_path:
                resource_directory = (
                    f"{Config().current_project_path}/{ASSETS_REPOSITORY}"
                )
            else:
                raise Exception(
                    f"Invalid search path: {search_path} while handling request {self.path}"
                )

            # Build the file path
            file_path = f"{resource_directory}/{resource_path}"

            # Check if the file exists
            if os.path.exists(file_path):
                # Open and read the file
                with open(file_path, "rb") as file:
                    content = file.read()

                # Send response headers
                self.send_response(200)
                self.send_header("Content-Type", self.guess_type(file_path))
                self.send_header("Content-Length", len(content))
                self.end_headers()

                # Send the file content
                self.wfile.write(content)
            else:
                # File not found, send a 404 response
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File Not Found")

        except Exception as e:
            # Handle exceptions and send a 500 response on error
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())


    # --------------------------------------------------------------------------
    # Method: log_message
    # Description: Overrides the log_message method to avoid logging in the stdout.
    # Date: 16/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def log_message(self, format, *args):
        """
        Overrides the log_message method to avoid logging in the stdout.
        """
        log.debug(format % args)

# --------------------------------------------------------------------------
# Class: WebEngineUrlRequestInterceptor
# Description: WebEngineUrlRequestInterceptor class.
# Date: 16/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    """
    WebEngineUrlRequestInterceptor class. Intercepts the resources requests
    from the view and sends them to the local server if needed.

    This class allows to load resources from disk in QWebEngine when using
    the following syntax:
        - template:///<template_dir_name>/<relative_path_to_template_resource>
        - assets:///<relative_path_to_asset_resource>

    Assets are accessed from the assets directory in the current opened project.
    Templates resources are accessed from the xslt directory in the resources folder,
    that is why it is needed to use the <template_dir_name>.

    This class uses a local server to handle the requests. The server is started
    when the class is instantiated and stopped when the application is closed. The
    port used by the server is the first available port starting from 20001.
    """

    HOST = "localhost"
    port = 20001

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Class constructor.
    # Date: 16/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Class constructor. Starts the threaded http server."""
        super(WebEngineUrlRequestInterceptor, self).__init__(*args, **kwargs)

        log.info("Starting WebEngineUrlRequestInterceptor server...")

        # Look for an available port
        self.port = self.find_available_port()

        log.info(
            f"WebEngineUrlRequestInterceptor server will listen on port {self.port}"
        )

        # Start the server
        self.server = ThreadingHTTPServer((self.HOST, self.port), CustomRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        log.info("WebEngineUrlRequestInterceptor server started")

    # --------------------------------------------------------------------------
    # Method: stop_server
    # Description: Stops the server.
    # Date: 16/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def stop_server(self):
        """Stops the server."""
        if self.server is None:
            return

        log.info("Stopping WebEngineUrlRequestInterceptor server...")
        self.server.shutdown()
        self.server.server_close()
        log.info("WebEngineUrlRequestInterceptor server stopped")

    # --------------------------------------------------------------------------
    # Method: find_available_port
    # Description: Finds an available port starting from the default port.
    # Date: 16/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def find_available_port(self) -> int:
        """
        Finds an available port starting from the default port.

        Uses socket to check if the port is available. If the port is not
        available, it tries with the next one.
        """
        port = self.port
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.HOST, port))
                    return port
            except OSError:
                port += 1

    # --------------------------------------------------------------------------
    # Method: interceptRequest
    # Description: Intercepts the resources requests and redirects them to the
    # local server if needed.
    # Date: 16/01/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def interceptRequest(self, info: QWebEngineUrlRequestInfo):
        """
        Intercepts the resources requests and redirects them to the local server
        if needed.

        Requests matching the following syntax are redirected to the local server:
            - template:///<path>
            - assets:///<path>
        """
        url = info.requestUrl().url()

        # Handle template resources or assets requests
        if url.startswith(f"{TEMPLATE_DUMMY_SEARCH_PATH}:///") or url.startswith(
            f"{ASSETS_DUMMY_SEARCH_PATH}:///"
        ):
            new_url = f"http://{self.HOST}:{self.port}/{url.replace(':///', '/')}"
            info.redirect(QUrl(new_url))
