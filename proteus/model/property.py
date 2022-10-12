# ==========================================================================
# File: property.py
# Description: an abstract PROTEUS property
# Date: 07/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================
# Update: 30/08/2022 (Amador)
# Description:
# - Added support for property categories.
# - Added PropertyFactory class to avoid Property class definition to be
#   splitted into two parts.
# ==========================================================================
# Update: 17/09/2022 (Amador)
# Description:
# - Added default category value in constructors.
# ==========================================================================
# Update: 29/09/2022 (Amador)
# Description:
# - Code review.
# - Argument "value" is always a string in __init()__, its conversion to
#   the right type is checked in each subclass.
# - TODO: type conversions raise ValueError exceptions that must be caught
#         in future versions, set a default value, and send an error message
#         to the log.
# ==========================================================================
# Update: 12/10/2022 (Amador)
# Description:
# - Code review.
# - Exception handling in type conversions.
# - RealProperty -> FloatProperty.
# - lxml is not very MyPy-friendly. Installed lxlm-stub.
# - TODO: finish review of PropertyFactory create method.
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import random
import datetime
from pathlib import Path
from functools import reduce
from abc import ABC, abstractmethod

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import validators
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model import DEFAULT_CATEGORY, CATEGORY_TAG, NAME_TAG

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

BOOLEAN_PROPERTY_TAG    = 'booleanProperty'
STRING_PROPERTY_TAG     = 'stringProperty'
DATE_PROPERTY_TAG       = 'dateProperty'
TIME_PROPERTY_TAG       = 'timeProperty'
MARKDOWN_PROPERTY_TAG   = 'markdownProperty'
INTEGER_PROPERTY_TAG    = 'integerProperty'
FLOAT_PROPERTY_TAG      = 'floatProperty'
ENUM_PROPERTY_TAG       = 'enumProperty'
URL_PROPERTY_TAG        = 'urlProperty'
FILE_PROPERTY_TAG       = 'fileProperty'
CLASSLIST_PROPERTY_TAG  = 'classListProperty'
CHOICES_TAG             = 'choices'
CLASS_TAG               = 'class'

# --------------------------------------------------------------------------
# Class: Property (abstract)
# Description: Abstract class for PROTEUS properties
# Date: 22/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------
# TODO: this class should be inmutable in the future, maybe using
#       @dataclass(frozen=True) or other approach.
# --------------------------------------------------------------------------

