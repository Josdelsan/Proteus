# ==========================================================================
# File: trace.py
# Description: PROTEUS trace
# Date: 23/10/2023
# Version: 0.4
# Author: José María Delgado Sánchez
# ==========================================================================
# Author: José María Delgado Sánchez
# Date: 12/09/2024
# Description: Trace now inherits from Property
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, ClassVar
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.property import Property
from proteus.model import (
    ProteusID,
    ProteusClassTag,
    NAME_ATTRIBUTE,
    TARGET_ATTRIBUTE,
    ACCEPTED_TARGETS_ATTRIBUTE,
    EXCLUDED_TARGETS_ATTRIBUTE,
    MAX_TARGETS_NUMBER_ATTRIBUTE,
    TRACE_TYPE_ATTRIBUTE,
    PROTEUS_ANY,
)
from proteus.model.properties import (
    TRACE_PROPERTY_TAG,
    TRACE_TAG,
    NO_TARGETS_LIMIT,
    DEFAULT_TRACE_TYPE,
    DEFAULT_TRACE_NAME,
    DEFAULT_TRACE_CATEGORY,
)

# logging configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: Trace
# Description: Dataclass for PROTEUS traces
# Date: 23/10/2023
# Version: 0.2
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TraceProperty(Property):
    """
    Class for PROTEUS traces.
    """

    # dataclass instance attributes
    element_tagname: ClassVar[str] = TRACE_PROPERTY_TAG
    acceptedTargets: List[ProteusClassTag] = field(default_factory=list)
    excludedTargets: List[ProteusClassTag] = field(default_factory=list)
    type: str = str(DEFAULT_TRACE_TYPE)
    value: List[ProteusID] = field(default_factory=list)  # targets
    max_targets_number: int = NO_TARGETS_LIMIT

    # --------------------------------------------------------------------------
    # Method: __post_init__
    # Description: It validates name, category and value of an PROTEUS trace.
    # Date: 23/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __post_init__(self) -> None:
        """
        It validates name, category, acceptedTargets and value of an PROTEUS trace.
        """
        # Name validation
        if not self.name:
            log.warning(
                f"PROTEUS trace must have a '{NAME_ATTRIBUTE}' attribute -> assigning '{DEFAULT_TRACE_NAME}' as name"
            )
            # self.name = DEFAULT_NAME cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, "name", DEFAULT_TRACE_NAME)

        # Category validation
        if not self.category:
            # self.category = DEFAULT_CATEGORY cannot be used when frozen=True
            object.__setattr__(self, "category", DEFAULT_TRACE_CATEGORY)

        # Accepted targets validation
        if not isinstance(self.acceptedTargets, list) or len(self.acceptedTargets) == 0:
            log.warning(
                f"PROTEUS trace '{self.name}' must have a list of accepted targets -> assigning :Proteus-any as accepted targets"
            )
            # self.acceptedTargets = list() cannot be used when frozen=True
            object.__setattr__(self, "acceptedTargets", [PROTEUS_ANY])

        if not isinstance(self.excludedTargets, list):
            log.debug(
                f"PROTEUS trace '{self.name}' must have a list of excluded targets -> assigning an empty list"
            )
            # self.excludedTargets = list() cannot be used when frozen=True
            object.__setattr__(self, "excludedTargets", list())

        # Tooltip validation
        if not self.tooltip:
            # self.tooltip = str() cannot be used when frozen=True
            object.__setattr__(self, "tooltip", str())

        # Type validation
        if not self.type:
            # self.type = DEFAULT_TYPE cannot be used when frozen=True
            object.__setattr__(self, "type", DEFAULT_TRACE_TYPE)

        # Value validation
        if not isinstance(self.value, list):
            log.warning(
                f"PROTEUS trace '{self.name}' must have a list of targets (value) -> assigning an empty list"
            )
            # self.targets = list() cannot be used when frozen=True
            object.__setattr__(self, "targets", list())

        # Max targets number validation
        if not isinstance(self.max_targets_number, int) or (
            self.max_targets_number <= 0 and self.max_targets_number != NO_TARGETS_LIMIT
        ):
            # Log warning omitted to avoid excessive logging so the user do not have to be excessively verbose when creating an archetype
            log.warning(
                f"PROTEUS trace '{self.name}' must have a max targets number -> assigning NO_TARGETS_LIMIT=-1 as max targets number"
            )

            # self.max_targets_number = NO_TARGETS_LIMIT cannot be used when frozen=True
            object.__setattr__(self, "max_targets_number", NO_TARGETS_LIMIT)

        # Ignore targets if max targets number is NO_TARGETS_LIMIT
        if (
            self.max_targets_number != NO_TARGETS_LIMIT
            and len(self.value) > self.max_targets_number
        ):
            log.warning(
                f"PROTEUS trace '{self.name}' has more targets than the max targets number -> ignoring leftover targets"
            )
            # self.targets = self.targets[:self.max_targets_number] cannot be used when frozen=True
            object.__setattr__(self, "value", self.value[: self.max_targets_number])

    # --------------------------------------------------------------------------
    # Method: generate_xml
    # Description: This template method generates the XML element for the trace.
    # Date: 23/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def generate_xml(self) -> ET._Element:
        """
        This template method generates the XML element for the trace.
        """
        trace_property_element: ET._Element = super().generate_xml()

        trace_property_element.set(
            ACCEPTED_TARGETS_ATTRIBUTE, " ".join(self.acceptedTargets)
        )

        # Create excluded targets attribute if it is not an empty list
        if len(self.excludedTargets) > 0:
            trace_property_element.set(
                EXCLUDED_TARGETS_ATTRIBUTE, " ".join(self.excludedTargets)
            )

        trace_property_element.set(TRACE_TYPE_ATTRIBUTE, self.type)

        # Create max targets number attribute if it is not NO_TARGETS_LIMIT
        if self.max_targets_number != NO_TARGETS_LIMIT:
            trace_property_element.set(
                MAX_TARGETS_NUMBER_ATTRIBUTE, str(self.max_targets_number)
            )

        return trace_property_element

    # --------------------------------------------------------------------------
    # Method: generate_xml_value
    # Description: Generates the value of the property for its XML element.
    # Date: 12/09/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def generate_xml_value(
        self, property_element: ET._Element
    ) -> str | ET.CDATA | None:
        """
        Generates the value of the property for its XML element. Creates each trace tag and sets its attribute.
        """
        # Create each trace tag and set its attribute
        for target in self.value:
            trace_element: ET._Element = ET.SubElement(property_element, TRACE_TAG)
            trace_element.set(TARGET_ATTRIBUTE, target)
            trace_element.set(TRACE_TYPE_ATTRIBUTE, self.type)

        # Returning None avoid the XML to be printed in a single line
        # https://lxml.de/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
        return None

    def compare(self, other: "TraceProperty") -> bool:
        """
        It compares the values of two TraceProperty objects.
        :param other: TraceProperty object to compare.
        :return: True if the attributes values are equal, False otherwise.
        """
        base_attributes = super().compare(other)
        return (
            base_attributes
            and self.acceptedTargets == other.acceptedTargets
            and self.excludedTargets == other.excludedTargets
            and self.type == other.type
            and self.max_targets_number == other.max_targets_number
        )