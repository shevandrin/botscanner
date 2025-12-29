from ...patterns import CHATBOT_FRAMEWORKS_PATTERNS

def _find_window_candidates_by_framework(driver, logger):
    """
    Fast DOM-side finder for chatbot window candidates
    based on known chatbot framework patterns.

    Finder only. No evaluation.
    """

    frameworks = CHATBOT_FRAMEWORKS_PATTERNS

    js = """
    const frameworks = arguments[0];
    const results = [];
    const seen = new Set();

    // Pre-collect elements
    const allDivs = document.querySelectorAll("div");
    const allIframes = document.querySelectorAll("iframe");

    function add(el) {
        if (!seen.has(el)) {
            seen.add(el);
            results.push(el);
        }
    }

    // ---- DIV-BASED WINDOWS ----
    for (const el of allDivs) {
        const cls = (el.className || "").toLowerCase();
        const id = (el.id || "").toLowerCase();
        const aria = (el.getAttribute("aria-label") || "").toLowerCase();

        for (const fw of Object.values(frameworks)) {
            if (fw.class) {
                for (const token of fw.class) {
                    if (cls.includes(token.toLowerCase())) {
                        add(el);
                        continue;
                    }
                }
            }

            if (fw.id) {
                for (const token of fw.id) {
                    if (id === token.toLowerCase()) {
                        add(el);
                        continue;
                    }
                }
            }

            if (fw["aria-label"]) {
                for (const token of fw["aria-label"]) {
                    if (aria === token.toLowerCase()) {
                        add(el);
                        continue;
                    }
                }
            }
        }
    }

    // ---- IFRAME-BASED WINDOWS ----
    for (const iframe of allIframes) {
        const cls = (iframe.className || "").toLowerCase();
        const id = (iframe.id || "").toLowerCase();

        for (const fw of Object.values(frameworks)) {
            if (fw.iframe) {
                for (const token of fw.iframe) {
                    const t = token.toLowerCase();
                    if (cls.includes(t) || id.includes(t)) {
                        add(iframe);
                        continue;
                    }
                }
            }
        }
    }

    return results;
    """

    try:
        elements = driver.execute_script(js, frameworks)
        logger.info(
            f"Framework-based window candidates found: {len(elements)}"
        )
        return elements
    except Exception as e:
        logger.error(f"JS framework finder failed: {e}")
        return []

