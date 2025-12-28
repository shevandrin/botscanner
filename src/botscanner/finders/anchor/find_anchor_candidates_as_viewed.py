from botscanner.jstools.find_el_anchor_viewpoint import FIND_VIEWPORT_ANCHORED_INTERACTIVE_ELEMENTS_JS
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def _find_anchor_candidates_as_viewed(driver: WebDriver, logger):
    """
    Finds anchor candidates that are positioned within the viewport
    and exhibit interactive affordances based on computed styles.

    Args:
        driver: The active Selenium WebDriver instance
        logger: Logger instance for logging information

    Returns:
        A list of WebElements that match the style criteria.
    """


    try:
        elements = driver.execute_script(FIND_VIEWPORT_ANCHORED_INTERACTIVE_ELEMENTS_JS)
        if elements:
            logger.info(f"Found {len(elements)} element(s) matching viewport criteria.")
            return elements
        else:
            logger.info("No elements matched the viewport criteria.")
            return []
    except Exception as e:
        logger.error(f"Error executing viewport anchored interactive elements search script: {e}")
        return []