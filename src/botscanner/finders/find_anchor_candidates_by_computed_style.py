from botscanner.utils import vprint
from botscanner.jstools.find_el_computed_style import FIND_ELEMENT_COMPUTED_STYLE_JS
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def _find_anchor_candidates_by_computed_style(driver: WebDriver, quiet: bool = True):
    """
    Finds all elements that match specific computed style properties
    common to chatbot widgets (e.g., fixed position, high z-index).

    Returns:
        A list of WebElements that match the style criteria.
    """


    try:
        elements = driver.execute_script(FIND_ELEMENT_COMPUTED_STYLE_JS)
        if elements:
            vprint(f"Found {len(elements)} element(s) matching computed style criteria.", quiet)
            return elements
        else:
            vprint("No elements matched the computed style criteria.", quiet)
            return []
    except Exception as e:
        vprint(f"Error executing computed style search script: {e}", quiet)
        return []