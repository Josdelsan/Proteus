# ==========================================================================
# File: test_proteus_xslt_basics.py
# Description: PROTEUS basics plugin tests.
# Date: 06/03/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import pytest
from lxml import etree as ET

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from .proteus_xslt_basics import generate_markdown

# ==========================================================================
# Tests
# ==========================================================================


@pytest.mark.parametrize(
    "markdown_text, expected_html",
    [
        ("Simple string not wrapped", "Simple string not wrapped"),
        ("```Fenced code block```", "<code>Fenced code block</code>"),
        (
            "| Header 1 | Header 2 |\n| -------- | -------- |\n| Cell 1 | Cell 2 |",
            "<table>\n<thead>\n<tr>\n<th>Header 1</th>\n<th>Header 2</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td>Cell 1</td>\n<td>Cell 2</td>\n</tr>\n</tbody>\n</table>",
        ),
        (
            "[TOC]\n\n# Header 1\n\n## Header 2",
            '<div class="toc">\n<ul>\n<li><a href="#header-1">Header 1</a><ul>\n<li><a href="#header-2">Header 2</a></li>\n</ul>\n</li>\n</ul>\n</div>\n<h1 id="header-1">Header 1</h1>\n<h2 id="header-2">Header 2</h2>',
        ),
    ],
)
def test_generate_markdown(markdown_text, expected_html):
    """
    Tests generated html works as expected. This test assumes
    markdown library works correctly.

    Generated HTML must not be wrapped in <p> tags and
    all the expected markdown library extensions must be
    working.
    """
    # Convert markdown text to ET._Element list
    markdown_element = ET.Element("markdown")
    markdown_element.text = markdown_text
    input_text = [markdown_element]

    generated_html = generate_markdown({}, input_text)
    assert (
        generated_html == expected_html
    ), f"Generated HTML: '\n{generated_html}\n' is not equal to expected HTML: '\n{expected_html}\n'"
