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

# --------------------------------------------------------------------------
# Third party imports
# --------------------------------------------------------------------------

import pytest
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.services.render_service import RenderService
from proteus.tests import PROTEUS_SAMPLE_DATA_PATH

# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

DEFAULT_TEMPLATE = "remus"


@pytest.fixture()
def render_service():
    """
    Fixture for RenderService object
    """
    # Config object is not mocked
    return RenderService()


@pytest.fixture()
def example_xml() -> ET.Element:
    """
    Fixture for example XML. XML was created from EXAMPLE document
    from example_project.
    """
    xml_path = PROTEUS_SAMPLE_DATA_PATH / "example_project_example_doc.xml"
    return ET.parse(xml_path)


@pytest.fixture()
def example_html() -> str:
    """
    Fixture for example HTML. HTML was created from EXAMPLE document
    from example_project. Generated with default template.
    """
    html_path = (
        PROTEUS_SAMPLE_DATA_PATH / "example_project_example_doc_default_template.html"
    )
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    return html_string


def normalize_string(string: str) -> str:
    """
    Normalize a string to compare it with another string
    """
    string = string.replace("\r\n", "\n").replace("\r", "\n")
    return " ".join(string.strip().split())


# --------------------------------------------------------------------------
# Integration tests
# --------------------------------------------------------------------------


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

@pytest.mark.order(2)
def test_render(
    mocker, render_service: RenderService, example_xml: ET.Element, example_html: str
):
    """
    Test for render method. PluginManager has to be loaded and namespace configuration
    has to be re-executed to test the render method.

    NOTE: The output HTML file does not load correctly the images, css and js because
    they are referenced using Proteus custom search paths that require server connection.
    This test only checks the HTML structure and content.
    """
    # Arrange -------------------------

    # TODO: Consider if it is worth to mock plugin_manager functions.
    render_service.plugin_manager.load_plugins()
    render_service._namespace_configuration()

    # Mock StataManager get_current_document method
    mocker.patch(
        "proteus.utils.state_manager.StateManager.get_current_document",
        return_value="722GfFiezi5F",
    )

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

@pytest.mark.order(1)
def test_render_error(mocker, render_service: RenderService, example_xml: ET.Element):
    """
    Test error handling when the XSLT transformation fails
    """
    # Arrange -------------------------
    # Force transformation failure not loading plugin manager because
    # default template requires a plugin function
    # Act -----------------------------
    html_string: str = render_service.render(example_xml, DEFAULT_TEMPLATE)

    # Assert --------------------------

    error_string = "<errors><error>Unregistered function</error><error>runtime error, element 'variable'</error><error>Failed to evaluate the expression of variable 'currentDocumentId'.</error></errors>\n"

    assert isinstance(
        html_string, str
    ), f"Render result must be an instance of string but it is {type(html_string)}"

    assert html_string == error_string, (
        "Render result does not match with the expected result from the example HTML file"
        f"\nRender result: {html_string}"
        f"\nExpected result: {error_string}"
    )


# --------------------------------------------------------------------------
# Unit tests
# --------------------------------------------------------------------------
