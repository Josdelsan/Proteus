# ==========================================================================
# File: render_service.py
# Description: Render service for document rendering
# Date: 29/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import List, Dict
from pathlib import Path
import os

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ASSETS_REPOSITORY
from proteus.utils.config import Config
from proteus.services.utils import xslt_utils

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: RenderService
# Description: Class for render service
# Date: 29/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class RenderService:
    """
    Handle the logic for rendering documents. Store the XSLT transformation
    objects.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Initialize the RenderService object. Load the XSLT
    #              templates.
    # Date       : 29/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, config: Config = None) -> None:
        """
        Initialize the RenderService object. Load the XSLT templates.
        """
        # Dependency injection
        if config is None:
            config = Config()
        self.config = config

        # Namespace configuration for the XSLT functions
        self._namespace_configuration()

        # Store the XSLT transformation objects
        self._transformations: List[ET.XSLT] = {}

        log.info("RenderService initialized")

    # ----------------------------------------------------------------------
    # Method     : _namespace_configuration
    # Description: Configuration setup for the XSLT functions. This allows
    #              to use custom python functions in the XSLT templates.
    # Date       : 29/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _namespace_configuration(self) -> None:
        """
        Configuration setup for the XSLT functions. This allows to use
        custom python functions in the XSLT templates.
        """
        # Namespace for the XSLT functions
        ns = ET.FunctionNamespace("http://proteus.us.es/utils")
        ns.prefix = "proteus-utils"

        # Register the function with the FunctionNamespace
        ns["generate_markdown"] = xslt_utils.generate_markdown
        ns["image_to_base64"] = xslt_utils.image_to_base64
        ns["current_document"] = xslt_utils.current_document

    # ----------------------------------------------------------------------
    # Method     : get_xslt
    # Description: Get the XSLT transformation object for the given xslt_name.
    #              If the object is not found, create it from the xslt file.
    # Date       : 29/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def _get_xslt(self, xslt_name) -> ET.XSLT:
        """
        Get the XSLT transformation object for the given xslt_name. If the
        object is not found, create it from the xslt file.
        """
        transform: ET.XSLT = None

        if xslt_name in self._transformations:
            transform = self._transformations[xslt_name]
        else:
            # Get the xslt file path and check if it exists in the app config
            xslt_routes: Dict[str, Path] = Config().xslt_routes
            assert (
                xslt_name in xslt_routes
            ), f"XSLT file {xslt_name} not found in config file"
            XSL_TEMPLATE = Config().xslt_routes[xslt_name]

            # Create the transformer from the xsl file
            transform = ET.XSLT(ET.parse(XSL_TEMPLATE))

            # NOTE: Comment this line to make XSLT debugging easier
            # Store the transformation object for future use
            self._transformations[xslt_name] = transform

        return transform

    # ----------------------------------------------------------------------
    # Method     : render
    # Description: Render the given xml using the xslt_name template.
    # Date       : 29/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def render(self, xml: ET.Element, xslt_name: str) -> str:
        """
        Render the given xml using the xslt_name template.
        """
        transform = self._get_xslt(xslt_name)
        try:
            result_tree = transform(xml)
        except:
            for error in transform.error_log:
                log.error(f"Error found while rendering xml using template {xslt_name}, line {error.line}, column {error.column}: {error.message}")
        html_string = ET.tostring(result_tree, encoding="unicode", pretty_print=True, method="html")
        return html_string

    # ----------------------------------------------------------------------
    # Method     : get_available_xslt
    # Description: Get the available xslt templates in the xslt folder.
    # Date       : 29/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_available_xslt(self) -> List[str]:
        """
        Get the available xslt templates in the xslt folder.
        """
        xslt_routes: Dict[str, Path] = self.config.xslt_routes
        return list(xslt_routes.keys())
