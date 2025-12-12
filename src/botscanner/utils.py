from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
)


def _is_element_clickable(element: WebElement, driver: WebDriver = None) ->  bool:
    """
    Checks if a WebElement is clickable WITHOUT clicking it.
    
    Tests: visibility, enabled state, size, location, CSS properties, and cursor style.
    Safe to use - does NOT modify page state.
    
    Args:
        element: The WebElement to check
        driver: WebDriver instance for JavaScript checks
        
    Returns:
        True if element is clickable, False otherwise
    """
    try:
        # Check 1: Element is displayed
        if not element.is_displayed():
            print(f"  ✗ Not displayed")
            return False
        
        # Check 2: Element is enabled
        if not element.is_enabled():
            print(f"  ✗ Not enabled")
            return False
        
        # Check 3: Element has size
        size = element.size
        if size['width'] == 0 or size['height'] == 0:
            print(f"  ✗ Zero size")
            return False
        
        # Check 4: Element is in viewport
        location = element.location
        if location['x'] < 0 or location['y'] < 0:
            print(f"  ✗ Outside viewport")
            return False
        
        # Check 5: CSS properties and cursor style
        if driver:
            script = """
            const elem = arguments[0];
            const style = window.getComputedStyle(elem);
            
            if (style.opacity === '0') return 'opacity-zero';
            if (style.visibility === 'hidden') return 'visibility-hidden';
            if (style.display === 'none') return 'display-none';
            if (style.pointerEvents === 'none') return 'pointer-events-none';
            if (style.cursor !== 'pointer') return 'cursor-not-pointer';
            
            return 'ok';
            """
            result = driver.execute_script(script, element)
            if result != 'ok':
                print(f"  ✗ CSS issue: {result}")
                return False
        
        print(f"  ✓ Clickable (cursor: pointer)")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False