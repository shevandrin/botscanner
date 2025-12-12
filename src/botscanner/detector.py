from selenium.webdriver.remote.webdriver import WebDriver
from ._detector_utils import _find_elements_by_computed_style, _get_html_from_element, _is_element_interactive, _find_cursor_is_pointer, _find_elements_by_anchors
from .utils import _is_element_clickable
import json

class ChatbotDetector:
    """Handles detection of chatbot widget on web pages."""

    def discover_chatbot(self, driver: WebDriver) -> None:
        """
        Discover chatbot anchors that launch chatbot widgets.

        Returns:
            (candidate_element_or_None, stats_json)
        """
        stats = {
            "s1_candidates": 0
        }
        candidate = None

        # The first starategy is to find elements by anchors
        s1_elements = _find_elements_by_anchors(driver)
        if len(s1_elements) > 0:
            s1_elements_clickable = [_is_element_clickable(el, driver) for el in s1_elements]
            s1_counts = s1_elements_clickable.count(True)
            if s1_counts == 1:
                print("The candidate chatbot launcher element found by the first starategy")              
                stats["s1_candidates"] = 1
                candidate = s1_elements[s1_elements_clickable.index(True)]
            if s1_counts > 1:
                print("Multiple candidate chatbot launcher elements found by the first starategy. The solver has to be launched.")
                stats["s1_candidates"] = s1_counts
            if s1_counts == 0:
                print("The first starategy found elements but none are clickable.")

        else:
            print("The first starategy found no elements.")
            stats["s1_candidates"] = 0


        # The second starategy is to find elements by computed styles (geometry, position, z-index, etc.)
        return candidate, json.dumps(stats)