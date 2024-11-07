# ==========================================================================
# File: update_object_meta_model.py
# Description: Command to update the meta model of an object.
# Date: 15/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
# NOTE: This file contains a developer feature that. This command will not
# used in a Controller/command_stack method, it will be injected directly
# into the Controller stack when needed.

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List, Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QUndoCommand

# --------------------------------------------------------------------------
# Project specific imports (starting from root)
# --------------------------------------------------------------------------

from proteus.model import ProteusClassTag
from proteus.model.object import Object
from proteus.model.properties import Property
from proteus.model.abstract_object import ProteusState
from proteus.application.events import (
    ModifyObjectEvent,
)


# --------------------------------------------------------------------------
# Class: UpdateObjectMetaModelCommand
# Description: Command class to update the meta model of an object.
# Date: 15/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class UpdateObjectMetaModelCommand(QUndoCommand):
    """
    Command class to update the properties of an element.

    NOTE: This is a developer feature that must be injected directly into the
    Controller stack when needed. It is not implemented as a method of the
    Controller/command_stack.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors.
    # Date       : 15/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(
        self,
        object: Object,
        new_classes: List[ProteusClassTag],
        new_acceptedChildren: List[ProteusClassTag],
        new_acceptedParents: List[ProteusClassTag],
        new_selectedCategory: str,
        new_numbered: bool,
        new_properties: Dict[str, Property],
    ):
        super(UpdateObjectMetaModelCommand, self).__init__()

        self.object: Object = object

        self.new_classes: List[ProteusClassTag] = new_classes
        self.new_acceptedChildren: List[ProteusClassTag] = new_acceptedChildren
        self.new_acceptedParents: List[ProteusClassTag] = new_acceptedParents
        self.new_selectedCategory: str = new_selectedCategory
        self.new_numbered: bool = new_numbered
        self.new_properties: Dict[str, Property] = new_properties

        self.old_classes: List[ProteusClassTag] = object.classes.copy()
        self.old_acceptedChildren: List[ProteusClassTag] = (
            object.acceptedChildren.copy()
        )
        self.old_acceptedParents: List[ProteusClassTag] = object.acceptedParents.copy()
        self.old_selectedCategory: str = str(object.selectedCategory)
        self.old_numbered: bool = object.numbered
        self.old_properties: Dict[str, Property] = (
            object.properties.copy()
        )  # Deep copy is not needed because properties are immutable
        self.old_state: ProteusState = ProteusState(object.state)

    # ----------------------------------------------------------------------
    # Method     : redo
    # Description: Redo the command, update the object meta model.
    # Date       : 15/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def redo(self) -> None:
        """
        Redo the command, update the object meta model.
        """
        self.object.classes = self.new_classes
        self.object.acceptedChildren = self.new_acceptedChildren
        self.object.acceptedParents = self.new_acceptedParents
        self.object.selectedCategory = self.new_selectedCategory
        self.object.numbered = self.new_numbered
        self.object.properties = self.new_properties
        self.object.state = ProteusState.DIRTY

        ModifyObjectEvent().notify(self.object.id)

    # ----------------------------------------------------------------------
    # Method     : undo
    # Description: Undo the command, restore the previous object meta model.
    # Date       : 15/10/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def undo(self) -> None:
        """
        Undo the command, restore the previous object meta model.
        """
        self.object.classes = self.old_classes
        self.object.acceptedChildren = self.old_acceptedChildren
        self.object.acceptedParents = self.old_acceptedParents
        self.object.selectedCategory = self.old_selectedCategory
        self.object.numbered = self.old_numbered
        self.object.properties = self.old_properties
        self.object.state = self.old_state

        ModifyObjectEvent().notify(self.object.id)
