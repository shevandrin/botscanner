SHADOW_ANCHOR = r"""
return (function (KEYWORDS) {
  const results = [];
  const MAX_TEXT_LEN = 200;

  const ALLOWED_TAGS = new Set([
    "button",
    "a",
    "svg",
    "img"
  ]);

  /* ---------- helpers ---------- */

  function normalize(str) {
    return (str || "").toString().toLowerCase();
  }

  function isVisible(style) {
    return (
      style.display !== "none" &&
      style.visibility !== "hidden" &&
      style.opacity !== "0" &&
      style.pointerEvents !== "none"
    );
  }

  function isTopMost(el, rect) {
    try {
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const topEl = document.elementFromPoint(cx, cy);

      if (!topEl) return true;

      if (el.contains(topEl)) return true;

      const style = window.getComputedStyle(el);
      if (
        el.tagName === "BUTTON" ||
        style.cursor === "pointer"
      ) {
        return true;
      }

      return false;
    } catch {
      return true; // fail open, not closed
    }
  }

  function isClickable(el) {
    try {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return false;

      const style = window.getComputedStyle(el);
      if (!isVisible(style)) return false;
      if (!isTopMost(el, rect)) return false;

      if (
        el.tagName === "BUTTON" &&
        style.cursor === "pointer"
      ) {
        return true;
      }
      
      return (
        style.cursor === "pointer" ||
        el.tagName === "BUTTON" ||
        el.getAttribute("role") === "button" ||
        el.hasAttribute("tabindex")
      );
    } catch {
      return false;
    }
  }

  function keywordScore(el) {
    const cls = normalize(el.className);
    const id = normalize(el.id);
    const aria = normalize(el.getAttribute?.("aria-label"));
    const text = normalize(el.innerText);
    const alt = normalize(el.querySelector("img")?.alt);

    let hits = 0;
    for (const k of KEYWORDS) {
      if (cls.includes(k)) hits++;
      if (id.includes(k)) hits++;
      if (aria.includes(k)) hits++;
      if (text.includes(k)) hits++;
      if (alt.includes(k)) hits++;
    }
    return hits;
  }

  function isAllowedCandidate(el) {
    const tag = el.tagName.toLowerCase();

    if (ALLOWED_TAGS.has(tag)) return true;

    if (
      tag === "div" &&
      el.getAttribute("role") === "button"
    ) return true;

    if (
      tag === "span" &&
      el.getAttribute("role") === "button"
    ) return true;

    return false;
  }

  function hostFingerprint(el) {
    return {
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      class: normalize(el.className).slice(0, 80) || null
    };
  }

  /* ---------- traversal ---------- */

  function traverse(root, hostChain = []) {
    if (!root || !root.querySelectorAll) return;

    const all = root.querySelectorAll("*");

    for (const el of all) {
      try {
        const tag = el.tagName.toLowerCase();
        if (
          tag === "head" ||
          tag === "script" ||
          tag === "style" ||
          tag === "meta" ||
          tag === "link"
        ) {
          continue;
        }

        if (isAllowedCandidate(el)) {
          const hits = keywordScore(el);
          if (hits > 0) {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);

            results.push({
              tag,
              identifiers: {
                id: el.id ? normalize(el.id) : null,
                class: el.className ? normalize(el.className).slice(0, 80) : null,
                name: el.getAttribute("name"),
                ariaLabel: normalize(el.getAttribute("aria-label"))
              },
              keywordHits: hits,
              clickable: isClickable(el),
              cursor: style.cursor,
              text: normalize(el.innerText).slice(0, MAX_TEXT_LEN),
              html: el.outerHTML,
              bounding: {
                x: rect.left + window.scrollX,
                y: rect.top + window.scrollY,
                width: rect.width,
                height: rect.height
              },
              style: {
                position: style.position,
                zIndex: style.zIndex
              },
              hostChain: hostChain.map(h => ({ ...h }))
            });
          }
        }

        if (el.shadowRoot) {
          traverse(
            el.shadowRoot,
            [...hostChain, hostFingerprint(el)]
          );
        }
      } catch (_) {}
    }
  }

  traverse(document, []);
  return results.filter(r => r.hostChain && r.hostChain.length > 0);
})(arguments[0]);

"""


SHADOW_ANCHOR_old = r"""
return (function (KEYWORDS) {
  const results = [];

  function isClickable(el) {
    el.scrollIntoView({ block: "center", inline: "center" });

    const clickRect = el.getBoundingClientRect();
    const clickStyle = window.getComputedStyle(el);

    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const topEl = document.elementFromPoint(cx, cy);
    if (topEl && !el.contains(topEl) && !topEl.contains(el)) return false;

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

    const elements = root.querySelectorAll('button, a, div[role="button"], span[role="button"], svg, img');


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