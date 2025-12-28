FIND_VIEWPORT_ANCHORED_INTERACTIVE_ELEMENTS_JS = r"""
(function () {

    const candidates = [];
    const elements = document.querySelectorAll('div, button, a, span');

    const vw = window.innerWidth;
    const vh = window.innerHeight;

    for (const el of elements) {
        try {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);

            // ---- Visibility check ----
            const isVisible =
                rect.width > 20 &&
                rect.height > 20 &&
                style.display !== 'none' &&
                style.visibility !== 'hidden' &&
                style.opacity !== '0';

            if (!isVisible) continue;

            // ---- Viewport bottom-right zone ----
            // bottom-right 30% × 30% of viewport
            const inBottomRight =
                rect.left >= vw * 0.65 &&
                rect.top >= vh * 0.65 &&
                rect.right <= vw &&
                rect.bottom <= vh;

            if (!inBottomRight) continue;

            // ---- Interaction affordance ----
            const hasPointerCursor = style.cursor === 'pointer';
            const hasRoleButton = el.getAttribute('role') === 'button';
            const hasOnClick =
                typeof el.onclick === 'function' ||
                el.hasAttribute('onclick');

            if (!(hasPointerCursor || hasRoleButton || hasOnClick)) continue;

            // ---- Exclude obvious layout noise ----
            const isTooLarge =
                rect.width > vw * 0.6 ||
                rect.height > vh * 0.6;

            if (isTooLarge) continue;

            // ---- Collect candidate ----
            candidates.push({
                element: el,
                rect: {
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                },
                affordance: {
                    cursor: style.cursor,
                    role: el.getAttribute('role'),
                    onclick: !!el.onclick
                }
            });

        } catch (e) {
            // Ignore detached / stale nodes
            continue;
        }
    }

    return candidates;
})();
"""