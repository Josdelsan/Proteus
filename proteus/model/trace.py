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
    NAME_ATTR,
    CATEGORY_ATTR,
    SOURCE_ATTR,
    ACCEPTED_SOURCES_ATTR,
    TRACE_PROPERTY_TAG,
    TRACE_TAG,
    DEFAULT_TRACE_NAME,
    DEFAULT_TRACE_CATEGORY,
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
    acceptedSources: List[ProteusClassTag] = field(default_factory=list)
    sources: List[ProteusID] = field(default_factory=list)

    # --------------------------------------------------------------------------
    # Method: __post_init__
    # Description: It validates name, category and value of an PROTEUS trace.
    # Date: 23/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __post_init__(self) -> None:
        """
        It validates name, category, acceptedSources and value of an PROTEUS trace.
        """
        # Name validation
        if not self.name:
            log.warning(
                f"PROTEUS trace must have a '{NAME_ATTR}' attribute -> assigning '{DEFAULT_TRACE_NAME}' as name"
            )
            # self.name = DEFAULT_NAME cannot be used when frozen=True
            # https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
            object.__setattr__(self, "name", DEFAULT_TRACE_NAME)

        # Category validation
        if not self.category:
            # self.category = DEFAULT_CATEGORY cannot be used when frozen=True
            object.__setattr__(self, "category", DEFAULT_TRACE_CATEGORY)

        # Accepted sources validation
        if not isinstance(self.acceptedSources, list):
            log.warning(
                f"PROTEUS trace '{self.name}' must have a list of accepted sources -> assigning :Proteus-any as accepted sources"
            )
            # self.acceptedSources = list() cannot be used when frozen=True
            object.__setattr__(self, "acceptedSources", list().append(PROTEUS_ANY))

        # Value validation
        if not isinstance(self.sources, list):
            log.warning(
                f"PROTEUS trace '{self.name}' must have a list of sources -> assigning an empty list"
            )
            # self.sources = list() cannot be used when frozen=True
            object.__setattr__(self, "sources", list())

    # --------------------------------------------------------------------------
    # Method: clone
    # Description: It clones the trace with new sources if it is not None.
    # Date: 23/10/2023
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def clone(self, new_sources: List = None) -> "Trace":
        """
        It clones the trace with new sources if it is not None.
        The new sources must be provided as a list of ProteusID.
        :param new_sources: new sources for the trace.
        :return: a copy of the trace with the new sources.
        """
        if new_sources is None:
            return replace(self)

        return replace(self, sources=new_sources)

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
        trace_property_element.set(NAME_ATTR, self.name)
        trace_property_element.set(CATEGORY_ATTR, self.category)
        trace_property_element.set(ACCEPTED_SOURCES_ATTR, "".join(self.acceptedSources))

        # Create each trace tag and set its attribute
        for source in self.sources:
            trace_element: ET._Element = ET.Element(TRACE_TAG)
            trace_element.set(SOURCE_ATTR, source)
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
            NAME_ATTR, DEFAULT_TRACE_NAME
        )

        # Get category
        category: AnyStr | None = trace_property_element.attrib.get(
            CATEGORY_ATTR, DEFAULT_TRACE_CATEGORY
        )

        # Get accepted sources
        accepted_sources: List | None = trace_property_element.attrib.get(
            ACCEPTED_SOURCES_ATTR, "".join(PROTEUS_ANY)
        ).split()

        # Get sources
        traces = list()
        for trace in trace_property_element.findall(TRACE_TAG):
            source: ProteusID = trace.attrib.get(SOURCE_ATTR)

            if source is None:
                log.warning(
                    f"PROTEUS trace '{name}' has a trace without a source -> ignoring it"
                )
                continue

            traces.append(source)

        return cls(
            name=name,
            category=category,
            sources=traces,
            acceptedSources=accepted_sources,
        )
