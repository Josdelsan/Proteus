# ==========================================================================
# Plugin: proteus_xslt_basics
# Description: PROTEUS plugin that provides basic XSLT functions for use in
#              templates. Some of these functions are:
#              - generate_markdown: Generate markdown from a list of etree.Element
#              - image_to_base64: Creates the base64 representation of an image.
#              - current_document: Returns the current selected document.
# Date: 03/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import markdown
import lxml.etree as ET
from PyQt6.QtGui import QImage
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.utils.config import Config
from proteus.utils.state_manager import StateManager
from proteus.model import ASSETS_REPOSITORY


# --------------------------------------------------------------------------
# Function: generate_markdown
# Description: Generate markdown from a list of etree.Element
# Date: 29/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def generate_markdown(context, markdown_element: List[ET._Element]) -> str:
    """
    Generate markdown from a list of etree.Element. Markdown is generated
    from the text of the elements in the list.
    """
    markdown_text = ""
    for element in markdown_element:
        markdown_text += element.text

    result: str = markdown.markdown(
        markdown_text,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
        ],
    )

    # Remove the first <p> tag and the last </p> tag
    result = result.replace("<p>", "", 1)
    result = result[::-1].replace("</p>", "", 1)[::-1]

    return result

# --------------------------------------------------------------------------
# Function: image_to_base64
# Description: Creates the base64 representation of an image.
# Date: 11/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def image_to_base64(context, asset_file: List[ET._Element]) -> str:
    """
    Given an asset file path, return the base64 representation of the image.
    Build the absolute path using the current project path and the assets
    repository name.
    """

    assets_path: str = f"{Config().current_project_path}/{ASSETS_REPOSITORY}/{asset_file[0].text}"

    # Load the image using QImage
    image = QImage(assets_path)

    ba = QByteArray()
    buffer = QBuffer(ba)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, 'PNG')
    base64_data = ba.toBase64().data().decode()
    return base64_data


# --------------------------------------------------------------------------
# Function: current_document
# Description: Returns the current document
# Date:21/12/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def current_document(context) -> str:
    """
    Returns the current selected document in the project context.
    """
    document_id = StateManager().get_current_document()
    return str(document_id)


# ==========================================================================
# Plugin registration method
# ==========================================================================
def register(register_xslt_function, _):
    register_xslt_function("generate_markdown", generate_markdown)
    register_xslt_function("image_to_base64", image_to_base64)
    register_xslt_function("current_document", current_document)