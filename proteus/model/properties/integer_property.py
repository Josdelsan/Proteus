# ==========================================================================
# File: integer_property.py
# Description: PROTEUS integer property
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
from proteus.model.properties import INTEGER_PROPERTY_TAG

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: IntegerProperty
# Description: Dataclass for PROTEUS integer properties
# Date: 15/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class IntegerProperty(Property):
    """
    Class for PROTEUS integer properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = INTEGER_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the integer passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            # self.value = int(self.value) cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            # TODO if self.value (str) is a float (x.y), will fail. Should we allow floats? (int(float(self.value)))
            object.__setattr__(self, 'value', int(self.value))
            
        except ValueError:
            log.warning(f"Integer property '{self.name}': Wrong format ({self.value}) -> assigning 0 value")
            # self.value = int(0) cannot be used when frozen=True
            object.__setattr__(self, 'value', int(0))

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value)