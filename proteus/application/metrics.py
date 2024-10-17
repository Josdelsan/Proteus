# ==========================================================================
# File: metrics.py
# Description: Application metrics module
# Date: 01/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import time
import logging

# --------------------------------------------------------------------------
# Third-party library imports
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.application.events import UpdateMetricsEvent


# Module configuration
log = logging.getLogger(__name__)  # Logger


# --------------------------------------------------------------------------
# Class: Metrics
# Description: Class to handle application metrics
# Date: 01/10/2024
# Version: 0.1
# Author: José María Delgado Sánchez
# --------------------------------------------------------------------------
class Metrics:

    # App metrics
    html_generation_time: int = 0  # XML + XSLT transform time (ms)

    _html_load_time_start: float = 0
    html_load_time: int = 0  # QWebEngineView load time (ms)

    # --------------------------------------------------------------------------
    # HTML generation time methods
    # --------------------------------------------------------------------------

    @staticmethod
    def html_generation_time_decorator(func: callable):
        """
        Decorator to measure the time it takes to generate the HTML.

        It is meant to be used with get_html_view_path() method in the controller.
        """

        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            Metrics.html_generation_time = int((end_time - start_time) * 1000)
            UpdateMetricsEvent().notify()
            log.debug(f"HTML generation time: {Metrics.html_generation_time} ms")
            return result

        return wrapper

    # --------------------------------------------------------------------------
    # HTML load time methods
    # --------------------------------------------------------------------------

    @staticmethod
    def html_load_time_start():
        """
        Start measuring the time it takes to load the HTML in the QWebEngineView.

        It is meant to be used in the views_container before browser load is called.
        """
        Metrics._html_load_time_start = time.perf_counter()

    @staticmethod
    def html_load_time_end():
        """
        End measuring the time it takes to load the HTML in the QWebEngineView.

        It is meant to be used along loadFinished signal in the views_container.
        """
        end_time = time.perf_counter()
        Metrics.html_load_time = int((end_time - Metrics._html_load_time_start) * 1000)
        UpdateMetricsEvent().notify()
        log.debug(f"HTML load time: {Metrics.html_load_time} ms")
