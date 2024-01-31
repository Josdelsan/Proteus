# ==========================================================================
# File: file_property.py
# Description: PROTEUS file property
# Date: 27/02/2023
# Version: 0.3
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
#         José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.property import Property
from proteus.model.properties import FILE_PROPERTY_TAG

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: FileProperty
# Description: Dataclass for PROTEUS file properties
# Date: 22/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class FileProperty(Property):
    """
    Class for PROTEUS file properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname: ClassVar[str] = FILE_PROPERTY_TAG
    value: str

    def __post_init__(self) -> None:
        """
        It validates the file path passed as a string.
        """
        # Superclass validation
        super().__post_init__()

        # Default value
        _value: str = str(self.value)

        # Value validation
        try:
            # If the value is a string, it is validated
            if isinstance(self.value, str):
                _value = self.value
            else:
                raise TypeError
        except TypeError:
            log.warning(
                f"File property '{self.name}': Wrong type ({type(self.value)}). Please use str -> assigning empty value"
            )
        finally:
            # self.value = _value cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, "value", _value)

        # NOTE: value validation is not performed since it stores
        # the file name and extension. Full path cannot be validated.

    @property
    def is_file(self) -> bool:
        return Path(self.value).is_file()

    def generate_xml_value(self, _: ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """

        _value = self.value

        # Check the value is not empty when required
        if self.required:
            assert not (
                _value == None or _value == ""
            ), f"fileProperty '{self.name}' is required but has no value"

        return ET.CDATA(_value)
