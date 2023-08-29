# ==========================================================================
# File: classlist_property.py
# Description: PROTEUS class list property
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
from proteus.model.properties import CLASSLIST_PROPERTY_TAG, CLASS_TAG


# --------------------------------------------------------------------------
# Class: ClassListProperty
# Description: Class for PROTEUS ClassList properties
# Date: 22/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class ClassListProperty(Property):
    """
    Class for PROTEUS class-tag-list properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = CLASSLIST_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the list of space-separated PROTEUS class names.
        """
        # Superclass validation        
        super().__post_init__()

        # TODO: how can we check whether class names are valid at this moment?

    def get_class_list(self) -> list[str]:
        """
        It generates a list of strings from the space-separated 
        string with the class names.
        :return: list of strings with the class names.
        """
        # use split() without arguments to get an empty list if string is empty
        return self.value.split()

    def generate_xml_value(self, property_element:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        In this case, it adds one <class> child for each class tag.
        """
        for class_name in self.get_class_list():
            class_element = ET.SubElement(property_element, CLASS_TAG)
            class_element.text = class_name

        return str()