# ==========================================================================
# File: __init__.py
# Description: PROTEUS 'model' package initializer
# Date: 10/08/2022
# Version: 0.2
# Author: Amador Durán Toro
#         José María Delgado Sánchez
# ==========================================================================
# Update: 23/10/2022 (José María)
# Description:
# - Refactorized constants names
# ==========================================================================


# standard library imports
from typing import NewType

# local imports
#from model.abstract_object import AbstractObject
#from model.property import Property, PropertyFactory
#from model.project import Project
#from model.object import Object

# ==========================================================================
# constants
# ==========================================================================

# Directory and file names
PROJECT_FILE_NAME  = str('proteus.xml')
OBJECTS_REPOSITORY = str('objects')
ASSETS_REPOSITORY  = str('assets')

# XML tags
PROJECT_TAG        = str('project')
OBJECT_TAG         = str('object')
PROPERTIES_TAG     = str('properties')
DOCUMENT_TAG       = str('document')
DOCUMENTS_TAG      = str('documents')
CHILD_TAG          = str('child')
CHILDREN_TAG       = str('children')
TRACES_TAG         = str('traces')
TRACE_PROPERTY_TAG = str('traceProperty')
TRACE_TAG          = str('trace')
XSL_TEMPLATES_TAG  = str('xsl-templates')
XLS_TEMPLATE_TAG   = str('xsl-template')

# XML attributes
ID_ATTRIBUTE                = str('id')
ACCEPTED_CHILDREN_ATTRIBUTE = str('acceptedChildren')
ACCEPTED_PARENTS_ATTRIBUTE  = str('acceptedParents')
ACCEPTED_TARGETS_ATTRIBUTE  = str('acceptedTargets')
CLASSES_ATTRIBUTE           = str('classes')
NAME_ATTRIBUTE              = str('name')
REQUIRED_ATTRIBUTE          = str('required')
INMUTABLE_ATTRIBUTE         = str('inmutable')
CATEGORY_ATTRIBUTE          = str('category')
TOOLTIP_ATTRIBUTE           = str('tooltip')
TARGET_ATTRIBUTE            = str('target')
TRACE_TYPE_ATTRIBUTE        = str('traceType')

# Type for Class tags in Proteus
ProteusClassTag = NewType('ProteusClassTag', str)

# Type for UUIDs in Proteus
ProteusID = NewType('ProteusID', str)

# Some predefined class tags
PROTEUS_DOCUMENT = ProteusClassTag(':Proteus-document')
PROTEUS_ANY      = ProteusClassTag(':Proteus-any')
PROTEUS_NONE     = ProteusClassTag(':Proteus-none')
PROTEUS_ALL      = ProteusClassTag(':Proteus-all')

# Some predefined attribute names
PROTEUS_CODE = str(':Proteus-code')
PROTEUS_NAME = str(':Proteus-name')
PROTEUS_DATE = str(':Proteus-date')
PROTEUS_ACRONYM = str(':Proteus-acronym')

# Some predefined traceability types
PROTEUS_DEPENDENCY = str(':Proteus-dependency')
PROTEUS_AUTHOR = str(':Proteus-author')
PROTEUS_INFORMATION_SOURCE = str(':Proteus-information-source')
PROTEUS_WORKS_FOR = str(':Proteus-works-for')

# Default values
DEFAULT_TRACE_NAME     = str('trace')
DEFAULT_TRACE_CATEGORY = str('dependencies')
DEFAULT_TRACE_TYPE     = PROTEUS_DEPENDENCY

# Name prefix for cloned objects
COPY_OF = str('archetype.copy-of')

