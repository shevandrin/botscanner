import time
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    JavascriptException,
    WebDriverException,
)


def snapshot_state(driver):
    return {
        "iframes": driver.execute_script("return document.querySelectorAll('iframe').length"),
        "html_len": len(driver.page_source),
    }

def wait_for_effect(driver, timeout=2.0):
    import time
    start = time.time()
    before = snapshot_state(driver)

    while time.time() - start < timeout:
        time.sleep(0.2)
        after = snapshot_state(driver)

        if after != before:
            return True, after

    return False, before


def clicking_inside_iframe(driver: WebDriver, iframe_element: WebElement, logger) -> bool:
    """
    Try to activate chatbot by clicking elements inside an iframe.

    Returns:
        bool: True if some observable DOM change happened after interaction,
              False otherwise.
    """

    def snapshot_state():
        return driver.execute_script("""
            return {
                iframeCount: document.querySelectorAll("iframe").length,
                bodyLength: document.body ? document.body.innerHTML.length : 0
            };
        """)

    try:
        driver.switch_to.frame(iframe_element)
    except WebDriverException as e:
        logger.warning("Cannot switch to iframe (possibly cross-origin): %s", e)
        return False

    try:
        before = snapshot_state()

        # Collect clickable candidates
        candidates = []

        # Native buttons
        candidates.extend(driver.find_elements(By.TAG_NAME, "button"))

        # Button-like divs
        candidates.extend(driver.find_elements(
            By.XPATH,
            "//div[@role='button' or @onclick or contains(@style,'cursor: pointer')]"
        ))

        # Filter visible & non-zero size
        def is_interactable(el):
            try:
                return el.is_displayed() and el.size["width"] > 0 and el.size["height"] > 0
            except StaleElementReferenceException:
                return False

        candidates = [c for c in candidates if is_interactable(c)]

        if not candidates:
            logger.info("No clickable elements found inside iframe")
            return False

        logger.info("Found %d clickable candidates inside iframe", len(candidates))

        for idx, el in enumerate(candidates):
            try:
                # Try native click
                try:
                    el.click()
                    logger.debug("Clicked candidate %d via native click", idx)
                except Exception:
                    driver.execute_script("arguments[0].click()", el)
                    logger.debug("Clicked candidate %d via JS click", idx)

                time.sleep(0.6)

                after = snapshot_state()

                if after != before:
                    logger.info("DOM change detected after iframe interaction")
                    return True

            except (StaleElementReferenceException, JavascriptException) as e:
                logger.debug("Skipping candidate %d due to error: %s", idx, e)
                continue

        logger.info("Iframe interaction attempted but no DOM changes detected")
        return False

    finally:
        driver.switch_to.default_content()



def click_chatbot_launcher(element, driver, logger):
    """
    Attempts to click a chatbot launcher element using native click first,
    falling back to JavaScript click if necessary.
    """
    logger.info("Safe clicking chatbot launcher...")

    try:
        element.click()
        logger.info("Chatbot launcher clicked via native click")
        return True
    except Exception as e:
        logger.warning(
            "Native click failed, falling back to JS click",
            extra={"error": str(e)}
        )
        before = snapshot_state(driver)
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        after = snapshot_state(driver)
        if after != before:
            logger.info("Chatbot launcher clicked via JS, DOM change detected")
            return True
        else:
            logger.warning("No DOM change detected after JS click")
            return clicking_inside_iframe(driver, element, logger)
        return True