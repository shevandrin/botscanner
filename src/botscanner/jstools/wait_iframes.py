WAIT_FOR_ALL_IFRAMES_JS = """
const callback = arguments[arguments.length - 1];
const timeout = arguments[0] || 20000;
const start = Date.now();

(function poll() {
    const iframes = Array.from(document.querySelectorAll('iframe'));

    if (iframes.length > 0) {
        callback({
            found: true,
            iframes: iframes
        });
        return;
    }

    if (Date.now() - start > timeout) {
        callback({
            found: false,
            iframes: []
        });
        return;
    }

    setTimeout(poll, 200);
})();
"""
