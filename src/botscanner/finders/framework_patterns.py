from selenium.webdriver.common.by import By
from ..patterns import CHATBOT_FRAMEWORKS_PATTERNS

def _find_windows_candidates_by_framework(driver, logger):
    """
    Finds chatbot *window* elements in the main DOM based on known
    chatbot framework patterns (class, id, iframe, etc.).
    Args:
        driver: Selenium WebDriver instance
        logger: Logger instance

    Returns:
        List[WebElement]
    """
    candidates = []
    seen = set()

    frameworks = CHATBOT_FRAMEWORKS_PATTERNS

    for framework_name, selectors in frameworks.items():
        logger.info(f"Scanning for chatbot framework: {framework_name}")


        for selector_type, values in selectors.items():
            for value in values:
                try:
                    if selector_type == "class":
                        xpath = f"//*[contains(@class, '{value}')]"

                    elif selector_type == "id":
                        xpath = f"//*[@id='{value}']"

                    elif selector_type == "iframe":
                        xpath = f"//iframe[contains(@class, '{value}') or contains(@id, '{value}')]"

                    elif selector_type == "area-label":
                        xpath = f"//*[@aria-label='{value}']"

                    else:
                        # Unknown selector type → ignore safely
                        continue
                    logger.debug(xpath)
                    elements = driver.find_elements(By.XPATH, xpath)

                    for el in elements:
                        el_id = id(el)
                        if el_id not in seen:
                            seen.add(el_id)
                            candidates.append(el)

                except Exception as e:
                    logger.error(
                        f"Error while searching {framework_name} ({selector_type}={value}): {e}"
                    )

    logger.info(f"Framework-based window candidates found: {len(candidates)}")
    return candidates
