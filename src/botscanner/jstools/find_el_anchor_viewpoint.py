FIND_VIEWPORT_ANCHORED_INTERACTIVE_ELEMENTS_JS = r"""
return (function () {

    const candidates = [];
    const visited = new Set();

    const vw = window.innerWidth;
    const vh = window.innerHeight;

    const EDGE_X = Math.min(320, vw * 0.35);
    const EDGE_Y = Math.min(240, vh * 0.30);

    function isVisible(el) {
        const r = el.getBoundingClientRect();
        const s = window.getComputedStyle(el);
        return (
            r.width > 20 &&
            r.height > 20 &&
            s.display !== 'none' &&
            s.visibility !== 'hidden' &&
            s.opacity !== '0' &&
            s.pointerEvents !== 'none'
        );
    }

    function normalizeTarget(el, maxDepth = 4) {
        let cur = el;
        let depth = 0;

        while (cur && depth <= maxDepth && cur !== document.body) {
            if (isVisible(cur)) return cur;
            cur = cur.parentElement;
            depth++;
        }
        return null;
    }

    for (let dx = 0; dx <= 40; dx += 10) {
        for (let dy = 0; dy <= 40; dy += 10) {

            const x = vw - 10 - dx;
            const y = vh - 10 - dy;

            const hit = document.elementFromPoint(x, y);
            if (!hit || visited.has(hit)) continue;
            visited.add(hit);

            try {
                const interactive = normalizeTarget(hit);
                if (!interactive) continue;

                const r = interactive.getBoundingClientRect();

                const nearBottomRight =
                    (vw - r.right) <= EDGE_X &&
                    (vh - r.bottom) <= EDGE_Y;

                if (!nearBottomRight) continue;

                if (r.width > vw * 0.7 || r.height > vh * 0.7) continue;

                candidates.push(interactive);

            } catch (e) {
                continue;
            }
        }
    }

    return candidates;
})();
"""