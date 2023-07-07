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
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import markdown
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------


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
# Description: Build a path from a list of strings
# Date: 03/07/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
def build_path(context, file_name: str, assets_path: Path) -> str:
    """
    Build a path from a list of strings
    """
    return str(assets_path / file_name)