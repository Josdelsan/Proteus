# ==========================================================================
# File: url_property.py
# Description: PROTEUS url property
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
import validators

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model.properties.property import Property
from proteus.model.properties import URL_PROPERTY_TAG



# --------------------------------------------------------------------------
# Class: UrlProperty
# Description: Dataclass for PROTEUS url properties
# Date: 22/10/2022
# Version: 0.3
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class UrlProperty(Property):
    """
    Class for PROTEUS url properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = URL_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the URL passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            if not validators.url(self.value):
                raise ValueError
        except ValueError:
            proteus.logger.warning(f"URL property '{self.name}': Wrong format ({self.value}). Please check.")

    @property
    def is_valid(self) -> bool:
        return True if validators.url(self.value) else False

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return ET.CDATA(self.value)