# ==========================================================================
# File: property_input_factory.py
# Description: Implementation of a property input factory to handle the
#              creation of property input widgets.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

# Properties imports
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

# Property input imports
from proteus.views.utils.forms.properties.property_input import PropertyInput
from proteus.views.utils.forms.properties.string_property_input import (
    StringPropertyInput,
)
from proteus.views.utils.forms.properties.boolean_property_input import (
    BooleanPropertyInput,
)
from proteus.views.utils.forms.properties.date_property_input import DatePropertyInput
from proteus.views.utils.forms.properties.markdown_property_input import (
    MarkdownPropertyInput,
)
from proteus.views.utils.forms.properties.integer_property_input import (
    IntegerPropertyInput,
)
from proteus.views.utils.forms.properties.float_property_input import (
    FloatPropertyInput,
)
from proteus.views.utils.forms.properties.enum_property_input import EnumPropertyInput
from proteus.views.utils.forms.properties.file_property_input import FilePropertyInput
from proteus.views.utils.forms.properties.url_property_input import UrlPropertyInput

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: PropertyInputFactory
# Description: Implementation of a property input factory to handle the
#              creation of property input widgets.
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class PropertyInputFactory:
    """
    Implementation of a property input factory to handle the creation of
    property input widgets.
    """

    # Map of property types to input creation functions
    property_input_map: Dict[type[Property], type[PropertyInput]] = {
        StringProperty: StringPropertyInput,
        DateProperty: DatePropertyInput,
        MarkdownProperty: MarkdownPropertyInput,
        BooleanProperty: BooleanPropertyInput,
        FloatProperty: FloatPropertyInput,
        IntegerProperty: IntegerPropertyInput,
        EnumProperty: EnumPropertyInput,
        FileProperty: FilePropertyInput,
        UrlProperty: UrlPropertyInput,
    }

    # ----------------------------------------------------------------------
    # Method     : create
    # Description: Creates a property input widget for the given property.
    # Date       : 26/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create(property: Property) -> PropertyInput:
        try:
            property_input_class = PropertyInputFactory.property_input_map[type(property)]
            return property_input_class(property)
        except KeyError:
            log.error(f"Property input widget for {type(property)} was not found")
            return None
