# ==========================================================================
# File: abstract_object.py
# Description: a PROTEUS abstract class to be used as a superclass for both
# projects and objects
# Date: 15/09/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================
# Update: 26/09/2022 (Amador)
# Description:
# - Using get in dictionaries to return None if key is not found. Using 
#   square brackets throw an exception if the key does not exits.
# ==========================================================================

# imports

# standard library imports
import lxml.etree as ET
from enum import Enum
from typing import Type
from abc import ABC

# local imports (starting from root)
from proteus.model import *
from proteus.model.properties import Property, PropertyFactory

# --------------------------------------------------------------------------
# Class: ProteusStates
# Description: Enumeration for abstract object's state
# Date: 17/09/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class ProteusState(Enum):
    """
    Enumeration for abstract object's state.
    """

    # TODO Is it necessary to add FRESH? When you clone project -> it saves -> CLEAN
    # When load project -> It is saved -> CLEAN ->
    # Remove something -> Deleted and father -> Dirty
    # when edit something -> dirty
    FRESH = 0 # new object, just cloned but not already saved
    CLEAN = 1 # loaded object, not modified
    DIRTY = 2 # loaded object, modified
    DEAD  = 3 # loaded object, to be deleted

# --------------------------------------------------------------------------
# Class: AbstractObject
# Description: Abstract base class (ABC) to be used as a superclass for both
# projects and objects (they are very similar)
# Date: 15/09/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class AbstractObject(ABC):
    """
    A PROTEUS abstract object is an abstraction of PROTEUS projects and
    objects. It contains all features which are common to both types of
    PROTEUS objects, especially, their path to its XML file, its ID, and
    its properties (and probably more in the future).
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a PROTEUS abstract project.
    # Date       : 26/09/2022
    # Version    : 0.2 (path assert simplified)
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def __init__(self, path) -> None:
        """
        It initializes an abstract PROTEUS object.

        :param path: the path to the XML file containing the object's data.
        """

        # # Check file exists at path 
        # assert os.path.isfile(path), \
        #     f"PROTEUS {(self.__class__.__name__).lower()} file {path} not found."

        # TODO: put all common code in Project and Object here     

        # path to XML file (to be initialized in other methods?)
        self.path : str = path

        # short UUID (to be initialized in other methods?)
        self.id : ProteusID = None

        # state (to be initialized in other methods?)
        self.state : ProteusState = ProteusState.CLEAN

        # Properties dictionary (indexed by property names)
        self.properties : dict[str,Property] = dict[str,Property]()

    # ----------------------------------------------------------------------
    # Method     : load_properties
    # Description: It loads the properties of a PROTEUS abstract object.
    # Date       : 26/09/2022 (using get with None as default value)
    # Version    : 0.3
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def load_properties(self, root : ET.Element) -> None:
        """
        It loads a PROTEUS abstract object's properties from an XML root element.

        :param root: the XML root element.
        :type root: ET.Element
        """

        # Check root is not None
        assert root is not None, \
            f"Root element is not valid in {self.path}."

        # Find the <properties> element
        properties_element : ET.Element = root.find(PROPERTIES_TAG)

        # Check whether it has <properties>
        assert properties_element is not None, \
            f"PROTEUS file {self.path} does not have a <{PROPERTIES_TAG}> element."

        # Parse properties
        property_element : ET.Element
        for property_element in properties_element:
            property_name : str = property_element.attrib.get('name', None)
            # Check whether the property has a name
            assert property_name is not None, \
                f"PROTEUS file {self.path} includes an unnamed property."

            # Add the property to the properties dictionary
            self.properties[property_name] = PropertyFactory.create(property_element)

    # ----------------------------------------------------------------------
    # Method     : get_property
    # Description: It returns an object's property given its name.
    # Date       : 17/09/2022
    # Version    : 0.2
    # Author     : Pablo Rivera Jiménez
    #              Amador Durán Toro
    # ----------------------------------------------------------------------

    def get_property(self, key: str) -> Property:
        """
        It returns an object's property given its name.
        It aborts if there is no property with that name.
        TODO: return None in that case?

        :param key: the name of the property to be returned.
        :return: the property with the given name.
        """
        assert key in self.properties.keys(), \
            f"Property {key} not found in {self.id} properties."

        # using self.properties.get(key,default) we can return a default value
        return self.properties[key]

    # ----------------------------------------------------------------------
    # Method     : set_property
    # Description: It sets an object's property.
    # Date       : 17/09/2022
    # Version    : 0.2
    # Author     : Pablo Rivera Jiménez
    #              Amador Durán Toro
    # ----------------------------------------------------------------------

    def set_property(self, new_property:Property) -> None:
        """
        It sets an abstract object's (Object and Project) property.
        
        :param new_property: the new property to be set.
        :type new_property: Property
        """

        # Get new property name
        new_property_name : str = new_property.name

        # Get current property with that name (or None)
        current_property : Property = self.properties.get(new_property_name, None)

        # Check current property exists
        assert current_property is not None, \
            f"Cannot set nonexistent property {new_property_name} in {self.id} properties"

        # Get current property concrete class
        current_property_class : Type = current_property.__class__

        # Get new property concrete class
        new_property_class : Type = new_property.__class__

        # Check current and new properties are instances of the same class
        assert current_property_class == new_property_class, \
            f"Current and new property types are different in {self.id}: {current_property_class} != {new_property_class}"

        # Update property
        self.properties[new_property_name] = new_property

        # Update object's state
        if self.state == ProteusState.CLEAN:
            self.state = ProteusState.DIRTY

    # ----------------------------------------------------------------------
    # Method     : generate_xml
    # Description: abstract method for generating an XML element from an
    # abstract object. It must be overriden in subclasses.
    # Date       : 15/09/2022
    # Version    : 0.1
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def generate_xml(self) -> ET.Element:
        """
        It generates an XML element from an abstract object. It must be
        overriden in subclasses.

        :return: ET.Element. The XML element
        """
        
        # Check if instance is a Project or an Object
        if (self.class_name == "Project"):
            # Create <project> element and set ID
            element : ET.Element = ET.Element(PROJECT_TAG)

        elif(self.class_name == "Object"):
            # Create <object> element and set ID
            element : ET.Element = ET.Element(OBJECT_TAG)
        
        # Set element the id
        element.set('id', self.id)

        # Create <properties> element
        self.generate_xml_properties(element)

        # Check if instance is a Project or an Object
        if(self.class_name == "Project"):
            # Create <documents> element
            documents_element = ET.SubElement(element, DOCUMENTS_TAG)
            # Create <document> subelements
            for document in self.documents.values():
                document_element = ET.SubElement(documents_element, DOCUMENT_TAG)
                document_element.set('id', document.id)

        elif(self.class_name == "Object"):
            # Create <children> element
            children_element = ET.SubElement(element, CHILDREN_TAG)
            # Create <child> subelements
            for child in self.children.values():
                child_element = ET.SubElement(children_element, CHILD_TAG)
                child_element.set('id', child.id)

        return element

    # ----------------------------------------------------------------------
    # Method     : generate_properties_xml
    # Description: method for generating an XML element from the properties
    # of an abstract object.
    # Date       : 15/09/2022
    # Version    : 0.1
    # Author     : Amador Durán Toro
    # ----------------------------------------------------------------------

    def generate_xml_properties(self, parent_element:ET.Element) -> ET.Element:
        """
        Generate xml property function. It generates an ET.Element from the properties of an abstract object
        (Object and Project).

        :param parent_element: ET.Element. The parent element of the properties.
        :return: ET.Element. The properties element.
        """

        # Check parent element is not None
        assert parent_element is not None, \
            f"Properties cannot be generated for a null parent element. {self.uuid=}"

        # Create <properties> element
        properties_element = ET.SubElement(parent_element, PROPERTIES_TAG)

        # Create <property> subelements
        for property in self.properties.values():
            properties_element.append(property.generate_xml())

        # return parent elmenent, i.e. <project> or <object>
        return parent_element
