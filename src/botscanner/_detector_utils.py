from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from .patterns import CORE_ANCHORS_PATTERNS
from .jstools.wait_iframes import WAIT_FOR_ALL_IFRAMES_JS
from .jstools.find_el_computed_style import FIND_ELEMENT_COMPUTED_STYLE_JS
from .jstools.find_el_pointer_cursor import FIND_ELEMENT_POINTER_CURSOR_JS
from selenium.common.exceptions import WebDriverException


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