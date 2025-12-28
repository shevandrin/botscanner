from selenium.webdriver.common.by import By
from botscanner.patterns import CHATBOT_WINDOWS_HOOKS_PATTERNS


def _find_windows_candidates_by_hooks(driver, logger):
    """
    Finds DOM-based chatbot window candidates using heuristic hooks.

    - Only <div> elements
    - Excludes iframes
    - Matches against class, id, and aria-label
    - Finder only (no evaluation)

    Returns:
        A list of WebElements
    """

    js = """
        const indicators = arguments[0];

        const results = [];
        const divs = document.querySelectorAll("div");

        for (const el of divs) {
            const style = window.getComputedStyle(el);
            if (style.display === "none" || style.visibility === "hidden") continue;

            const rect = el.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) continue;

            if (el.querySelector("iframe")) continue;

            const cls = (el.className || "").toLowerCase();
            const id = (el.id || "").toLowerCase();
            const aria = (el.getAttribute("aria-label") || "").toLowerCase();

            for (const token of indicators) {
                if (
                    cls.includes(token) ||
                    id.includes(token) ||
                    aria.includes(token)
                ) {
                    results.push(el);
                    break;
                }
            }
        }

        return results;
        """

    try:
        elements = driver.execute_script(js, CHATBOT_WINDOWS_HOOKS_PATTERNS)
        logger.info(
            f"Found {len(elements)} simple DOM chatbot window candidate(s)."
        )
        return elements
    except Exception as e:
        logger.error(f"JS window hook finder failed: {e}")
        return []