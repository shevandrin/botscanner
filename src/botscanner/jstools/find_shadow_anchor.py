SHADOW_ANCHOR = r"""
return (function (KEYWORDS) {
  const results = [];

  function isClickable(el) {
    el.scrollIntoView({ block: "center", inline: "center" });

    const clickRect = el.getBoundingClientRect();
    const clickStyle = window.getComputedStyle(el);

    return (
      clickRect.width > 0 &&
      clickRect.height > 0 &&
      clickStyle.display !== "none" &&
      clickStyle.visibility !== "hidden" &&
      clickStyle.opacity !== "0" &&
      clickStyle.pointerEvents !== "none"
    );
  }


  function traverse(root, hostChain = []) {
    if (!root) return;

    const elements = root.querySelectorAll('*');

    for (const el of elements) {
      try {
        const cls = (el.className || '').toString().toLowerCase();
        const id = (el.id || '').toLowerCase();
        const aria = (el.getAttribute?.('aria-label') || '').toLowerCase();
        const text = (el.innerText || '').toLowerCase();
        const imgAlt = el.querySelector('img')?.alt?.toLowerCase() || '';

        let keywordHits = 0;
        for (const k of KEYWORDS) {
          if (cls.includes(k)) keywordHits++;
          if (id.includes(k)) keywordHits++;
          if (aria.includes(k)) keywordHits++;
          if (text.includes(k)) keywordHits++;
          if (imgAlt.includes(k)) keywordHits++;
        }

        if (keywordHits > 0) {
          const rect = el.getBoundingClientRect();
          const style = window.getComputedStyle(el);

          results.push({
            width: rect.width,
            height: rect.height,
            display: style.display,
            visibility: style.visibility,
            opacity: style.opacity,
            pointerEvents: style.pointerEvents,
            tag: el.tagName.toLowerCase(),
            keywordHits,
            text: text.slice(0, 200),
            html: el.outerHTML,
            clickable: isClickable(el),
            cursor: style.cursor,
            bounding: {
              x: rect.x, y: rect.y,
              width: rect.width, height: rect.height
            },
            hostChain: [...hostChain]
          });
        }

        if (el.shadowRoot) {
          traverse(el.shadowRoot, [...hostChain, el.tagName.toLowerCase()]);
        }
      } catch (_) {}
    }
  }

  traverse(document);
  return results;
})(arguments[0]);
"""