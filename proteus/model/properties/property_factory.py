# ==========================================================================
# File: property_factory.py
# Description: PROTEUS property Factory
# Date: 27/02/2023
# Version: 0.3
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
#         José María Delgado Sánchez    
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from functools import reduce
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
from proteus.model.properties.string_property import StringProperty
from proteus.model.properties.boolean_property import BooleanProperty
from proteus.model.properties.date_property import DateProperty
from proteus.model.properties.time_property import TimeProperty
from proteus.model.properties.markdown_property import MarkdownProperty
from proteus.model.properties.integer_property import IntegerProperty
from proteus.model.properties.float_property import FloatProperty
from proteus.model.properties.enum_property import EnumProperty
from proteus.model.properties.file_property import FileProperty
from proteus.model.properties.url_property import UrlProperty
from proteus.model.properties.classlist_property import ClassListProperty

from proteus.model import NAME_TAG, CATEGORY_TAG

from proteus.model.properties import \
    CLASS_TAG,                       \
    DEFAULT_CATEGORY,                \
    CHOICES_TAG

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: PropertyFactory
# Description: Factory class for PROTEUS properties
# Date: 30/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class PropertyFactory:
    """
    Factory class for PROTEUS properties.
    """
    # Dictionary of valid property types and classes (class attribute)
    # Note the type hint type[Property] for the dictionary
    # https://adamj.eu/tech/2021/05/16/python-type-hints-return-class-not-instance/
    propertyFactory: dict[str,type[Property]] = {
        BooleanProperty.element_tagname   : BooleanProperty,
        StringProperty.element_tagname    : StringProperty,
        DateProperty.element_tagname      : DateProperty,
        TimeProperty.element_tagname      : TimeProperty,
        MarkdownProperty.element_tagname  : MarkdownProperty,
        IntegerProperty.element_tagname   : IntegerProperty,
        FloatProperty.element_tagname     : FloatProperty,
        EnumProperty.element_tagname      : EnumProperty,
        FileProperty.element_tagname      : FileProperty,
        UrlProperty.element_tagname       : UrlProperty,
        ClassListProperty.element_tagname : ClassListProperty    
    }


    @classmethod
    def create( cls, element : ET._Element ) -> Property | None:
        """
        Factory class method for PROTEUS properties.
        :param element: XML element with the property.
        :return: Property object or None if the property type is not valid.
        """
        # Check it is one of the valid property types
        try:
            property_class = cls.propertyFactory[element.tag]
        except KeyError:
            log.warning(f"<{element.tag}> is not a valid PROTEUS property type -> ignoring invalid property")
            return None

        # Get name (checked in property constructors)
        name = element.attrib.get(NAME_TAG)

        # Get category (checked in property constructors)
        category = element.attrib.get(CATEGORY_TAG, DEFAULT_CATEGORY)

        # Get value (checked in property constructors)
        if( property_class is ClassListProperty ):
            # We need to collect the list of class names,
            # put them toghether in a space-separated string
            # and use it as property value. In order to do so, we use
            # reduce (from functools) and a lambda expression.
            if element.findall(CLASS_TAG):
                class_names = map(lambda e: e.text, element.findall(CLASS_TAG))
                value = reduce(lambda c1, c2: c1+' '+c2, class_names) if class_names else str()
            else:
                value = str()
        else:
            # Value could be empty
            value = str(element.text)

        # Create and return the property object

        # Special case: EnumProperty
        if( property_class is EnumProperty ):
            # We need to collect its choices
            choices = element.attrib.get(CHOICES_TAG, str())
            return EnumProperty(name, category, value, choices)

        # Ordinary case: rest of property classes
        return property_class(name, category, value)