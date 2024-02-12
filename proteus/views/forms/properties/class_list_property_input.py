# ==========================================================================
# File: class_list_property_input.py
# Description: Class list input widget for properties forms.
# Date: 06/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import List

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtGui import QIcon

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties import ClassListProperty
from proteus.controller.command_stack import Controller
from proteus.views.forms.properties.property_input import PropertyInput
from proteus.views.forms.check_combo_box import CheckComboBox
from proteus.utils.translator import Translator
from proteus.utils import ProteusIconType
from proteus.utils.dynamic_icons import DynamicIcons

# Module configuration
_ = Translator().text  # Translator


# --------------------------------------------------------------------------
# Class: ClassListPropertyInput
# Description: Class list input widget for properties forms.
# Date: 06/02/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ClassListPropertyInput(PropertyInput):
    """
    Class list input widget for properties forms.
    """

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 06/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> List:
        """
        Returns the value of the input widget. The value is converted to a
        list.
        """
        self.input: CheckComboBox
        return self.input.checkedItemsData()

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 06/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str:
        """
        Validates the input widget. Returns an error message if the input
        has errors, None otherwise.
        """
        pass

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 06/02/2024
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(
        property: ClassListProperty, controller: Controller, *args, **kwargs
    ) -> CheckComboBox:
        """
        Creates the input widget based on PROTEUS TraceEdit.
        """
        input: CheckComboBox = CheckComboBox()

        # Get project and property classes
        project_classes = controller.get_project_available_classes()
        property_classes = property.value

        # Include items in the checkcombobox setting the checked state
        # If there was a class selected in the property that is not in the project
        # it will be excluded from the list
        for project_available_class in project_classes:

            # Check if it has to be checked
            is_checked = project_available_class in property_classes

            # Class icon
            class_icon = DynamicIcons().icon(
                ProteusIconType.Archetype, project_available_class
            )

            # Class name translation
            class_name_translated = _(
                f"archetype.class.{project_available_class}",
                alternative_text=project_available_class,
            )

            # Add item
            input.addItem(
                class_name_translated, project_available_class, is_checked, class_icon
            )

        return input
