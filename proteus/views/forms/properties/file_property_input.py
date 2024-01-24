# ==========================================================================
# File: file_property_input.py
# Description: File property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================


# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.properties.file_property import FileProperty
from proteus.views.forms.properties.property_input import PropertyInput
from proteus.views.forms.asset_edit import AssetEdit


# --------------------------------------------------------------------------
# Class: FilePropertyInput
# Description: File property input widget for properties forms.
# Date: 17/10/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class FilePropertyInput(PropertyInput):
    """
    File property input widget for properties forms.
    """

    # ----------------------------------------------------------------------
    # Method     : get_value
    # Description: Returns the value of the input widget.
    # Date       : 04/08/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def get_value(self) -> str:
        """
        Returns the value of the input widget. The value is converted to a
        file.
        """
        self.input: AssetEdit
        return self.input.asset()

    # ----------------------------------------------------------------------
    # Method     : validate
    # Description: Validates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def validate(self) -> str:
        """
        Validates the input widget. Returns an error message if the input
        has errors, None otherwise.
        """
        file_name: str = self.get_value()
        
        # Check if text contains CDATA section delimiters
        if file_name.find("<![CDATA[") != -1 or file_name.find("]]>") != -1:
            return "file_property_input.validator.error.cdata"
        
        return None

    # ----------------------------------------------------------------------
    # Method     : create_input
    # Description: Creates the input widget.
    # Date       : 17/10/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_input(property: FileProperty, *args, **kwargs) -> AssetEdit:
        """
        Creates the input widget based on PROTEUS AssetEdit.
        """
        input: AssetEdit = AssetEdit()
        input.setAsset(property.value)
        return input
