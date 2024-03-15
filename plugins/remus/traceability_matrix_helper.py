# ==========================================================================
# File: traceability_matrix_helper.py
# Description: Traceability matrix helper functions and classes
# Date: 07/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import Dict, List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from lxml import etree as ET

# --------------------------------------------------------------------------
# Plugin imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Proteus imports
# --------------------------------------------------------------------------

from proteus.model import (
    ProteusClassTag,
    ProteusID,
    PROTEUS_CODE,
    PROTEUS_NAME,
    PROTEUS_DEPENDENCY,
)
from proteus.model.object import Object
from proteus.model.properties.code_property import ProteusCode
from proteus.views.components.abstract_component import ProteusComponent
from proteus.application.events import (
    OpenProjectEvent,
    AddObjectEvent,
    DeleteObjectEvent,
)


# Module configuration
log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Class: TraceabilityMatrixHelper
# Description: This class provides helper functions to work with the
#              traceability matrix.
# Date: 07/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class TraceabilityMatrixHelper(ProteusComponent):
    """
    Provides helper functions to work with the traceability matrix.

    It stores the objects in class variables referenced by class and id.
    This helps to avoid iterating all the objects every time we need to
    get the objects from a class or id. This could be done setting the
    controller instance as a class attribute during the construction
    of the component, but it may not be a good practice.

    The class provides methods to update the objects cache when the project
    is opened, a new object is added or an object is deleted. This methods
    are called when the corresponding events are triggered.

    The class also provides two XSLT functions to be used in the traceability
    matrix XSLT file. The first one gets the objects from a list of classes
    and the second one checks if a dependency exists between two objects.
    """

    # TODO: We could set the controller instance as a class attribute using
    # the __init__ method once the component is loaded in the app. This
    # would save code lines but it may not be a good practice. Consider
    # this aproach.

    objects_by_class: Dict[ProteusClassTag, List[Object]] = {}
    objects_by_id: Dict[ProteusID, Object] = {}

    # --------------------------------------------------------------------------
    # Method: __init__
    # Description: Initialize the traceability matrix helper.
    # Date: 08/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def __init__(self, parent):
        """
        It initializes the traceability matrix helper.
        """
        super().__init__(parent)

        # Subscribe to the events
        OpenProjectEvent().connect(self.update_on_project_open)
        AddObjectEvent().connect(self.update_on_add_object)
        DeleteObjectEvent().connect(self.update_on_delete_object)

    # --------------------------------------------------------------------------
    # Method: update_on_project_open
    # Description: Separate the objects by class when the project is opened
    # and store their references.
    # Date: 08/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_on_project_open(self):
        """
        Separate the objects by class when the project is opened
        and store their references.
        """

        # Clear previous data
        TraceabilityMatrixHelper.objects_by_class = {}
        TraceabilityMatrixHelper.objects_by_id = {}

        # Get all the objects
        objects: List[Object] = self._controller.get_objects()

        # Iterate all objects
        for obj in objects:

            # Store the object reference by id
            TraceabilityMatrixHelper.objects_by_id[obj.id] = obj

            # Store the object reference by class
            for _class in obj.classes:
                if _class not in TraceabilityMatrixHelper.objects_by_class:
                    TraceabilityMatrixHelper.objects_by_class[_class] = []
                TraceabilityMatrixHelper.objects_by_class[_class].append(obj)

    # --------------------------------------------------------------------------
    # Method: update_on_add_object
    # Description: Add the new object to objects cache.
    # Date: 08/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_on_add_object(self, object_id: ProteusID):
        """
        Add the new object to objects cache.
        """
        obj = self._controller.get_element(object_id)

        # Store the object reference by id
        TraceabilityMatrixHelper.objects_by_id[obj.id] = obj

        # Store the object reference by class
        for _class in obj.classes:
            if _class not in TraceabilityMatrixHelper.objects_by_class:
                TraceabilityMatrixHelper.objects_by_class[_class] = []
            TraceabilityMatrixHelper.objects_by_class[_class].append(obj)

        # Add its children if any
        for child in obj.get_descendants():
            self.update_on_add_object(child.id)

    # --------------------------------------------------------------------------
    # Method: update_on_delete_object
    # Description: Remove the object from the objects cache.
    # Date: 08/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    def update_on_delete_object(self, object_id: ProteusID):
        """
        Remove the object from the objects cache.
        """
        obj = self._controller.get_element(object_id)

        # Remove the object from the objects_by_id dictionary
        try:
            TraceabilityMatrixHelper.objects_by_id.pop(obj.id)
        except KeyError:
            log.error(
                f"Consistency error: object {obj.id} not found in TraceabilityMatrixHelper.update_on_delete_object"
            )

        # Remove the object from the objects_by_class dictionary
        for _class in obj.classes:
            try:
                TraceabilityMatrixHelper.objects_by_class[_class].remove(obj)
            except ValueError:
                log.error(
                    f"Consistency error: object {obj.id} not found in class {_class} \
                          in TraceabilityMatrixHelper.update_on_delete_object"
                )

        # Remove its children if any
        for child in obj.get_descendants():
            self.update_on_delete_object(child.id)
        

    # --------------------------------------------------------------------------
    # Method: get_objects_from_classes
    # Description: This method (XSLT function) recieves a string with space-separated
    #              Proteus classes and return a node-set (List[_Element]) with the
    #              objects information that have the specified classes.
    # Date: 08/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @staticmethod
    def get_objects_from_classes(context, classes: str) -> List[ET._Element]:
        """
        This method (XSLT function) recieves a string with space-separated
        Proteus classes and return a node-set (List[_Element]) with the objects
        information that have the specified classes.

        The selected object information is parsed in an specific XML format
        to make easier XSLT processing and improve readability.

        The object information retrieved is the Id and Code. If
        proteus code is not found, name is used instead.

        The XML format is the following:
            <object id="1234">
                <label>Object label</label>
            </object>

        :param context: The XSLT context (no need to be present in the function signature)
        :param classes: A string with space-separated Proteus classes

        :return: A node-set (XPath object) with the objects information
        """
        classes = classes[0]

        # Objects -------------------------------------------------------------
        # Get the objects from the classes present in the project
        objects: List[Object] = []
        class_list: List[str] = classes.strip().split()
        for _class in class_list:
            objects_from_class = TraceabilityMatrixHelper.objects_by_class.get(
                _class, []
            )
            objects.extend(objects_from_class)


        # Create ObjectMatrixInformation from objects and sort them by label
        objects_information: List[ObjectMatrixInformation] = []
        for obj in objects:

            obj_label: str

            # Try to get the proteus code, if not found, use the name
            code_prop = obj.get_property(PROTEUS_CODE)
            if code_prop is not None:
                code: ProteusCode = code_prop.value
                obj_label = code.to_string()
            else:
                obj_label = obj.get_property(PROTEUS_NAME).value

            objects_information.append(ObjectMatrixInformation(obj.id, obj_label))

        # Sort the objects by label
        objects_information.sort(key=lambda obj: obj.label)


        # Node-set ------------------------------------------------------------
        node_set: List[ET._Element] = []

        # Add the object information to the root element
        for obj_info in objects_information:
            node = obj_info.generate_node()
            node_set.append(node)
        
        return node_set


    # --------------------------------------------------------------------------
    # Method: check_dependency
    # Description: This method (XSLT function) checks if a dependency exists between
    #              two objects.
    # Date: 08/02/2024
    # Version: 0.1
    # Author: José María Delgado Sánchez
    # --------------------------------------------------------------------------
    @staticmethod
    def check_dependency(context, source_id: ProteusID, target_id: ProteusID) -> str:
        """
        This method (XSLT function) checks if a dependency exists between
        two objects.

        :param context: The XSLT context (no need to be present in the function signature)
        :param source_id: The id of the source object
        :param target_id: The id of the target object

        :return: True if a dependency exists, False otherwise. The result is
                 returned as string to be used in the XSLT file.
        """
        source_id = source_id[0]
        target_id = target_id[0]

        # Get the source and target objects
        source_obj: Object = TraceabilityMatrixHelper.objects_by_id.get(source_id, None)
        target_obj: Object = TraceabilityMatrixHelper.objects_by_id.get(target_id, None)

        # Check if the objects exist
        if source_obj is None or target_obj is None:
            return str(False)

        # Get source traces
        source_traces = source_obj.traces.values()
        for trace in source_traces:
            # Check if the trace is a dependency type
            if trace.type == PROTEUS_DEPENDENCY:
                # Check if the target object is the target of the dependency
                if target_id in trace.targets:
                    return str(True)

        return str(False)


# --------------------------------------------------------------------------
# Class: ObjectMatrixInformation
# Description: This class represents the information of an object in the
#              traceability matrix.
# Date: 07/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ObjectMatrixInformation:
    """
    Class that represents the basic information of an object in the
    traceability matrix. It generates the node (etree.Element) with the
    object information in a specific XML format to make easier XSLT
    processing.

    The object information retrieved is the Id and matrix label.
    """
    def __init__(self, id: ProteusID, label: str):
        self.id = id
        self.label = label

    def generate_node(self) -> ET._Element:
        """
        Get the XML representation of the object information
        """
        element = ET.Element("object", id=self.id)
        label = ET.SubElement(element, "label")
        label.text = self.label
        return element