class Property(ABC):
    """
    Abstract class for PROTEUS properties.
    """

    def __init__(self, name: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes an abstract PROTEUS property. Value is set in subclasses.
        """
        super().__init__()

        # Check name is not the empty string
        assert name, \
            f"Unnamed properties are not valid in PROTEUS."

        # Set name and category (value is set in subclasses)
        self.name     : str = name
        self.category : str = category

    def generate_xml(self) -> ET.Element:
        """
        This template method generates the XML element for the property.
        """
        # element_tagname is a class attribute of each concrete subclass
        property_element : ET._Element = ET.Element(self.element_tagname)
        property_element.set(NAME_TAG, self.name)
        property_element.set(CATEGORY_TAG, self.category)
        # generate_xml_value() is defined in subclasses
        property_element.text = self.generate_xml_value(property_element)

        return property_element

    @abstractmethod
    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        Depending on the type of property, it can be a string or
        a CDATA section.
        """
        pass

# --------------------------------------------------------------------------
# Class: StringProperty
# Description: Class for PROTEUS string properties
# Date: 22/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class StringProperty(Property):
    """
    Class for PROTEUS string properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = STRING_PROPERTY_TAG

    def __init__(self, name: str, value: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the string property.
        """
        super().__init__(name, category)

        self.value : str = str(value) # implicit type check and conversion

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return ET.CDATA(self.value)

# --------------------------------------------------------------------------
# Class: DateProperty
# Description: Class for PROTEUS date properties (YYYY-MM-DD)
# Date: 22/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class DateProperty(Property):
    """
    Class for PROTEUS date properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = DATE_PROPERTY_TAG

    def __init__(self, name: str, value: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the date property.
        """
        super().__init__(name, category)

        # Convert string to date and check it is correct
        self.value : datetime.date
        try:
            self.value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            proteus.logger.error(f"Date property '{self.name}': Wrong format ({value}). Please use YYYY-MM-DD -> assigning today's date")
            self.value = datetime.date.today()

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return self.value.strftime('%Y-%m-%d')

# --------------------------------------------------------------------------
# Class: TimeProperty
# Description: Class for PROTEUS time properties (hh:mm:ss)
# Date: 18/09/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class TimeProperty(Property):
    """
    Class for PROTEUS time properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = TIME_PROPERTY_TAG

    def __init__(self, name: str, value: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the time property.
        """
        super().__init__(name, category)

        # Convert string to time and check it is correct
        self.value : datetime.time
        try:
            self.value = datetime.datetime.strptime(value, '%H:%M:%S').time()
        except ValueError:
            proteus.logger.error(f"Time property '{self.name}': Wrong format ({value}). Please use HH:MM:SS -> assigning now's time")
            self.value = datetime.datetime.now().time()

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return self.value.strftime('%H:%M:%S')

# --------------------------------------------------------------------------
# Class: MarkdownProperty
# Description: Class for PROTEUS markdown properties
# Date: 22/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class MarkdownProperty(Property):
    """
    Class for PROTEUS markdown properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = MARKDOWN_PROPERTY_TAG

    def __init__(self, name: str, value: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the markdown property.
        """
        super().__init__(name, category)

        self.value : str = str(value) # implicit type check and conversion

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return ET.CDATA(self.value)

# --------------------------------------------------------------------------
# Class: IntegerProperty
# Description: Class for PROTEUS integer properties
# Date: 22/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class IntegerProperty(Property):
    """
    Class for PROTEUS integer properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = INTEGER_PROPERTY_TAG

    def __init__(self, name: str, value: int, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the interger property.
        """
        super().__init__(name, category)

        # Convert string to int and check it is correct
        self.value : int
        try:
            self.value = int(value)
        except ValueError:
            proteus.logger.error(f"Integer property '{self.name}': Wrong format ({value}) -> assigning 0 value")
            self.value = int(0)

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value)

# --------------------------------------------------------------------------
# Class: FloatProperty
# Description: Class for PROTEUS float properties
# Date: 17/09/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class FloatProperty(Property):
    """
    Class for PROTEUS real properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = FLOAT_PROPERTY_TAG

    def __init__(self, name: str, value: float, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the real property.
        """
        super().__init__(name, category)

        # Convert string to float and check it is correct
        self.value : float
        try:
            self.value = float(value)
        except ValueError:
            proteus.logger.error(f"Float property '{self.name}': Wrong format ({value}) -> assigning 0.0 value")
            self.value = float(0.0)

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value)

# --------------------------------------------------------------------------
# Class: BooleanProperty
# Description: Class for PROTEUS boolean properties
# Date: 17/09/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class BooleanProperty(Property):
    """
    Class for PROTEUS boolean properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = BOOLEAN_PROPERTY_TAG

    def __init__(self, name: str, value: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the boolean property.
        """
        super().__init__(name, category)

        # Convert string to bool and check it is correct
        self.value : bool
        try:
            if value.lower() not in ['true','false']:
                raise ValueError
            self.value = bool(value.lower() == "true")
        except ValueError:
            proteus.logger.error(f"Boolean property '{self.name}': Wrong format ({value}). Please use 'true' or 'false' -> assigning False value")
            self.value = bool(False)

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value).lower()

