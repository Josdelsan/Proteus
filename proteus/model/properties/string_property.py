# ==========================================================================
# File: string_property.py
# Description: PROTEUS string property
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

from proteus.model.properties.property import Property
from proteus.model.properties import STRING_PROPERTY_TAG


# --------------------------------------------------------------------------
# Class: StringProperty
# Description: Dataclass for PROTEUS string properties
# Date: 15/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class StringProperty(Property):
    """
    Class for PROTEUS string properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname: ClassVar[str] = STRING_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        Superclass turns value into a string, there is nothing to validate.
        """
        # Superclass validation        
        super().__post_init__()

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return ET.CDATA(self.value)