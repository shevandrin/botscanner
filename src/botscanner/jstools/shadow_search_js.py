SHADOW_SEARCH_JS = r"""
return (function (KEYWORDS) {
    console.log("Starting shadow DOM chatbot element search (pruned)");

    const results = [];

    function isInShadowDom(el) {
        return el.getRootNode() instanceof ShadowRoot;
    }

    function computeScore(el) {
        const cls = (el.className || "").toString().toLowerCase();
        const id = (el.id || "").toLowerCase();
        const aria = (el.getAttribute?.("aria-label") || "").toLowerCase();

        let score = 0;
        for (const k of KEYWORDS) {
            if (cls.includes(k)) score += 2;
            if (id.includes(k)) score += 3;
            if (aria.includes(k)) score += 3;
        }
        return score;
    }

    function traverse(node) {
        if (!node) return;


        if (node.shadowRoot) {
            traverse(node.shadowRoot);
        }

        if (node.nodeType === Node.ELEMENT_NODE && isInShadowDom(node)) {
            const score = computeScore(node);
            if (score > 0) {
                node.__chatbot_score = score;
                results.push(node);
                return; 
            }
        }

        for (const child of node.children || []) {
            traverse(child);
        }
    }

    traverse(document);
    return results;
})(arguments[0]);
"""