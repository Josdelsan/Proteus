# ==========================================================================
# File: __init__.py
# Description: module initialization for the PROTEUS raw model editor component
# Date: 10/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================
from PyQt6.QtWidgets import QLabel

XML_PROBLEMATIC_CHARS = ["&", '"', "<", ">"]

# Helper function to create an error label
def create_error_label() -> QLabel:
    """
    Create an error label
    """
    error_label: QLabel = QLabel()
    error_label.setObjectName("error_label")
    error_label.setWordWrap(True)
    error_label.hide()
    return error_label