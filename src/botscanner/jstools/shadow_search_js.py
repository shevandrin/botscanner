SHADOW_SEARCH_JS = r"""
(function (KEYWORDS) {
    const results = [];

    function traverse(root) {
        if (!root) return;

        const elements = root.querySelectorAll('*');
        for (const el of elements) {
            const cls = (el.className || '').toString().toLowerCase();
            const id = (el.id || '').toLowerCase();
            const aria = (el.getAttribute && el.getAttribute('aria-label') || '').toLowerCase();

            let score = 0;
            for (const k of KEYWORDS) {
                if (cls.includes(k)) score += 2;
                if (id.includes(k)) score += 2;
                if (aria.includes(k)) score += 3;
            }

            if (score > 0) {
                el.__chatbot_score = score;
                results.push(el);
            }

            if (el.shadowRoot) {
                traverse(el.shadowRoot);
            }
        }
    }

    traverse(document);
    return results;
})
"""