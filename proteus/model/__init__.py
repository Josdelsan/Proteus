# ==========================================================================
# File: __init__.py
# Description: PROTEUS 'model' package initializer
# Date: 10/08/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# standard library imports
from typing import NewType

# local imports
#from model.abstract_object import AbstractObject
#from model.property import Property, PropertyFactory
#from model.project import Project
#from model.object import Object

# constants
PROJECT_FILE_NAME  = str('proteus.xml')
OBJECTS_REPOSITORY = str('objects')
ASSETS_REPOSITORY  = str('assets')

PROJECT_TAG        = str('project')
OBJECT_TAG         = str('object')
NAME_TAG           = str('name')
CATEGORY_TAG       = str('category')
PROPERTIES_TAG     = str('properties')
DOCUMENT_TAG       = str('document')
DOCUMENTS_TAG      = str('documents')
CHILD_TAG          = str('child')
CHILDREN_TAG       = str('children')

# Type for Class tags in Proteus
ProteusClassTag = NewType('ProteusClassTag', str)

# Some predefined class tags
PROTEUS_DOCUMENT = ProteusClassTag(':Proteus-document')
PROTEUS_ANY      = ProteusClassTag(':Proteus-any')
PROTEUS_ALL      = ProteusClassTag(':Proteus-all')

# Type for UUIDs in Proteus
ProteusID = NewType('ProteusID', str)
