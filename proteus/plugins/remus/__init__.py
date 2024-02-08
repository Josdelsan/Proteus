# ==========================================================================
# Plugin: REMUS
# Description: PROTEUS 'remus' plugin for user interaction with documents
#              and specific use cases management.
# Date: 03/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

from .document_interactions import DocumentInteractions
from .glossary_handler import GlossaryHandler
from .traceability_matrix_helper import TraceabilityMatrixHelper

def register(register_xslt_function, register_qwebchannel_class, register_proteus_component):

    # Document Interactions
    register_qwebchannel_class("documentInteractions", DocumentInteractions)

    # Glossary
    register_xslt_function("glossary_highlight", GlossaryHandler.highlight_glossary_items)
    register_proteus_component("glossaryHandler", GlossaryHandler)

    # Traceability Matrix
    register_proteus_component("traceabilityMatrixHelper", TraceabilityMatrixHelper)
    register_xslt_function("get_objects_from_classes", TraceabilityMatrixHelper.get_objects_from_classes)
    register_xslt_function("check_dependency", TraceabilityMatrixHelper.check_dependency)
