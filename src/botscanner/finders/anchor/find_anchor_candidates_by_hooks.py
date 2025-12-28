from ..patterns import CORE_ANCHORS_PATTERNS
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def _find_anchor_candidates_by_hooks(driver: WebDriver, logger):
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

        logger.info(f"Found {len(elements)} element(s) matching chatbot anchors.")
        return elements

    except Exception as e:
        logger.error(f"Error executing anchor text search: {e}")
        return []
