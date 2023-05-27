# ==========================================================================
# File: property_form.py
# Description: PyQT6 properties form component for the PROTEUS application
# Date: 26/05/2023
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from typing import Dict

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QDialogButtonBox


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.object import Object
from proteus.views.utils.decorators import component
from proteus.views.utils.input_factory import PropertyInputFactory



@component(QWidget)
class PropertyForm():

    def __init__(self, object_id : Object, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.object_id = object_id
        self.input_widgets = {}

    def create_component(self) -> None:

        self.object = self.project_service._get_element_by_id(self.object_id)

        # Set the window name
        window_name = self.object.get_property('name').value
        self.setWindowTitle(window_name)

        # Create the form vertical layout
        form_layout = QVBoxLayout(self)

        # Create a QTabWidget to organize properties by categories
        tab_widget = QTabWidget()

        # Get the object's properties dictionary
        properties_dict = self.object.properties

        # Create a dictionary to hold category widgets
        category_widgets = {}

        # Iterate over the properties and create widgets for each category
        for prop in properties_dict.values():
            # Get the category for the property
            category = prop.category

            # Create a QWidget for the category if it doesn't exist
            if category not in category_widgets:
                category_widget = QWidget()
                category_layout = QVBoxLayout(category_widget)
                category_widgets[category] = category_widget
            else:
                category_widget = category_widgets[category]
                category_layout = category_widget.layout()

            # Create the property input widget
            prop_widget, input_field_widget = PropertyInputFactory.create(prop)
            category_layout.addWidget(prop_widget)

            # Add the input field widget to the input widgets dictionary
            # NOTE: This is used to retrieve the values of the widgets that changed
            self.input_widgets[prop.name] = input_field_widget

        # Add the category widgets as tabs in the tab widget
        for category, category_widget in category_widgets.items():
            tab_widget.addTab(category_widget, category)

        # Add the tab widget to the main form layout
        form_layout.addWidget(tab_widget)

        # Create Save and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.save_button_clicked)
        button_box.rejected.connect(self.cancel_button_clicked)
        form_layout.addWidget(button_box)

        self.setLayout(form_layout)



    def update_component(self) -> None:
        pass

    def save_button_clicked(self):
        # Empty dictionary to hold the properties values to update
        update_list = []

        # Get the original object properties dictionary
        properties_dict = self.object.properties

        # Iterate over the input widgets and update the properties dictionary
        for prop_name in properties_dict.keys():

            # Get the property input value
            input_widget = self.input_widgets[prop_name]
            new_prop_value = PropertyInputFactory.widget_to_value(input_widget)

            # Get the original property and its value
            original_prop = properties_dict[prop_name]
            original_prop_value = original_prop.value

            # If the values are different, clone the original property with the new value
            if new_prop_value != original_prop_value:
                cloned_property = original_prop.clone(new_prop_value)
                update_list.append(cloned_property)

        print(update_list)
        self.project_service.update_properties(self.object_id, update_list)

        # Close the form window
        self.close()
        self.deleteLater()

    def cancel_button_clicked(self):
        # Close the form window without saving any changes
        self.close()
        self.deleteLater()
