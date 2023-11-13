# ==========================================================================
# File: trace.py
# Description: PROTEUS trace
# Date: 23/10/2023
# Version: 0.3
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from dataclasses import dataclass, replace, field
from typing import List, AnyStr
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import lxml.etree as ET

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import (
    ProteusID,
    ProteusClassTag,
    NAME_ATTRIBUTE,
    CATEGORY_ATTRIBUTE,
    TARGET_ATTRIBUTE,
    ACCEPTED_TARGETS_ATTRIBUTE,
    TRACE_PROPERTY_TAG,
    TRACE_TYPE_ATTRIBUTE,
    TRACE_TAG,
    DEFAULT_TRACE_NAME,
    DEFAULT_TRACE_CATEGORY,
    DEFAULT_TRACE_TYPE,
    PROTEUS_ANY,
)

# logging configuration
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Class: Trace
# Description: Dataclass for PROTEUS traces
# Date: 23/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Trace:
    """
    Class for PROTEUS traces.
    """

    # dataclass instance attributes
    name: str = str(DEFAULT_TRACE_NAME)
    category: str = str(DEFAULT_TRACE_CATEGORY)
    acceptedTargets: List[ProteusClassTag] = field(default_factory=list)
    type: str = str(DEFAULT_TRACE_TYPE)
    targets: List[ProteusID] = field(default_factory=list)

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
        if not isinstance(self.acceptedTargets, list):
            log.warning(
                f"PROTEUS trace '{self.name}' must have a list of accepted targets -> assigning :Proteus-any as accepted targets"
            )
            # self.acceptedTargets = list() cannot be used when frozen=True
            object.__setattr__(self, "acceptedTargets", list().append(PROTEUS_ANY))

        # Type validation
        if not self.type:
            # self.type = DEFAULT_TYPE cannot be used when frozen=True
            object.__setattr__(self, "type", DEFAULT_TRACE_TYPE)

        # Value validation
        if not isinstance(self.targets, list):
            log.warning(
                f"PROTEUS trace '{self.name}' must have a list of targets -> assigning an empty list"
            )
            # self.targets = list() cannot be used when frozen=True
            object.__setattr__(self, "targets", list())

    # --------------------------------------------------------------------------
    # Method: clone
    # Description: It clones the trace with new targets if it is not None.
    # Date: 23/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def clone(self, new_targets: List = None) -> "Trace":
        """
        It clones the trace with new targets if it is not None.
        The new targets must be provided as a list of ProteusID.
        :param new_targets: new targets for the trace.
        :return: a copy of the trace with the new targets.
        """
        if new_targets is None:
            return replace(self)

        return replace(self, targets=new_targets)

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
        # Create trace property tag and set its attributes
        trace_property_element: ET._Element = ET.Element(TRACE_PROPERTY_TAG)
        trace_property_element.set(NAME_ATTRIBUTE, self.name)
        trace_property_element.set(CATEGORY_ATTRIBUTE, self.category)
        trace_property_element.set(ACCEPTED_TARGETS_ATTRIBUTE, "".join(self.acceptedTargets))
        trace_property_element.set(TRACE_TYPE_ATTRIBUTE, self.type)

        # Create each trace tag and set its attribute
        for target in self.targets:
            trace_element: ET._Element = ET.Element(TRACE_TAG)
            trace_element.set(TARGET_ATTRIBUTE, target)
            trace_element.set(TRACE_TYPE_ATTRIBUTE, self.type)
            trace_property_element.append(trace_element)

        return trace_property_element

    # --------------------------------------------------------------------------
    # Method: create (class method)
    # Description: It creates a trace from an XML element.
    # Date: 23/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @classmethod
    def create(cls, trace_property_element: ET._Element) -> "Trace":
        """
        It creates a trace from an XML element.

        :param element: XML element with the trace.
        :return: Trace object.
        """
        # Get name
        name: AnyStr | None = trace_property_element.attrib.get(
            NAME_ATTRIBUTE, DEFAULT_TRACE_NAME
        )

        # Get category
        category: AnyStr | None = trace_property_element.attrib.get(
            CATEGORY_ATTRIBUTE, DEFAULT_TRACE_CATEGORY
        )

        # Get accepted targets
        accepted_targets: List | None = trace_property_element.attrib.get(
            ACCEPTED_TARGETS_ATTRIBUTE, [PROTEUS_ANY]
        ).split()

        # Get type
        type: AnyStr | None = trace_property_element.attrib.get(
            TRACE_TYPE_ATTRIBUTE, DEFAULT_TRACE_TYPE
        )

        # Get targets
        traces = list()
        for trace in trace_property_element.findall(TRACE_TAG):
            target: ProteusID = trace.attrib.get(TARGET_ATTRIBUTE)

            if target is None:
                log.warning(
                    f"PROTEUS trace '{name}' has a trace without a target -> ignoring it"
                )
                continue

            traces.append(target)

        return cls(
            name=name,
            category=category,
            targets=traces,
            acceptedTargets=accepted_targets,
            type=type,
        )
