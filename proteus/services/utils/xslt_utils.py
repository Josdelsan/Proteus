# ==========================================================================
# File: xslt_utils.py
# Description: XSLT utils for document rendering
# Date: 29/06/2023
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

from proteus.config import Config
from proteus.model import ASSETS_REPOSITORY


# --------------------------------------------------------------------------
# Function: generate_markdown
# Description: Generate markdown from a list of etree.Element
# Date: 29/06/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def generate_markdown(context, markdown_element: List[ET.Element]) -> str:
    """
    Generate markdown from a list of etree.Element. Markdown is generated
    from the text of the elements in the list.
    """
    markdown_text = ""
    for element in markdown_element:
        markdown_text += element.text

    # TODO: Loading markdown extensions generate tons of innecesary logs.
    # This is caused by markdown library using logging module. Check
    # alternatives to avoid this.
    # https://github.com/Python-Markdown/markdown/issues/954
    result: str = markdown.markdown(
        markdown_text,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
        ],
    )
    return result


# --------------------------------------------------------------------------
# Function: build_path
# Description: Creates the base64 representation of the image.
# Date: 11/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def image_to_base64(context, asset_file: List[ET.Element]) -> str:
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
