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


def register(register_xslt_function, register_qwebchannel_class, register_proteus_component):
    register_qwebchannel_class("documentInteractions", DocumentInteractions)
    register_xslt_function("glossary_highlight", GlossaryHandler.highlight_glossary_items)
    register_proteus_component("glossaryHandler", GlossaryHandler)
