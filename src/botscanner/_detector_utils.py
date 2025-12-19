from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from .patterns import CORE_ANCHORS_PATTERNS
from .utils import vprint
from .jstools.wait_iframes import WAIT_FOR_ALL_IFRAMES_JS
from .jstools.find_el_computed_style import FIND_ELEMENT_COMPUTED_STYLE_JS
from .jstools.find_el_pointer_cursor import FIND_ELEMENT_POINTER_CURSOR_JS
from selenium.common.exceptions import WebDriverException


def test_function():
    # It checks that the module is imported correctly.
    print("Test function executed.")
    return "test successful"

def _find_elements_by_anchors(driver: WebDriver, quiet: bool = True):
    """
    Finds all elements that contain common chatbot-related anchor texts.

    Returns:
        A list of WebElements that match the anchor text criteria.
    """

    chatbot_anchors = CORE_ANCHORS_PATTERNS.get('chatbot_anchors', [])

    anchor_queries = []
    for anchor in chatbot_anchors:
        anchor_upper = anchor.upper()
        anchor_lower = anchor.lower()
        
        anchor_queries.extend([
            f"//button[contains(translate(@aria-label, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//button[contains(translate(@class, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//button[contains(translate(@id, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//button[contains(translate(., '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//a[contains(translate(@aria-label, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//a[contains(translate(@class, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//a[contains(translate(., '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//div[@role='button' and contains(translate(@aria-label, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//div[@role='button' and contains(translate(@class, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//div[@role='button' and contains(translate(., '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
            f"//*[contains(translate(@class, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')][@role='button']",
            f"//iframe[contains(translate(@title, '{anchor_upper}', '{anchor_lower}'), '{anchor_lower}')]",
        ])

    all_queries = anchor_queries

    try:
        elements = []
        seen_elements = set()

        for xpath in all_queries:
            try:
                found_elements = driver.find_elements(By.XPATH, xpath)
                for elem in found_elements:
                    # Avoid duplicates
                    elem_id = id(elem)
                    if elem_id not in seen_elements:
                        seen_elements.add(elem_id)
                        elements.append(elem)
            except Exception as e:
                # Skip invalid XPath queries
                pass

        vprint(f"Found {len(elements)} element(s) matching chatbot anchors.", quiet)
        return elements

    except Exception as e:
        vprint(f"Error executing anchor text search: {e}", quiet)
        return []


def _find_elements_by_computed_style(driver: WebDriver, quiet: bool = True):
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


def _is_element_interactive(element: WebElement):
    try:
        return element is not None and element.is_displayed() and element.is_enabled()
    except Exception:
        return False


def _find_cursor_is_pointer(container_element: WebElement, driver: WebDriver):
    """
    Finds a clickable element by recursively searching the DOM, intelligently
    prioritizing the content of iframes over their clickable parent containers.

    Args:
        container_element: The parent WebElement to search within.
        driver: The active Selenium WebDriver instance.

    Returns:
        A dictionary containing the found element and the exploration path.
    """

    try:
        result = driver.execute_script(FIND_ELEMENT_POINTER_CURSOR_JS, container_element)
        return result

    except Exception as e:
        print(f"  - An error occurred during the recursive search script: {e}")
        return {'foundElement': None, 'exploredPath': []}


def _find_iframes(driver: WebDriver, result: dict, quiet):
    candidates = []

    iframe_data = driver.execute_async_script(WAIT_FOR_ALL_IFRAMES_JS, 20_000)

    if not iframe_data or not iframe_data.get("found"):
        result["error"] = "No iframes detected after launcher click"
        return result, candidates
        
    iframes = iframe_data.get("iframes", [])
    vprint(f"Detected {len(iframes)} iframe(s)", quiet)

    for idx, iframe in enumerate(iframes):
        iframe_element = None

        try:
            vprint(f"Processing iframe {idx}...", quiet)

            iframe_element = None
                     
            if iframe.get("id"):
                try:
                    iframe_element = driver.find_element(By.ID, iframe["id"])
                except WebDriverException:
                    iframe_element = None
            
            if iframe_element == None:
                continue

            html = iframe_element.get_attribute('outerHTML')

            candidates.append({
                "index": idx,
                "element": iframe_element,
                "html": html
            })

        except WebDriverException:
            vprint("Error: Cross-origin or detached iframe", quiet)

    if not candidates:
        result["error"] = "Iframes detected but none were accessible (same-origin)"

    return result, candidates