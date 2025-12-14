FIND_ELEMENT_POINTER_CURSOR_JS = """
function getXPath(node) {
    if (!node || node.nodeType !== 1) { // Only process element nodes (type 1)
            return '';
        }
        if (node === document.body) {
            return '/html/body';
        }
        if (node.id) {
            return '//*[@id="' + node.id + '"]';
        }

        const parent = node.parentNode;
        // Handle root elements that might not have a parent with children
        if (!parent || !parent.children) {
            return node.tagName.toLowerCase();
        }

        const siblings = Array.from(parent.children);
        const sameTagSiblings = siblings.filter(sibling => sibling.tagName === node.tagName);

        if (sameTagSiblings.length > 1) {
            // Find the 1-based index of the element among its siblings of the same tag
            const index = sameTagSiblings.indexOf(node) + 1;
            return getXPath(parent) + '/' + node.tagName.toLowerCase() + '[' + index + ']';
        } else {
            return getXPath(parent) + '/' + node.tagName.toLowerCase();
        }
    }

    function getAttributes(element) {
        if (!element.attributes) return {};
        return Array.from(element.attributes).reduce((obj, attr) => {
            obj[attr.name] = attr.value;
            return obj;
        }, {});
    }


    function findPointerCursorElements(startNode, maxDepth = 10, currentDepth = 0, iframeXPath = null) {
        if (!startNode || currentDepth > maxDepth) return [];

        const results = [];

        try {
            if (startNode.nodeType === 1 || startNode.nodeType === 11) { // Element or ShadowRoot

                if (startNode.nodeType === 1 && window.getComputedStyle(startNode).cursor === 'pointer') {
                    results.push({
                        tagName: startNode.tagName,
                        id: startNode.id,
                        className: startNode.className,
                        text: startNode.textContent?.trim()?.slice(0, 100) || '',
                        xpath: getXPath(startNode),
                        attributes: getAttributes(startNode),
                        iframe_xpath: iframeXPath 
                    });
                }

                const children = Array.from(startNode.children || []);
                for (const child of children) {
                    if (child.tagName === 'IFRAME') {
                        const currentIframeXPath = getXPath(child);
                        try {
                            const iframeDoc = child.contentDocument || child.contentWindow?.document;
                            if (iframeDoc?.body) {
                                results.push(...findPointerCursorElements(iframeDoc.body, maxDepth, currentDepth + 1, currentIframeXPath));
                            }
                        } catch (e) {
                            console.warn('Cannot access iframe content:', child);
                        }
                    } 
                    else if (child.shadowRoot) {
                        results.push(...findPointerCursorElements(child.shadowRoot, maxDepth, currentDepth + 1, iframeXPath));
                    }
                    else {
                        results.push(...findPointerCursorElements(child, maxDepth, currentDepth + 1, iframeXPath));
                    }
                }
            }
        } catch (e) {
            console.error('Error checking element:', startNode, e);
        }

        return results;
    }

    return findPointerCursorElements(arguments[0], 10, 0, null);
"""