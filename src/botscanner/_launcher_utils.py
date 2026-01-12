from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from .patterns import load_patterns, get_cookie_patterns
from .jstools.find_button_by_text import FIND_BUTTON_BY_TEXT_JS

patterns = load_patterns()
COOKIE_PATTERNS = get_cookie_patterns(patterns)


def _prepare_url(url: str) -> str:
    """
    Ensures the URL starts with 'http://' or 'https://'
    and ends with a trailing slash '/'.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not url.endswith("/"):
        url += "/"

    return url

def _query_shadow_buttons(driver, phrases):
    """
    Searches for buttons with matching text phrases in shadow DOM and regular DOM.
    
    Args:
        driver: The active Selenium WebDriver instance.
        phrases: A list of text phrases to search for in button elements.
    
    Returns:
        A list of button elements whose text content contains any of the phrases.
    """

    return driver.execute_script(FIND_BUTTON_BY_TEXT_JS, phrases)

def _handle_cookie_consent(driver: WebDriver, logger):
    """
    Attempts to find and click a cookie consent button.

    This function uses a list of common XPath selectors for cookie banners
    and tries to click them. It fails gracefully if no banner is found.

    Args:
        driver: The active Selenium WebDriver instance.
        logger: Logger for logging messages.
    """

    time.sleep(6)
    # Forming a list of common patterns for "accept" buttons.
    text_phrases = COOKIE_PATTERNS.get('button_text_phrases', [])
    literal_xpaths = COOKIE_PATTERNS.get('literal_xpaths', [])
    generated_xpaths = [f"//button[contains(., '{phrase}')]" for phrase in text_phrases]
    common_button_xpaths = generated_xpaths + literal_xpaths
    logger.info("Attempting to handle cookie consent banner...")

    # main DOM traversal
    for xpath in common_button_xpaths:
        # Find the button using the current XPath
        consent_buttons = driver.find_elements(By.XPATH, xpath)
        for button in consent_buttons:
            try:
                # If found, try to click it
                if button.is_displayed() and button.is_enabled():
                    logger.debug(f"  - Found consent button with XPath: {xpath}")
                    button.click()
                    logger.debug("  - Clicked the consent button.")
                    time.sleep(1)
                    return
            except NoSuchElementException:
                # This is expected: the button for this XPath doesn't exist.
                continue
            except ElementClickInterceptedException:
                # The button might be temporarily unclickable, try a JS click.
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)
                return
            except Exception as e:
                # Catch any other unexpected errors
                logger.error(f"  - Click failed for XPath {xpath}: {e}")
                continue
    
    # shadow DOM traversal
    try:
        logger.info("  - No regular banner found. Searching shadow roots...")
        shadow_buttons = _query_shadow_buttons(driver, text_phrases)
        for el in shadow_buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                driver.execute_script("arguments[0].click();", el)
                logger.info("  - Clicked consent button inside shadow root.")
                time.sleep(1)
                return
            except Exception as e:
                logger.error(f"  - Shadow-root click failed: {e}")
                continue
    except Exception as e:
        logger.error(f"  - Shadow-root traversal error: {e}")
        
    logger.info("  - No cookie consent banner found, or it was already handled.")
            
            
def _check_robots_txt(driver: WebDriver) -> bool:
    """
    Reads the robots.txt file for the current page and checks if crawlers are allowed.
                
    Args:
        driver: The active Selenium WebDriver instance.
                    
    Returns:
        True if crawling is allowed, False if forbidden.
    """
    
    from urllib.parse import urlparse
    from robotexclusionrulesparser import RobotExclusionRulesParser
    import requests

    try:
        # Get the current URL from the driver
        url = driver.current_url
        
        # Prepare the robots.txt URL
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        try:
            text = requests.get(robots_url, timeout=5).text
        except Exception:
            return True
              
        rp = RobotExclusionRulesParser()
        rp.parse(text)

        path = parsed.path or "/"

        return rp.is_allowed("*", path)
                        
    except Exception as e:
        print(f"⚠ Could not read robots.txt: {e}")
        return True  # Assume allowed if robots.txt is inaccessible
