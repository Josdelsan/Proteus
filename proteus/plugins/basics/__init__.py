# ==========================================================================
# Plugin: basics
# Description: PROTEUS 'basics' plugin provides general XSLT utilities and
#              QWebChannel classes for PROTEUS.
# Date: 06/03/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

from .proteus_xslt_basics import generate_markdown, image_to_base64, current_document
from .proteus_xslt_basics import ProteusBasicMethods


def register(register_xslt_function, register_qwebchannel_class, _):
    register_xslt_function("generate_markdown", generate_markdown)
    register_xslt_function("image_to_base64", image_to_base64)
    register_xslt_function("current_document", current_document)

    register_qwebchannel_class("proteusBasics", ProteusBasicMethods)
