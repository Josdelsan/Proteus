# ==========================================================================
# File: float_property.py
# Description: PROTEUS float property
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

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model.properties.property import Property
from proteus.model.properties import FLOAT_PROPERTY_TAG



# --------------------------------------------------------------------------
# Class: FloatProperty
# Description: Dataclass for PROTEUS float properties
# Date: 15/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class FloatProperty(Property):
    """
    Class for PROTEUS real properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = FLOAT_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the float passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            # self.value = float(self.value) cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'value', float(self.value))
        except ValueError:
            proteus.logger.warning(f"Float property '{self.name}': Wrong format ({self.value}) -> assigning 0.0 value")
            #self.value = float(0.0) cannot be used when frozen=True
            object.__setattr__(self, 'value', float(0.0))

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value)