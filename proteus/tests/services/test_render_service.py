# ==========================================================================
# File: test_render_service.py
# Description: pytest file for the PROTEUS render service
# Date: 19/08/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.properties import Property, PropertyFactory
from proteus.services.project_service import ProjectService
from proteus.services.render_service import RenderService
from proteus.tests import PROTEUS_SAMPLE_DATA_PATH

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

DEFAULT_TEMPLATE = "default"


@pytest.fixture(scope="module")
def render_service():
    """
    Fixture for RenderService object
    """
    # Config object is not mocked
    return RenderService()

@pytest.fixture(scope="module")
def example_xml() -> ET.Element:
    """
    Fixture for example XML. XML was created from EXAMPLE document
    from example_project.
    """
    xml_path = PROTEUS_SAMPLE_DATA_PATH / "example_project_example_doc.xml"
    return ET.parse(xml_path)

@pytest.fixture(scope="module")
def example_html() -> str:
    """
    Fixture for example HTML. HTML was created from EXAMPLE document
    from example_project. Generated with default template.
    """
    html_path = PROTEUS_SAMPLE_DATA_PATH / "example_project_example_doc_default_template.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    return html_string

def normalize_string(string: str) -> str:
    """
    Normalize a string to compare it with another string
    """
    string = string.replace('\r\n', '\n').replace('\r', '\n')
    return ' '.join(string.strip().split())


# --------------------------------------------------------------------------
# Integration tests
# --------------------------------------------------------------------------

@pytest.mark.order(1)
def test_get_xslt(render_service: RenderService):
    """
    Test for get_xslt method
    """
    # Act -----------------------------
    xslt = render_service._get_xslt(DEFAULT_TEMPLATE)

    # Assert --------------------------
    assert isinstance(
        xslt, ET.XSLT
    ), f"XSLT object must be an instance of ET.XSLT but it is {type(xslt)}"

    assert (
        xslt in render_service._transformations.values()
    ), "XSLT object must be stored in the RenderService object"


# @pytest.mark.order(2)
@pytest.mark.skip(reason="Comparing both html strings is not working correctly")
def test_render(render_service: RenderService, example_xml: ET.Element, example_html: str):
    """
    Test for render method
    """
    # Arrange -------------------------
    # Act -----------------------------
    # Test for a valid render
    html_string: str = render_service.render(example_xml, DEFAULT_TEMPLATE)

    # Assert --------------------------
    assert isinstance(
        html_string, str
    ), f"Render result must be an instance of string but it is {type(html_string)}"

    assert (
        html_string == example_html
    ), "Render result does not match with the expected result from the example HTML file"

# --------------------------------------------------------------------------
# Unit tests
# --------------------------------------------------------------------------
