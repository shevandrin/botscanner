SHADOW_SEARCH_JS = r"""
(function () {
    const results = [];
    const KEYWORDS = ['chat', 'widget', 'bot', 'support', 'conversation'];

    document.querySelectorAll('iframe').forEach(iframe => {
        const id = (iframe.id || '').toLowerCase();
        const title = (iframe.title || '').toLowerCase();
        const src = (iframe.src || '').toLowerCase();

        if (KEYWORDS.some(k => id.includes(k) || title.includes(k) || src.includes(k))) {
            results.push({
                type: 'iframe',
                id: iframe.id || null,
                title: iframe.title || null,
                class: iframe.className || null,
                src: iframe.src || null,
                cross_origin: true
            });
        }
    });

    return results;
})();
"""