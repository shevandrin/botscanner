from selenium.webdriver.remote.webdriver import WebDriver
from ._detector_utils import _find_elements_by_computed_style, _get_html_from_element, _is_element_interactive, _find_cursor_is_pointer, _find_elements_by_anchors
from .utils import vprint, _is_element_clickable
import json

class ChatbotDetector:
    """Handles detection of chatbot widget on web pages."""

    def discover_chatbot(self, driver: WebDriver, quiet: bool = True) -> None:
        """
        Discover chatbot anchors that launch chatbot widgets.

        Returns:
            (candidate_element_or_None, stats_json)
        """
        stats = {
            "s1_candidates": 0
            ,"s2_candidates": 0
        }
        candidate = None

        # The first starategy is to find elements by anchors
        s1_elements = _find_elements_by_anchors(driver, quiet)
        if len(s1_elements) > 0:
            s1_elements_clickable = [_is_element_clickable(el, driver, quiet) for el in s1_elements]
            s1_counts = s1_elements_clickable.count(True)
            if s1_counts == 1:
                vprint("The candidate chatbot launcher element found by the first strategy", quiet)              
                stats["s1_candidates"] = 1
                candidate = s1_elements[s1_elements_clickable.index(True)]
            if s1_counts > 1:
                vprint("Multiple candidate chatbot launcher elements found by the first starategy. The solver has to be launched.", quiet)
                stats["s1_candidates"] = s1_counts
            if s1_counts == 0:
                vprint("The first starategy found elements but none are clickable.", quiet)

        else:
            vprint("The first starategy found no elements.", quiet)

        s2_elements = _find_elements_by_computed_style(driver, quiet)
        if len(s2_elements) > 0:
                s2_elements_clickable = [_is_element_clickable(el, driver, quiet) for el in s2_elements]
                s2_counts = s2_elements_clickable.count(True)
                if s2_counts == 1:
                    vprint("The candidate chatbot launcher element found by the second starategy", quiet)              
                    stats["s2_candidates"] = 1
                    candidate = s2_elements[s2_elements_clickable.index(True)]
                if s2_counts > 1:
                    vprint("Multiple candidate chatbot launcher elements found by the second starategy. The solver has to be launched.", quiet)
                    stats["s2_candidates"]= s2_counts
                if s2_counts == 0:
                    vprint("The first starategy found elements but none are clickable.", quiet)
        else:
                vprint("The first starategy found no elements.", quiet)

        return candidate, json.dumps(stats)
