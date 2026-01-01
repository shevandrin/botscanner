from ...patterns import load_patterns, get_chatbot_windows_shadow_dom_patterns
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from ...jstools.find_shadow_anchor import SHADOW_ANCHOR


patterns = load_patterns()
CORE_ANCHORS_PATTERNS = get_chatbot_windows_shadow_dom_patterns(patterns)

def _find_shadow_anchor_candidates(driver: WebDriver, logger):
    """
    Find potential chatbot anchor elements within Shadow DOM structures.
    This function searches for chatbot anchor candidates hidden in Shadow DOM
    by executing JavaScript that matches against predefined anchor patterns.

    Arguments:
        driver (WebDriver): Selenium WebDriver instance used to execute JavaScript
        logger: Logger instance for logging information
    
    Returns:
        List of structured data about Shadow DOM elements matching chatbot anchor patterns.
    """

    keywords = CORE_ANCHORS_PATTERNS.get('chatbot_anchors', [])

    elements = driver.execute_script(SHADOW_ANCHOR,
                                    [k.lower() for k in keywords])
    
    if not elements:
        logger.info("No shadow DOM chatbot window candidates found.")
        return []
    
    logger.info(f"Found {len(elements)} shadow DOM chatbot window candidates.")

    return elements


