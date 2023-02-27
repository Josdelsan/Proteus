# ==========================================================================
# File: __init__.py
# Description: PROTEUS 'properties' package initializer
# Date: 27/08/2022
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================


# Constants

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


# Making objects available at the package level
# Note: This must be below the constants definition
#       to avoid circular imports

from proteus.model.properties.property import Property
from proteus.model.properties.property_factory import PropertyFactory

from proteus.model.properties.boolean_property import BooleanProperty
from proteus.model.properties.string_property import StringProperty
from proteus.model.properties.date_property import DateProperty
from proteus.model.properties.time_property import TimeProperty
from proteus.model.properties.markdown_property import MarkdownProperty
from proteus.model.properties.integer_property import IntegerProperty
from proteus.model.properties.float_property import FloatProperty
from proteus.model.properties.enum_property import EnumProperty
from proteus.model.properties.url_property import UrlProperty
from proteus.model.properties.file_property import FileProperty
from proteus.model.properties.classlist_property import ClassListProperty
