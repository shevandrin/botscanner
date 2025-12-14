WAIT_FOR_ALL_IFRAMES_JS = """
const callback = arguments[arguments.length - 1];
const start = Date.now();

(function poll() {
    const iframes = document.querySelectorAll('iframe');

    if (iframes.length > 0) {
        const iframeList = Array.from(iframes).map((iframe, index) => ({
            index: index,
            id: iframe.id || null,
            title: iframe.title || null,
            src: iframe.src || null,
            name: iframe.name || null,
            html: iframe.outerHTML || null,
            visible: !!(
                iframe.offsetWidth ||
                iframe.offsetHeight ||
                iframe.getClientRects().length
            )
        }));

        callback({
            found: true,
            iframes: iframeList
        });
        return;
    }

    if (Date.now() - start > arguments[0]) {
        callback({ found: false, iframes: [] });
        return;
    }

    setTimeout(poll, 200);
})();
"""
