from selenium.webdriver.common.by import By
from ...jstools.shadow_search_js import SHADOW_SEARCH_JS
from ...patterns import CHATBOT_WINDOWS_SHADOW_DOM_PATTERNS

def _find_windows_candidates_as_shadowdom(driver, logger):
    """
    Find potential chatbot window elements within Shadow DOM structures.
    This function searches for chatbot window candidates hidden in Shadow DOM
    by executing JavaScript that matches against predefined shadow DOM patterns.
    
    Arguments:
        driver: Selenium WebDriver instance used to execute JavaScript
        quiet: Boolean flag to control verbose output (default: True)
    
    Returns:
        List of Shadow DOM elements matching chatbot window patterns, 
             or empty list if no candidates found
    
    Raises:
        WebDriverException if JavaScript execution fails
    """

    keywords = CHATBOT_WINDOWS_SHADOW_DOM_PATTERNS
    elements = driver.execute_script(SHADOW_SEARCH_JS,
                                    [k.lower() for k in keywords])

    if not elements:
        logger.info("No shadow DOM chatbot window candidates found.")
        return []
    
    logger.info(f"Found {len(elements)} shadow DOM chatbot window candidates.")

    return elements