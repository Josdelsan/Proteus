# ==========================================================================
# File: boolean_property.py
# Description: PROTEUS boolean property
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
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model.properties.property import Property
from proteus.model.properties import BOOLEAN_PROPERTY_TAG

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: BooleanProperty
# Description: Dataclass for PROTEUS boolean properties
# Date: 15/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class BooleanProperty(Property):
    """
    Class for PROTEUS boolean properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = BOOLEAN_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the boolean passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            if not self.value:
                raise ValueError
            if self.value.lower() not in ['true','false']:
                raise ValueError
            # self.value = bool(self.value.lower() == "true") cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'value', bool(self.value.lower() == "true"))
        except ValueError:
            log.warning(f"Boolean property '{self.name}': Wrong format ({self.value}). Please use 'true' or 'false' -> assigning False value")
            # self.value = bool(False) cannot be used when frozen=True
            object.__setattr__(self, 'value', bool(False))

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value).lower()