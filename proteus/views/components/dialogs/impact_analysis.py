# ==========================================================================
# File: impact_analysis.py
# Description: PyQT6 impact analysis window component for the PROTEUS application
# Date: 31/10/2024
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

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QTreeWidget,
    QSizePolicy,
    QSplitter,
)

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.views.forms.items.objects_list_edit import ObjectsListEdit
from proteus.views.components.dialogs.base_dialogs import ProteusDialog
from proteus.controller.command_stack import Controller
from proteus.application.resources.translator import translate as _


# --------------------------------------------------------------------------
# Class: ImpactAnalysisWindow
# Description: PyQT6 impact analysis window component for the PROTEUS application
# Date: 31/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class ImpactAnalysisWindow(ProteusDialog):

    def __init__(self, *args, **kargs):
        super(ImpactAnalysisWindow, self).__init__(*args, **kargs)

        self.create_component()

    def create_component(self):
        self.setWindowTitle("Impact Analysis")
        self.resize(500, 400)

        # Get all objects in the project
        project = self._controller.get_current_project()
        all_objects = project.get_descendants_recursively()
        all_objects.remove(project)
        all_objects: List[Object] = [obj for obj in all_objects if obj.state != ProteusState.DEAD]

        # Create the object picker
        self.object_picker = ObjectsListEdit(self._controller, candidates=all_objects)


        # Create the tree widget to show the impact analysis
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Document", "Object"])
        self.tree.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        

        splitter.addWidget(self.object_picker)
        splitter.addWidget(self.tree)
        splitter.setSizes([200, 400])

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(splitter)

        self.set_content_layout(layout)

        # Set the buttons
        self.reject_button.setText(_("dialog.close_button"))
        self.accept_button.setHidden(True)

    @staticmethod
    def show_dialog(parent: QObject, controller: Controller):
        dialog = ImpactAnalysisWindow(parent=parent, controller=controller)
        dialog.show()
        return dialog