# --------------------------------------------------------------------------
# Class: UrlProperty
# Description: Class for PROTEUS url properties
# Date: 22/08/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class UrlProperty(Property):
    """
    Class for PROTEUS url properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = URL_PROPERTY_TAG

    def __init__(self, name: str, value: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the url property.
        """
        super().__init__(name, category)

        # Convert string to bool and check it is correct
        self.value : str = str(value)
        try:
            if not validators.url(value):
                raise ValueError
        except ValueError:
            proteus.logger.error(f"URL property '{self.name}': Wrong format ({value}). Please check.")

    def generate_xml_value(self, _:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return ET.CDATA(self.value)

# --------------------------------------------------------------------------
# Class: EnumProperty
# Description: Class for PROTEUS enumerated properties
# Date: 17/09/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

class EnumProperty(Property):
    """
    Class for PROTEUS enumerated properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = ENUM_PROPERTY_TAG

    def __init__(self, name: str, value: str, choices: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the enumerated property.
        """
        super().__init__(name, category)

        # Parse choices and check they are not empty
        self.choices : set[str] = set( choices.split(' ') )

        try:
            if not len(self.choices):
                raise ValueError
        except ValueError:
            proteus.logger.error(f"Enum property '{self.name}': Empty set of choices -> assigning value choice")
            self.choices = {value}

        # Get value and check it is in choices
        self.value : str = value

        try:
            if value not in self.choices:
                raise ValueError
        except ValueError:
            proteus.logger.error(f"Enum property '{self.name}': invalid value -> assigning random choice")
            self.value = random.choice(list(self.choices))

    def get_choices_as_str(self) -> str:
        return reduce(lambda c1, c2 : c1 + ' ' + c2, self.choices)

    def generate_xml_value(self, property_element:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        It also generates the list of choices as the 'choices' attribute
        using reduce (from functools) and a lambda expression.
        """
        property_element.set(CHOICES_TAG, self.get_choices_as_str())
        return str(self.value)

# --------------------------------------------------------------------------
# Class: ClassListProperty
# Description: Class for PROTEUS ClassList properties
# Date: 22/08/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

class ClassListProperty(Property):
    """
    Class for PROTEUS class-tag-list properties.
    """

    # XML element tag name for this class of property (class attribute)
    element_tagname : str = CLASSLIST_PROPERTY_TAG

    def __init__(self, name: str, value: str, category: str = DEFAULT_CATEGORY) -> None:
        """
        It initializes the class-tag list property.
        """
        super().__init__(name, category)

        # Parse value and get class tags set (it could be empty)
        self.value : list[str] = value.split(' ')

        # TODO: can we check class tags are valid at this moment?

    def generate_xml_value(self, property_element:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        In this case, it adds one <class> child for each class tag.
        """
        class_tag : str
        for class_tag in self.value:
            class_element : ET._Element = ET.SubElement(property_element, CLASS_TAG)
            class_element.text = class_tag

        return str("")

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
    propertyFactory : dict[str,type[Property]] = {
        BooleanProperty.element_tagname   : BooleanProperty,
        StringProperty.element_tagname    : StringProperty,
        DateProperty.element_tagname      : DateProperty,
        TimeProperty.element_tagname      : TimeProperty,
        MarkdownProperty.element_tagname  : MarkdownProperty,
        IntegerProperty.element_tagname   : IntegerProperty,
        FloatProperty.element_tagname     : FloatProperty,
        EnumProperty.element_tagname      : EnumProperty,
        UrlProperty.element_tagname       : UrlProperty,
        ClassListProperty.element_tagname : ClassListProperty,
        # TODO remove it in the future when we'll be sure
        # we don't need it (use UrlProperty instead)
        'fileProperty'                   : None
    }

    @classmethod
    def create( cls, element : ET._Element ) -> Property:
        """
        Factory class method for PROTEUS properties.
        """
        # Check it is one of the valid property types
        assert element.tag in cls.propertyFactory.keys(), \
            f"<{element.tag}> is not a valid PROTEUS property type"

        # Check it has a name attribute
        assert element.attrib.get(NAME_TAG, None) is not None, \
             f"PROTEUS properties must have a 'name' attribute"

        # Look up the class property in the factory dictionary
        property_class : type[Property] = cls.propertyFactory[element.tag]

        # Extract name and value from XML element
        name  : str = element.attrib[NAME_TAG]
        value : str
        if( property_class is ClassListProperty ):
            # We need to collect the list of class tag names,
            # put them toghether in a space-separated string
            # and use it as its value. In order to do so, we use
            # reduce (from functools) and a lambda expression.
            value = reduce(lambda e1, e2 : e1.text + ' ' + e2.text, element.findall(CLASS_TAG))
        else:
            value = element.text

        # Use get on attrib dictionary to provide default value
        # 'general' if key is missing
        category : str = element.attrib.get(CATEGORY_TAG, DEFAULT_CATEGORY)

        # Special case: EnumProperty
        if( property_class is EnumProperty ):
            # We need to collect its choices
            choices : str = element.attrib.get(CHOICES_TAG, None)
            return EnumProperty(name, value, choices, category)

        # Ordinary case: rest of property classes
        # Create and return the property object
        return property_class(name, value, category)
