# ==========================================================================
# File: __init__.py
# Description: module initialization for the PROTEUS export package
# Date: 22/01/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

from enum import StrEnum

# Export formats -------------------------------------------------------------
class ExportFormat(StrEnum):
    HTML = "HTML"
    PDF = "PDF"

# Export strategies ----------------------------------------------------------
from proteus.views.export.export_strategy import ExportStrategy
from proteus.views.export.export_pdf import ExportPDF
from proteus.views.export.export_html import ExportHTML
