# ==========================================================================
# File: date_property.py
# Description: PROTEUS date property
# Date: 27/02/2023
# Version: 0.3
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
#         José María Delgado Sánchez    
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import datetime
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
from proteus.model.properties import DATE_PROPERTY_TAG, DATE_FORMAT

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: DateProperty
# Description: Dataclass for PROTEUS date properties (YYYY-MM-DD)
# Date: 15/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class DateProperty(Property):
    """
    Class for PROTEUS date properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = DATE_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the date passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            # self.value = datetime.datetime.strptime(self.value, DATE_FORMAT).date() cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'value', datetime.datetime.strptime(self.value, DATE_FORMAT).date())
        except ValueError:
            log.warning(f"Date property '{self.name}': Wrong format ({self.value}). Please use YYYY-MM-DD -> assigning today's date")
            # self.value = datetime.date.today() cannot be used when frozen=True
            object.__setattr__(self, 'value', datetime.date.today())

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return self.value.strftime(DATE_FORMAT)