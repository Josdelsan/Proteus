# ==========================================================================
# File: test_icons.py
# Description: pytest file for the PROTEUS icons module
# Date: 01/04/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Generator, List
from pathlib import Path

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import pytest

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.tests import PROTEUS_SAMPLE_ICONS_PATH
from proteus.application.resources.icons import Icons


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------
@pytest.fixture
def icons_object() -> Generator[Icons, None, None]:
    """
    Icons is defined as a singleton, it is necessary to 'reset' the object
    before and after each test to ensure that the tests are independent when
    executed in a batch.
    """

    Icons._instances.pop(Icons, None)
    yield Icons()
    Icons._instances.pop(Icons, None)


# --------------------------------------------------------------------------
# Unit tests
# --------------------------------------------------------------------------


def test_icons_singleton(icons_object: Icons) -> None:
    """
    Test that the Icons object is a singleton.
    """

    icons_object_2 = Icons()
    assert icons_object is icons_object_2


def test_icons_load_icons_min(icons_object: Icons) -> None:
    """
    Test that the icons are loaded correctly with a minimal example directory.

    icons.xml file constains just one icon.
    """

    icons_object.load_icons(PROTEUS_SAMPLE_ICONS_PATH / "icons_valid_min")
    assert (
        len(icons_object._icons_paths) == 1
    ), "No icons types were found in the 'icons.xml' file"

    icons: List[Path] = []
    for icon_type in icons_object._icons_paths:
        icons.extend(icons_object._icons_paths[icon_type])

    assert len(icons) == 1, "No icons were found in the 'icons.xml' file"


def test_icons_load_icons_all_types(icons_object: Icons) -> None:
    """
    Test that the icons are loaded correctly with all icon types.

    icons.xml file constains just one icon.
    """

    icons_object.load_icons(PROTEUS_SAMPLE_ICONS_PATH / "icons_all_types")
    assert (
        len(icons_object._icons_paths) == 5
    ), f"Expected 5 icons types but '{len(icons_object._icons_paths)}' were found in the 'icons.xml' file"

    icons: List[Path] = []
    for icon_type in icons_object._icons_paths:
        icons.extend(icons_object._icons_paths[icon_type])

    assert (
        len(icons) == 5
    ), f"Expected 5 icons but '{len(icons)}' were found in the 'icons.xml' file"


def test_icons_load_icons_empty(icons_object: Icons) -> None:
    """
    Test that the icons are loaded correctly with a directory that does not contain any icons.

    icons.xml file just have <icons></icons> tags.
    """

    icons_object.load_icons(PROTEUS_SAMPLE_ICONS_PATH / "icons_valid_empty")
    assert (
        len(icons_object._icons_paths) == 0
    ), "Icons types were found in the 'icons.xml' file"


@pytest.mark.parametrize("sample_dir", ["icons_missing_file", "nonexistingdir"])
def test_icons_load_fail(icons_object: Icons, sample_dir: str) -> None:
    """
    Test that the icons are loaded correctly with a directory that does not contain any icons.xml file.
    """

    succes: bool = icons_object.load_icons(PROTEUS_SAMPLE_ICONS_PATH / sample_dir)

    assert (
        not succes
    ), f"Icons were loaded from a directory that is not supposed to be valid, directory: '{sample_dir}'"


def test_icons_load_fail_none(icons_object: Icons) -> None:
    """
    Test that the icons are loaded correctly with a directory that does not contain any icons.xml file.
    """

    succes: bool = icons_object.load_icons(None)

    assert (
        not succes
    ), f"Icons were loaded from a directory that is not supposed to be valid, directory: 'None'"
