# finds button by text from 'phrases'
FIND_BUTTON_BY_TEXT_JS = """
    const phrases = arguments[0].map(p => p.toLowerCase());
    const results = [];

    function walk(root) {
      const tree = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
      let node;
      while ((node = tree.nextNode())) {
        if (node.shadowRoot) walk(node.shadowRoot);
        const tag = (node.tagName || '').toLowerCase();
        if (tag === 'button' || (node.getAttribute && node.getAttribute('role') === 'button')) {
          const txt = (node.textContent || '').trim().toLowerCase();
          if (txt && phrases.some(p => txt.includes(p))) {
            results.push(node);
          }
        }
      }
    }

    walk(document);
    return results;
"""