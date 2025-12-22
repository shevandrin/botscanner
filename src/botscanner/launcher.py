# launcher.py
import requests
from selenium import webdriver
from ._launcher_utils import _prepare_url, _handle_cookie_consent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from .jstools.shadow_dom import SHADOW_DOM_OVERRIDE_JS
import time


def check_ip():
    """
    Returns the current public IP address of the machine.

    Returns:
        str: The public IP address, or None if the request fails.
    """
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json()['ip']
    except requests.RequestException:
        return None
    except Exception as e:
        print(f"An unexpected error occurred in check_ip: {e}")
        return None


def install_shadow_dom_override(driver):
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": SHADOW_DOM_OVERRIDE_JS}
    )


def launch_page(
        url: str,
        logger,
        keep_open: bool = True,
        handle_cookies: bool = True,
        wait_seconds: int = 10,
        ):
    """Launches a Chrome browser to the specified URL.

    Args:
        url (str): The URL to open.
        logger: Logger instance for logging messages.
        keep_open (bool): If True, the browser window will remain open
            after the function finishes. Defaults to True.
        handle_cookies (bool): If True, handle cookie consent. Defaults to True.
        wait_seconds (int): Number of seconds to wait after loading the page. Defaults to 10.

    Returns:
        driver: Selenium Chrome webdriver.
    """
    ip = check_ip()
    url = _prepare_url(url)
    print(f"Launching browser to {url} | Current public IP: {ip or 'Unable to retrieve'}")

    chrome_options = Options()
    if keep_open:
        chrome_options.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(options=chrome_options)
        install_shadow_dom_override(driver)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception as e:
        if logger:
            logger.error(f"Error launching browser: {e}")
        return None

    if handle_cookies: _handle_cookie_consent(driver, logger=logger)
    
    time.sleep(wait_seconds)
    return driver
