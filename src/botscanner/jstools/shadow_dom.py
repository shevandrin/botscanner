SHADOW_DOM_OVERRIDE_JS = r"""
(function () {
    if (Element.prototype.__shadowPatched) return;

    const originalAttachShadow = Element.prototype.attachShadow;

    Element.prototype.attachShadow = function (init) {
        const shadowRoot = originalAttachShadow.call(this, init);

        Object.defineProperty(this, "__shadowRoot", {
            value: shadowRoot,
            writable: false,
            configurable: false
        });

        return shadowRoot;
    };

    Element.prototype.__shadowPatched = true;
})();
"""