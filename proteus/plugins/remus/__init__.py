# ==========================================================================
# Plugin: REMUS
# Description: PROTEUS 'remus' plugin for user interaction with documents
#              and specific use cases management.
# Date: 03/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

from .document_interactions import DocumentInteractions

def register(_,register_qwebchannel_class):
    register_qwebchannel_class("documentInteractions", DocumentInteractions)