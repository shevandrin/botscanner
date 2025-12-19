from selenium.webdriver.common.by import By
from ..jstools.wait_iframes import WAIT_FOR_ALL_IFRAMES_JS
from ..utils import vprint


def _find_iframe_chatbot_windows(driver, quiet: bool = True):
    """
    Finds chatbot windows within same-origin iframes on the page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        quiet (bool): If True, suppresses verbose output.
    Returns:
        List of ChatbotWindowCandidate objects found within iframes.
    """

    elements = driver.execute_async_script(WAIT_FOR_ALL_IFRAMES_JS, 20_000)

    if not elements or not elements.get("found"):
        vprint("No iframes found on the page.", quiet)

    iframes = elements.get("iframes", [])
    vprint(f"Detected {len(iframes)} iframe(s)", quiet)

    candidates = []

    for iframe in iframes:
        try:
            # Warning: it skips invisible iframes
            if not iframe.is_displayed():
                continue

            candidates.append(iframe)

        except Exception:
            # Cross-origin or detached iframe
            continue

    return candidates