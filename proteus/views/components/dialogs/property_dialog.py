# ==========================================================================
# File: property_dialog.py
# Description: PyQT6 properties form component for the PROTEUS application
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from typing import Union, List, Dict, Any

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QDialogButtonBox,
    QFormLayout,
    QDialog,
    QGroupBox,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model import ProteusID, PROTEUS_NAME
from proteus.model.project import Project
from proteus.model.object import Object
from proteus.model.trace import Trace
from proteus.model.properties import Property, MarkdownProperty
from proteus.utils import ProteusIconType
from proteus.utils.dynamic_icons import DynamicIcons
from proteus.utils.translator import Translator
from proteus.views.forms.properties.property_input import PropertyInput
from proteus.views.forms.properties.property_input_factory import (
    PropertyInputFactory,
)
from proteus.views.components.abstract_component import ProteusComponent
from proteus.controller.command_stack import Controller

# Module configuration
_ = Translator().text  # Translator
log = logging.getLogger(__name__)  # Logger


# --------------------------------------------------------------------------
# Class: PropertyDialog
# Description: Class for the PROTEUS application properties form component.
# Date: 27/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class PropertyDialog(QDialog, ProteusComponent):
    """
    Class for the PROTEUS application properties form component. It is used
    to display the properties an traces of an element in a form. Properties
    and traces are grouped by categories in tabs. Each property and trace
    is displayed in a widget that is created using the PropertyInputFactory
    class.

    NOTE: Properties and Traces are different concepts in PROTEUS, but they
    are handle the same in the GUI. This is to simplify the user experience
    creating just one form to display both properties and traces.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: Class constructor, invoke the parents class constructors
    #              and create the component.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def __init__(self, element_id=None, *args, **kwargs) -> None:
        """
        Class constructor, invoke the parents class constructors and create
        the component.

        Store the element id, reference to the element whose properties and
        traces will be displayed, and the PropertyInput widgets in a dictionary.

        Flag project_dialog is used to avoid handling traces in the project
        form.

        :param element_id: The id of the element to edit.
        """
        super(PropertyDialog, self).__init__(*args, **kwargs)

        # Set the element id, reference to the element whose properties
        # will be displayed
        self.element_id: ProteusID = element_id
        self.project_dialog: bool = False

        # Create a dictionary to hold the input widgets for each property
        # NOTE: This is used to get the input values when the form is
        #       accepted
        self.input_widgets: Dict[str, PropertyInput] = {}

        # Create the component
        self.create_component()

    # ----------------------------------------------------------------------
    # Method     : create_component
    # Description: Create the component.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def create_component(self) -> None:
        """
        Create the dialog component. This method is called from the constructor.

        It creates a vertical layout where a tab widget is added. Each tab contains
        a form layout with the PropertyInput widgets for each category (properties
        and traces).

        Store the input widgets in a dictionary to get the values when the form
        is accepted.

        Creation is dinamic, depending on the properties and traces of the element.
        """

        # Retrieve properties and traces --------------------------------

        self.object: Union[Project, Object] = self._controller.get_element(
            self.element_id
        )

        # Get the object's properties dictionary
        properties_dict: Dict[str, Union[Property, Trace]] = (
            self.object.properties.copy()
        )

        main_obj_class: str
        try:
            # Merge object's traces with properties dict
            properties_dict.update(self.object.traces)

            # Get the main object class to set the icon
            main_obj_class = self.object.classes[-1]

        # Project will raise an AttributeError
        except AttributeError:
            log.debug("Project properties form.")

            main_obj_class = "proteus_icon"
            # Check if the object is a project to set the flag
            # This is used to avoid handling traces in the project form
            self.project_dialog = True

        # Dialog settings (icon is set later) ---------------------------
        self.sizeHint = lambda: QSize(500, 300)

        window_name: str = self.object.get_property(PROTEUS_NAME).value
        self.setWindowTitle(window_name)

        dialog_icon: QIcon = DynamicIcons().icon(ProteusIconType.App, main_obj_class)
        self.setWindowIcon(dialog_icon)

        # Properties and traces layout ----------------------------------

        # Create a dictionary to hold category widgets
        category_widgets: Dict[str, QWidget] = self.create_category_widgets(
            properties_dict
        )

        # Iterate over the properties and create widgets for each category
        prop: Property = None
        for prop in properties_dict.values():

            # Get the category widget
            category_widget: QWidget = category_widgets[prop.category]

            # Add a row to the category widget with the property input widget and label
            self.add_row_to_category_widget(category_widget, prop)

        # Tabs layout ---------------------------------------------------

        # Create the form vertical layout and the tab widget
        # to organize the properties by category
        tabbed_layout: QVBoxLayout = QVBoxLayout()
        tab_widget: QTabWidget = QTabWidget()

        # Add the category widgets as tabs in the tab widget
        for category, category_widget in category_widgets.items():
            translated_category: str = _(
                f"archetype.prop_category.{category}",
                alternative_text=category,
            )
            tab_widget.addTab(category_widget, translated_category)

        # Add the tab widget to the main form layout
        tabbed_layout.addWidget(tab_widget)

        # Buttons and logo layout ---------------------------------------

        buttons_layout: QVBoxLayout = QVBoxLayout()

        # Create Save and Cancel buttons
        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.setOrientation(Qt.Orientation.Vertical)
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)
        buttons_layout.addWidget(self.button_box)

        # Add US logo to the buttons layout and push it to the bottom
        us_logo: QIcon = DynamicIcons().icon(ProteusIconType.App, "US-digital")
        us_logo_label: QLabel = QLabel()
        us_logo_label.setPixmap(us_logo.pixmap(80, 80))
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(us_logo_label)

        # Main layout ---------------------------------------------------

        # Create layout to hold tabbed widgets and buttons
        window_layout: QHBoxLayout = QHBoxLayout(self)

        # Add the layouts to the main layout
        window_layout.addLayout(tabbed_layout)
        window_layout.addLayout(buttons_layout)

        self.setLayout(window_layout)

    # ======================================================================
    # Helper private methods
    # ======================================================================

    def create_category_widgets(
        self, properties_dict: Dict[str, Union[Property, Trace]]
    ) -> Dict[str, QWidget]:
        """
        Create the category widgets tabs for the properties and traces available
        categories.
        """
        # Create a dictionary to hold category widgets
        category_widgets: Dict[str, QWidget] = {}

        # Iterate over the properties and create widgets for each category
        prop: Property | Trace = None
        for prop in properties_dict.values():

            # Create a QWidget for the category if it doesn't exist
            if prop.category not in category_widgets:
                category_widget: QWidget = QWidget()
                category_layout: QFormLayout = QFormLayout(category_widget)
                category_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
                category_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
                category_widgets[prop.category] = category_widget

        return category_widgets

    def add_row_to_category_widget(
            self, category_widget: QWidget, prop: Union[Property, Trace]
    ) -> None:
        """
        Add a row to the category widget with the property input widget and label.
        """
        # Create the property input widget and label
        input_field_widget: PropertyInput = PropertyInputFactory.create(
            prop, controller=self._controller
        )
        input_label: QLabel = PropertyInputFactory.generate_label(prop)

        # Get the category layout
        category_layout: QFormLayout = category_widget.layout()

        # Traces and MarkdownProperty are wrapped in a group box
        if isinstance(prop, (Trace, MarkdownProperty)):
            group_box: QGroupBox = QGroupBox()
            group_box.setTitle(input_label.text())
            group_box_layout: QVBoxLayout = QVBoxLayout()
            group_box_layout.addWidget(input_field_widget)
            group_box_layout.setContentsMargins(0, 0, 0, 0)
            group_box.setLayout(group_box_layout)

            category_layout.addRow(group_box)
        else:
            # Add the input field widget and label to the category layout
            category_layout.addRow(input_label, input_field_widget)

        # Add the input field widget to the input widgets dictionary
        # NOTE: This is used to retrieve the values of the widgets that changed
        self.input_widgets[prop.name] = input_field_widget

    # ======================================================================
    # Dialog slots methods (connected to the component signals)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : save_button_clicked
    # Description: Manage the save button clicked event. It gets the values
    #              of the input widgets and updates the properties of the
    #              element.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def save_button_clicked(self):
        """
        Manage the save button clicked event. It gets the values of the
        input widgets and updates the propertie and traces of the element.

        This method compares the values of the input widgets with the
        original properties and traces of the element. If there are changes,
        just the properties and traces that changed are updated.

        Form errors are checked before updating the properties. All errors
        are displayed in each input widget. If there are errors, the
        properties update method is not called

        Controller update_properties method is called. Both properties and
        traces are passed in the same list, they can be processed separately
        later.
        """
        # Empty dictionary to hold the properties to update
        update_list: List[Union[Property, Trace]] = []

        # Get the original object properties (and merge with traces if needed)
        properties_dict: Dict[str, Property] = self.object.properties.copy()
        if not self.project_dialog:
            properties_dict.update(self.object.traces)

        # Boolean property to check if there are errors
        form_has_errors: bool = False

        # Iterate over the input widgets and update the properties dictionary
        for prop_name in properties_dict.keys():
            # Get the property input value
            input_widget: PropertyInput = self.input_widgets[prop_name]

            # Check if the widget has errors and update the form errors flag
            widget_has_errors: bool = input_widget.has_errors()
            form_has_errors = form_has_errors or widget_has_errors

            # If the widget has errors or previous errors exist, continue
            if widget_has_errors or form_has_errors:
                continue

            # Get the value of the property (or trace property)
            new_prop_value: Any = input_widget.get_value()

            # Get the original property and its value
            original_prop: Union[Property, Trace] = properties_dict[prop_name]
            if isinstance(original_prop, Trace):
                original_prop_value: list = original_prop.targets
            else:
                original_prop_value: Any = original_prop.value

            # If the values are different, clone the original property with the new value
            if new_prop_value != original_prop_value:
                cloned_property: Union[Property, Trace] = original_prop.clone(
                    new_prop_value
                )
                update_list.append(cloned_property)

        # If there are errors, do not update the properties
        if form_has_errors:
            return

        # Update the properties of the element if there are changes
        if len(update_list) > 0:
            self._controller.update_properties(
                self.element_id, new_properties=update_list
            )

        # Close the form window
        self.close()
        self.deleteLater()

    # ----------------------------------------------------------------------
    # Method     : cancel_button_clicked
    # Description: Manage the cancel button clicked event. It closes the
    #              form window without saving any changes.
    # Date       : 27/05/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    def cancel_button_clicked(self):
        """
        Manage the cancel button clicked event. It closes the form window
        without saving any changes.
        """
        # Close the form window without saving any changes
        self.close()
        self.deleteLater()

    # ======================================================================
    # Dialog static methods (create and show the form window)
    # ======================================================================

    # ----------------------------------------------------------------------
    # Method     : create_dialog (static)
    # Description: Handle the creation and display of the form window.
    # Date       : 05/06/2023
    # Version    : 0.1
    # Author     : José María Delgado Sánchez
    # ----------------------------------------------------------------------
    @staticmethod
    def create_dialog(
        controller: Controller, element_id: ProteusID
    ) -> "PropertyDialog":
        """
        Handle the creation and display of the form window.

        :param controller: A Controller instance.
        :param element_id: The id of the element to edit.
        """
        dialog = PropertyDialog(element_id=element_id, controller=controller)
        dialog.exec()
        return dialog
