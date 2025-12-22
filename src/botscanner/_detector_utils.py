from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


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
        driver.execute_script("arguments[0].click();", element)
        logger.info("Chatbot launcher clicked via JS")
        return True

def _get_html_from_element(element: WebElement, driver: WebDriver):
    """
    Provides with HTML of an element, handling iframes.
    Args:
        element:
        driver:

    Returns:
        The HTML content as a string.
    """

    wrapper_html = element.get_attribute("outerHTML")
    soup = BeautifulSoup(wrapper_html, features="html.parser")

    iframe_tag = soup.find('iframe')
    if not iframe_tag:
        return wrapper_html

    try:
        live_iframe = element.find_element(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(live_iframe)
        iframe_html = driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')
        driver.switch_to.default_content()
        print("  - Successfully extracted iframe HTML and switched back.")
    except Exception as e:
        print(f"  - Error switching to iframe: {e}")
        driver.switch_to.default_content()
        iframe_html = "<!-- Could not retrieve iframe content -->"

    iframe_soup = BeautifulSoup(iframe_html, features="html.parser")
    iframe_tag.clear()
    iframe_tag.append(iframe_soup)

    return soup.prettify()