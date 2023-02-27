# ==========================================================================
# File: markdown_property.py
# Description: PROTEUS markdown property
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


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.string_property import StringProperty
from proteus.model.properties import MARKDOWN_PROPERTY_TAG

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