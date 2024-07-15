# ==========================================================================
# File: class_diagram.py
# Description: Plugin for creating class diagrams using PlantUML
# Date: 10/06/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import Dict, List, MutableSet, Callable
import re
from io import StringIO
from html import escape

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

import markdown
from trieregex import TrieRegEx as TRE

# --------------------------------------------------------------------------
# Plugin imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Proteus imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.trace import Trace
from proteus.views.components.abstract_component import ProteusComponent
from proteus.application.events import (
    OpenProjectEvent,
    AddObjectEvent,
    DeleteObjectEvent,
    ModifyObjectEvent,
)


# logging configuration
log = logging.getLogger(__name__)

# Constants

CLASS_DIAGRAM_ARCHETYPE_CLASS = "class-diagram"
ASSOCIATION_ROLE_ARCHETYPE_CLASS = "association-role"

CLASSES_TRACE = 'classes'
ASSOCIATIONS_TRACE = 'associations'
BASE_TYPE_ROLE_TRACE = 'base-type'

# Class
class ClassDiagramGenerator(ProteusComponent):

    """
    Generates a class diagram given the ProteusID of a class-diagram object.
    It uses the PlantUML server to generate the diagram and returns an image
    encoded in base64 so it can be inserted in the HTML.
    """

    get_element_by_id: Callable[[ProteusID], Object] = None


    def create(self, context, class_diagram_object_id: ProteusID) -> str:
        """
        Create a class diagram from a 'class-diagram' object. Returns the PlantUML code.
        """

        # Check a project has been opened
        if self._controller.get_element is None:
            return ""
        
        class_diagram_object_id = class_diagram_object_id[0]

        # Get the object
        class_diagram_object = self._controller.get_element(class_diagram_object_id)

        # Check the object is a class diagram class
        assert CLASS_DIAGRAM_ARCHETYPE_CLASS in class_diagram_object.classes, f"Class '{CLASS_DIAGRAM_ARCHETYPE_CLASS}' not found in object '{class_diagram_object_id}' with classes '{class_diagram_object.classes}'"

        # Get classes and associations
        classes = self.get_traces_objects_from_diagram(class_diagram_object, CLASSES_TRACE)
        associations = self.get_traces_objects_from_diagram(class_diagram_object, ASSOCIATIONS_TRACE)

        # Notes variable
        notes = ""

        # Generate PlantUML code
        plantuml_classes_code = ""
        for class_object in classes:
            plantuml_classes_code += self.generate_plantuml_class_code(class_object)
            notes += self.generate_notes(class_object)

        # Generate PlantUML code for associations
        plantuml_associations_code = ""
        for association_object in associations:
            plantuml_associations_code += self.generate_plantuml_association_code(association_object)

        # Generate PlantUML code for the diagram
        plantuml_code = f"@startuml\n"
        plantuml_code += plantuml_classes_code
        plantuml_code += plantuml_associations_code
        plantuml_code += notes
        plantuml_code += "@enduml\n"

        return plantuml_code


    def get_traces_objects_from_diagram(self, class_diagram_object: Object, trace_name: str) -> List[Object]:
        """
        Get the classes objects from a class diagram object.
        """

        objects = []

        for target_id in class_diagram_object.traces[trace_name].targets:
            target_object = self._controller.get_element(target_id)
            objects.append(target_object)

        return objects
    

    def generate_plantuml_class_code(self, class_object: Object):
        """
        Generate the PlantUML code for a class object.
        """

        # Get the class name
        class_name = class_object.get_property(PROTEUS_NAME).value

        # Empty string for the PlantUML code
        plantuml_code = ""

        # Check if it is abstract
        if class_object.get_property("is-abstract").value:
            plantuml_code += "abstract "

        # Class keyword
        plantuml_code += "class "

        # Class name
        plantuml_code += class_name

        # Check if it is a stereotype (supertype), it is knows supertype is 1 per class limited
        supertype_list = class_object.traces['supertype'].targets
        if len(supertype_list) > 0:
            supertype_id = supertype_list[0]
            supertype_object = self._controller.get_element(supertype_id)
            supertype_name = supertype_object.get_property(PROTEUS_NAME).value
            plantuml_code += f" <<{supertype_name}>>"

        # Open class
        plantuml_code += " {\n"

        # Attributes
        plantuml_code += self.generate_class_attributes(class_object)

        # Close class
        plantuml_code += "}\n"

        return plantuml_code


    def generate_plantuml_association_code(self, association_object: Object):
        """
        Generate the PlantUML code for an association object.
        """

        role_objects: list[Object] = []

        # Get association roles objects from association children
        for child in association_object.get_descendants():
            if ASSOCIATION_ROLE_ARCHETYPE_CLASS in child.classes:
                role_objects.append(child)

        # Generate the PlantUML code
        plantuml_code = ""

        for index, role_object in enumerate(role_objects):
            
            # Skip if there is less than two roles
            if len(role_objects) > 1:

                # For first and second role, create a normal association
                if index == 0:

                    association_connector = "-down-"
                    if association_object.get_property("is-derived").value:
                        association_connector = "^-down-"

                    next_role_object = role_objects[index+1]
                    # Get class names from traces (it is known max base type is 1 per role)
                    class_name1 = self.get_class_name_from_role(role_object)
                    class_name2 = self.get_class_name_from_role(next_role_object)

                    # Classes bounds
                    class1_bounds = self.get_association_role_bounds(role_object)
                    class2_bounds = self.get_association_role_bounds(next_role_object)

                    plantuml_code += f"{class_name1} {class1_bounds} {association_connector} {class2_bounds} {class_name2}\n"
                
                # Role 2 has been processed in previous iteration
                elif index == 1:
                    pass

                # For third role, use previous two roles to create a three-way association
                elif index == 2:
                    # Get class names from traces (it is known max base type is 1 per role)
                    class_name1 = self.get_class_name_from_role(role_objects[0])
                    class_name2 = self.get_class_name_from_role(role_objects[1])
                    class_name3 = self.get_class_name_from_role(role_objects[2])

                    plantuml_code += f"({class_name1}, {class_name2}) - {class_name3}\n"

                # More than three roles are not supported
                else:
                    log.error(f"Association with more than three roles is not supported by PlantUML. Association object: {association_object.id}")
                    break

        return plantuml_code


    def get_class_name_from_role(self, role_object: Object) -> str:
        """
        Get the class name from a role object.
        """

        class_id = role_object.traces[BASE_TYPE_ROLE_TRACE].targets[0]
        class_object = self._controller.get_element(class_id)
        class_name = class_object.get_property(PROTEUS_NAME).value

        return class_name


    def get_association_role_bounds(self, role_object: Object) -> str:
        """
        Get the multiplicity bounds from a role object.
        """

        lower_bound = role_object.get_property("multiplicity-lower-bound").value
        upper_bound = role_object.get_property("multiplicity-upper-bound").value

        return f'"{lower_bound}..{upper_bound}"' if lower_bound and upper_bound else ""


    def generate_class_attributes(self, class_object: Object) -> str:
        """
        Generate the PlantUML code for the attributes of a class object.
        """

        attributes = ""

        # Iterate over the children and handle 'object-attribute' objects
        for child in class_object.get_descendants():
            if "object-attribute" in child.classes:
                attribute_name = child.get_property(PROTEUS_NAME).value
                attribute_base_type = child.get_property("base-type").value
                attribute_type = child.get_property("type").value
                attribute_init_value = child.get_property("init-value").value
                
                if attribute_type == 'simple':
                    attributes += f"{attribute_name} : {attribute_base_type}"
                else:
                    attributes += f"{attribute_name} : {attribute_type}({attribute_base_type})"
                    attribute_lower_bound = child.get_property("multiplicity-lower-bound").value
                    attribute_upper_bound = child.get_property("multiplicity-upper-bound").value

                    if attribute_lower_bound and attribute_upper_bound:
                        attributes += f" [{attribute_lower_bound}..{attribute_upper_bound}]"

                if attribute_init_value:
                    attributes += f" = {attribute_init_value}"

                attributes += "\n"

        return attributes


    def generate_notes(self, object: Object) -> str:
        """
        Generate notes in the right format for the given object in PlantUML.
        """
        description = object.get_property("description").value
        name = object.get_property(PROTEUS_NAME).value
        if description:
            return f"note right of {name}\n{description}\nend note\n"
        else:
            return ""