# ==========================================================================
# File: time_property.py
# Description: PROTEUS time property
# Date: 27/02/2023
# Version: 0.3
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
#         José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from datetime import datetime, time
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
from proteus.model.properties import TIME_PROPERTY_TAG, TIME_FORMAT


# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: TimeProperty
# Description: Dataclass for PROTEUS time properties (hh:mm:ss)
# Date: 15/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TimeProperty(Property):
    """
    Class for PROTEUS time properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname: ClassVar[str] = TIME_PROPERTY_TAG
    value: time

    def __post_init__(self) -> None:
        """
        It validates the time passed as a string.
        """
        # Superclass validation
        super().__post_init__()

        # Default value
        _value: time = datetime.now().time()

        # Value validation
        try:
            # If the value is a time, it is valid
            if isinstance(self.value, time):
                _value = self.value
            # If the value is a string, convert it to time
            elif isinstance(self.value, str):
                _value = datetime.strptime(self.value, TIME_FORMAT).time()
            else:
                raise TypeError
        except ValueError:
            log.warning(
                f"Time property '{self.name}': Wrong format ({self.value}). Please use HH:MM:SS -> assigning now's time"
            )
        except TypeError:
            log.warning(
                f"Time property '{self.name}': Wrong type ({type(self.value)}). Please use str or datetime.time -> assigning now's time"
            )
        finally:
            # self.value = _value cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, "value", _value)

    def generate_xml_value(self, _: ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return self.value.strftime(TIME_FORMAT)
