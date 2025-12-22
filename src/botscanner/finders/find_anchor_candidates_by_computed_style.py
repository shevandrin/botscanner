from botscanner.jstools.find_el_computed_style import FIND_ELEMENT_COMPUTED_STYLE_JS
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def _find_anchor_candidates_by_computed_style(driver: WebDriver, logger):
    """
    Finds all elements that match specific computed style properties
    common to chatbot widgets (e.g., fixed position, high z-index).

    Args:
        driver: The active Selenium WebDriver instance
        logger: Logger instance for logging information

    Returns:
        A list of WebElements that match the style criteria.
    """


    try:
        elements = driver.execute_script(FIND_ELEMENT_COMPUTED_STYLE_JS)
        if elements:
            logger.info(f"Found {len(elements)} element(s) matching computed style criteria.")
            return elements
        else:
            logger.info("No elements matched the computed style criteria.")
            return []
    except Exception as e:
        logger.error(f"Error executing computed style search script: {e}")
        return []