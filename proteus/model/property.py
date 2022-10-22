# ==========================================================================
# File: property.py
# Description: PROTEUS properties
# Date: 22/10/2022
# Version: 0.3
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
# ==========================================================================
# Update: 15/10/2022 (Amador)
# Description:
# - Use of dataclass and __post_init()__.
# - ValueError exception handling in type conversions.
# - RealProperty -> FloatProperty.
# - Added FileProperty.
# - MarkdownProperty is now a subclass of StringProperty.
# - lxml is not very MyPy-friendly. Installed lxlm-stub in venv.
# - Added pytest parametrized tests in proteus/tests/test_properties.py.
# - Use dataclasses.replace(obj,value=new_value) to clone a property with a
#   new value. The new_value must be in string format, as in the constructor.
# ==========================================================================
# Update: 17/10/2022 (Amador)
# Description:
# - clone(new_value=None) added.
# ==========================================================================
# Update: 22/10/2022 (Amador)
# Description:
# - UrlProperty::is_valid computed property added.
# - URLs without protocol (i.e. https://) are not valid.
# - FileProperty::is_file computed property added.
# - EnumProperty: split() without arguments uses space and returns an
#   empty list if the splitted string is empty. split(' ') returns [''],
#   which is not an empty list.
# - EnumProperty assings first choice instead of random choice if value is
#   not specified.
# - EnumProperty replaces spaces by underscores in values.
# - PropertyFactory: fixed error in reduce expression for ClasslistProperty.
# ==========================================================================

# TODO: turn this module into a package (dir) and split one class per module (file)?

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import datetime
from pathlib import Path
from functools import reduce
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import Any, ClassVar, Optional

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import validators
import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
from proteus.model import CATEGORY_TAG, NAME_TAG

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

BOOLEAN_PROPERTY_TAG    = str('booleanProperty')
STRING_PROPERTY_TAG     = str('stringProperty')
DATE_PROPERTY_TAG       = str('dateProperty')
TIME_PROPERTY_TAG       = str('timeProperty')
MARKDOWN_PROPERTY_TAG   = str('markdownProperty')
INTEGER_PROPERTY_TAG    = str('integerProperty')
FLOAT_PROPERTY_TAG      = str('floatProperty')
ENUM_PROPERTY_TAG       = str('enumProperty')
URL_PROPERTY_TAG        = str('urlProperty')
FILE_PROPERTY_TAG       = str('fileProperty')
CLASSLIST_PROPERTY_TAG  = str('classListProperty')

CLASS_TAG               = str('class')
CHOICES_TAG             = str('choices')

DEFAULT_NAME            = str('unnamed')
DEFAULT_CATEGORY        = str('general')

DATE_FORMAT             = str('%Y-%m-%d')
TIME_FORMAT             = str('%H:%M:%S')

# --------------------------------------------------------------------------
# Class: Property (abstract)
# Description: Abstract dataclass for PROTEUS properties
# Date: 17/10/2022
# Version: 0.3
# Author: Amador Durán Toro
# --------------------------------------------------------------------------
# About using __post_init__: 
# https://stackoverflow.com/questions/60179799/python-dataclass-whats-a-pythonic-way-to-validate-initialization-arguments
# Dataclasses have a replace(object, value=new_value) function which returns 
# a copy of an object with a new value (similar to attr.evolve()).
# https://stackoverflow.com/questions/56402694/how-to-evolve-a-dataclass-in-python
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Property(ABC):
    """
    Abstract class for PROTEUS properties.
    """
    # dataclass instance attributes
    name     : str = str(DEFAULT_NAME)
    category : str = str(DEFAULT_CATEGORY)
    value    : Any = str()

    def __post_init__(self) -> None:
        """
        It validates name and category of an abstract PROTEUS property. 
        Value is converted into a string (just in case) and validated in subclasses.
        """      
        # Name validation
        if not self.name:
            proteus.logger.warning(f"PROTEUS properties must have a '{NAME_TAG}' attribute -> assigning '{DEFAULT_NAME}' as name")
            # self.name = DEFAULT_NAME cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'name', DEFAULT_NAME)

        # Category validation
        if not self.category:
            # self.category = DEFAULT_CATEGORY cannot be used when frozen=True
            object.__setattr__(self, 'category', DEFAULT_CATEGORY)

        # Value -> string
        object.__setattr__(self, 'value', str(self.value))

    def clone(self, new_value=None) -> 'Property':
        """
        It clones the property with a new value if it is not None.
        The new value must be provided as a string.
        """
        if new_value is None:
            return replace(self)
        
        return replace(self, value=str(new_value))

    def generate_xml(self) -> ET._Element:
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
    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        Depending on the type of property, it can be a string or
        a CDATA section.
        """

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

# --------------------------------------------------------------------------
# Class: MarkdownProperty
# Description: Dataclass for PROTEUS markdown properties
# Date: 15/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class MarkdownProperty(StringProperty):
    """
    Class for PROTEUS markdown properties. They are exactly the same as
    string properties except for the XML tag.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = MARKDOWN_PROPERTY_TAG

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
            proteus.logger.warning(f"Date property '{self.name}': Wrong format ({self.value}). Please use YYYY-MM-DD -> assigning today's date")
            # self.value = datetime.date.today() cannot be used when frozen=True
            object.__setattr__(self, 'value', datetime.date.today())

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return self.value.strftime(DATE_FORMAT)

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
    element_tagname : ClassVar[str] = TIME_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the time passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            # self.value = datetime.datetime.strptime(self.value, TIME_FORMAT).time() cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'value', datetime.datetime.strptime(self.value, TIME_FORMAT).time())
        except ValueError:
            proteus.logger.warning(f"Time property '{self.name}': Wrong format ({self.value}). Please use HH:MM:SS -> assigning now's time")
            # self.value = datetime.datetime.now().time() cannot be used when frozen=True
            object.__setattr__(self, 'value', datetime.datetime.now().time())

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return self.value.strftime(TIME_FORMAT)

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
            object.__setattr__(self, 'value', int(self.value))
        except ValueError:
            proteus.logger.warning(f"Integer property '{self.name}': Wrong format ({self.value}) -> assigning 0 value")
            # self.value = int(0) cannot be used when frozen=True
            object.__setattr__(self, 'value', int(0))

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value)

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

