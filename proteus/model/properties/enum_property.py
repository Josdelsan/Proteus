# ==========================================================================
# File: enum_property.py
# Description: PROTEUS enum property
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

from proteus.model.properties import Property
from proteus.model.properties import ENUM_PROPERTY_TAG, CHOICES_ATTRIBUTE

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------


# logging configuration
log = logging.getLogger(__name__)

@dataclass(frozen=True)
class EnumProperty(Property):
    """
    Class for PROTEUS enumerated properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = ENUM_PROPERTY_TAG
    value           : str

    # dataclass instance attributes
    choices: str = str()

    def __post_init__(self) -> None:
        """
        It validates that the value is one of the choices and that the choices are not empty.
        """
        # Superclass validation        
        super().__post_init__()
        object.__setattr__(self, 'value', str(self.value))

        # Parse choices set
        # use split() without arguments to get an empty list if string is empty
        _choices = str(self.choices).split()

        # Validate value and choices
        try:
            if (not bool(self.value)) and (not bool(_choices)):
                raise ValueError
        except ValueError:
            log.warning(f"Enum property '{self.name}': empty set of choices and no value, please check.")
            return

        # Validate value (spaces into underscores)
        try:
            if (' ' in self.value):
                raise ValueError
        except ValueError:
            log.warning(f"Enum property '{self.name}': values cannot contain spaces -> replaced by underscores")
            # self.value = self.value.replace(' ', '_') cannot be used when frozen=True
            object.__setattr__(self, 'value', self.value.replace(' ', '_'))

        # Validate choices (value is not empty)
        try:
            if not bool(_choices):
                raise ValueError
        except ValueError:
            log.warning(f"Enum property '{self.name}': Empty set of choices -> using value '{self.value}' as the only choice")
            # self.choices = self.value cannot be used when frozen=True
            object.__setattr__(self, 'choices', self.value)


        # Validate value (choices are not empty)
        try:
            if self.value not in self.get_choices_as_list():
                raise ValueError
        except ValueError:
            log.warning(f"Enum property '{self.name}': invalid value -> assigning first choice '{_choices[0]}'")
            # self.value = random.choice(list(_choices)) if bool(_choices) else str() cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'value', _choices[0])


    def get_choices_as_list(self) -> list[str]:
        """
        It generates a list of strings from the space-separated 
        string with the enumerated choices.
        :return: list of strings with the enumerated choices.
        """
        # use split() without arguments to get an empty list if string is empty
        return str(self.choices).split()

    def generate_xml_value(self, property_element:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element and
        the list of choices as the 'choices' attribute of the XML element.
        """
        property_element.set(CHOICES_ATTRIBUTE, self.choices)
        return self.value