# --------------------------------------------------------------------------
# Class: BooleanProperty
# Description: Dataclass for PROTEUS boolean properties
# Date: 15/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class BooleanProperty(Property):
    """
    Class for PROTEUS boolean properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = BOOLEAN_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the boolean passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            if not self.value:
                raise ValueError
            if self.value.lower() not in ['true','false']:
                raise ValueError
            # self.value = bool(self.value.lower() == "true") cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'value', bool(self.value.lower() == "true"))
        except ValueError:
            proteus.logger.warning(f"Boolean property '{self.name}': Wrong format ({self.value}). Please use 'true' or 'false' -> assigning False value")
            # self.value = bool(False) cannot be used when frozen=True
            object.__setattr__(self, 'value', bool(False))

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return str(self.value).lower()

# --------------------------------------------------------------------------
# Class: FileProperty
# Description: Dataclass for PROTEUS file properties
# Date: 22/10/2022
# Version: 0.2
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class FileProperty(Property):
    """
    Class for PROTEUS file properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = FILE_PROPERTY_TAG

    def __post_init__(self) -> None:
        """
        It validates the file path passed as a string.
        """
        # Superclass validation        
        super().__post_init__()

        # Value validation
        try:
            if not (Path(self.value).exists()):
                raise ValueError
        except ValueError:
            proteus.logger.warning(f"File property '{self.name}': file '{self.value}' does not exist. Please check.")

        # TODO: how to access project path and make relative file path from it?

    @property
    def is_file(self) -> bool:
        return Path(self.value).is_file()

    def generate_xml_value(self, _:ET._Element = None) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element.
        """
        return ET.CDATA(self.value)

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

# --------------------------------------------------------------------------
# Class: EnumProperty
# Description: Dataclass for PROTEUS enumerated properties
# Date: 22/10/2022
# Version: 0.3
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class EnumProperty(Property):
    """
    Class for PROTEUS enumerated properties.
    """
    # XML element tag name for this class of property (class attribute)
    element_tagname : ClassVar[str] = ENUM_PROPERTY_TAG

    # dataclass instance attributes
    choices: str = str()

    def __post_init__(self) -> None:
        """
        It validates that the value is one of the choices and that the choices are not empty.
        """
        # Superclass validation        
        super().__post_init__()

        # Parse choices set
        # use split() without arguments to get an empty list if string is empty
        _choices = str(self.choices).split()

        # Validate value and choices
        try:
            if (not bool(self.value)) and (not bool(_choices)):
                raise ValueError
        except ValueError:
            proteus.logger.warning(f"Enum property '{self.name}': empty set of choices and no value, please check.")
            return

        # Validate value (spaces into underscores)
        try:
            if (' ' in self.value):
                raise ValueError
        except ValueError:
            proteus.logger.warning(f"Enum property '{self.name}': values cannot contain spaces -> replaced by underscores")
            # self.value = self.value.replace(' ', '_') cannot be used when frozen=True
            object.__setattr__(self, 'value', self.value.replace(' ', '_'))

        # Validate choices (value is not empty)
        try:
            if not bool(_choices):
                raise ValueError
        except ValueError:
            proteus.logger.warning(f"Enum property '{self.name}': Empty set of choices -> using value '{self.value}' as the only choice")
            # self.choices = self.value cannot be used when frozen=True
            object.__setattr__(self, 'choices', self.value)
            return

        # Validate value (choices are not empty)
        try:
            if self.value not in self.get_choices_as_set():
                raise ValueError
        except ValueError:
            proteus.logger.warning(f"Enum property '{self.name}': invalid value -> assigning first choice '{_choices[0]}'")
            # self.value = random.choice(list(_choices)) if bool(_choices) else str() cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, 'value', _choices[0])
            return

    def get_choices_as_set(self) -> set[str]:
        """
        It generates a set of strings from the space-separated 
        string with the enumerated choices.
        """
        # use split() without arguments to get an empty list if string is empty
        return set( str(self.choices).split() )

    def generate_xml_value(self, property_element:ET._Element) -> str | ET.CDATA:
        """
        It generates the value of the property for its XML element and
        the list of choices as the 'choices' attribute of the XML element.
        """
        property_element.set(CHOICES_TAG, self.choices)
        return self.value

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
        """
        # Check it is one of the valid property types
        try:
            property_class = cls.propertyFactory[element.tag]
        except KeyError:
            proteus.logger.warning(f"<{element.tag}> is not a valid PROTEUS property type -> ignoring invalid property")
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