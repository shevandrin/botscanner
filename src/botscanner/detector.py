from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from ._detector_utils import _find_elements_by_computed_style, _get_html_from_element, _is_element_interactive, _find_cursor_is_pointer, _find_elements_by_anchors, _finalize_shadow_result, _find_iframes
from .utils import vprint, _is_element_clickable
import json
from .jstools.shadow_search_js import SHADOW_SEARCH_JS
from .evaluators.eval_iframe_chatbot_window import _evaluate_iframe_candidate
from .selectors.select_anchor_chatbot_widget import select_anchor_chatbot_widget
import time




class ChatbotDetector:
    """Handles detection of chatbot widget on web pages."""
    def __init__(self, outcome_writer):
        self.outcome_writer = outcome_writer

    def discover_chatbot(self, driver: WebDriver, quiet: bool = True) -> None:
        """
        Discover chatbot anchors that launch chatbot widgets.

        Returns:
            (candidate_element_or_None, stats_json)
        """
        vprint("Discovering chatbot launcher elements (anchors)...", quiet)

        stats = {
            "s1_candidates": 0
            ,"s2_candidates": 0
        }
        candidate = None

        candidates_log = {
        "strategy_1": [],
        "strategy_2": []
        }

        # The first starategy is to find elements by anchors
        s1_elements = _find_elements_by_anchors(driver, quiet)
        if len(s1_elements) > 0:
            s1_elements_clickable = [_is_element_clickable(el, driver, quiet) for el in s1_elements]
            s1_counts = s1_elements_clickable.count(True)
            for idx, el in enumerate(s1_elements):
                candidates_log["strategy_1"].append({
                    "index": idx,
                    "element": el,
                    "clickable": s1_elements_clickable[idx],
                    "html": el.get_attribute('outerHTML'),
                    "tag": el.tag_name,
                    "text": el.text[:100] if el.text else ""  # First 100 chars
                })
                if self.outcome_writer:
                    path_dom = f"s1_anchor_candidate_{idx}"
                    self.outcome_writer.save_dom(path_dom, el.get_attribute('outerHTML'))
                    candidates_log["strategy_1"][-1]["dom_path"] = path_dom
            if s1_counts == 1:
                vprint("The candidate chatbot launcher element found by the first strategy", quiet)              
                stats["s1_candidates"] = 1
                # candidate = s1_elements[s1_elements_clickable.index(True)]
            if s1_counts > 1:
                vprint("Multiple candidate chatbot launcher elements found by the first starategy. The solver has to be launched.", quiet)
                stats["s1_candidates"] = s1_counts
            if s1_counts == 0:
                vprint("The first starategy found elements but none are clickable.", quiet)

        else:
            vprint("The first starategy found no elements.", quiet)

        s2_elements = _find_elements_by_computed_style(driver, quiet)
        if len(s2_elements) > 0:
                s2_elements_clickable = [_is_element_clickable(el, driver, quiet) for el in s2_elements]
                s2_counts = s2_elements_clickable.count(True)
                for idx, el in enumerate(s2_elements):
                    candidates_log["strategy_2"].append({
                    "index": idx,
                    "element": el,
                    "clickable": s2_elements_clickable[idx],
                    "html": el.get_attribute('outerHTML'),
                    "tag": el.tag_name,
                    "text": el.text[:100] if el.text else ""
                })
                if s2_counts == 1:
                    vprint("The candidate chatbot launcher element found by the second starategy", quiet)              
                    stats["s2_candidates"] = 1
                    # candidate = s2_elements[s2_elements_clickable.index(True)]
                if s2_counts > 1:
                    vprint("Multiple candidate chatbot launcher elements found by the second starategy. The solver has to be launched.", quiet)
                    stats["s2_candidates"]= s2_counts
                if s2_counts == 0:
                    vprint("The second starategy found elements but none are clickable.", quiet)
        else:
                vprint("The second starategy found no elements.", quiet)
        
        evaluated_candidates = select_anchor_chatbot_widget(candidates_log, quiet)

        for strategy in ["strategy_1", "strategy_2"]:
            vprint(strategy, quiet)
            if strategy in evaluated_candidates and evaluated_candidates[strategy]:
                if self.outcome_writer:
                    # Create JSON-serializable version (remove WebElement objects)
                    json_safe = [
                        {k: v for k, v in cand.items() if k != 'element'}
                        for cand in evaluated_candidates[strategy]
                    ]
                    self.outcome_writer.save_json(f"evaluated_{strategy}_candidates", json_safe)
                for cand in evaluated_candidates[strategy]:
                    score = cand.get('score')
                    if score > 0:
                        vprint(f"Candidate Score: {score}", quiet)
                        vprint(f"Candidate HTML: {cand.get('html')}", quiet)

        if len(evaluated_candidates.get("strategy_1", [])) > 0:
            candidates = evaluated_candidates.get("strategy_1", [])
            candidate = max(candidates, key=lambda c: c.get('score', 0)).get('element')
        elif len(evaluated_candidates.get("strategy_2", [])) > 0:
            candidates = evaluated_candidates.get("strategy_2", [])
            candidate = max(candidates, key=lambda c: c.get('score', 0)).get('element')

        return candidate, json.dumps(stats), candidates_log


    def capture_chatbot_window(self, driver: WebDriver, launcher_element: WebElement, quiet: bool = True) -> dict:
        """
        Clicks the chatbot launcher element and captures the opened chatbot widget window.
        Handles iframes, shadow DOM, and regular DOM elements.
        
        Args:
            driver: The active Selenium WebDriver instance
            launcher_element: The element that opens the chatbot widget
            quiet: If True, suppress verbose output
            
        Returns:
            Dictionary containing the chatbot window details and HTML
        """
        result = {
        "success": False,
        "window_type": "shadow_dom",
        "detection_method": "iframe + shadow_dom",
        "html": None,
        "element_info": {},
        "error": None
        }

        try:
            vprint("Clicking chatbot launcher...", quiet)
            launcher_element.click()

            driver.implicitly_wait(2)

            vprint("Scanning main document for chatbot (shadow DOM)...", quiet)
            page_html = driver.page_source
            if self.outcome_writer:
                self.outcome_writer.save_dom("start_page_dom", page_html)

            # 1Main document
            shadow_results = driver.execute_script(SHADOW_SEARCH_JS)
            if shadow_results:
                return _finalize_shadow_result(result, shadow_results, quiet)

            # Same-origin iframes
            result, candidates = _find_iframes(driver, result, quiet)

            evaluated = [_evaluate_iframe_candidate(c) for c in candidates]

            evaluated.sort(key=lambda c: c["score"], reverse=True)
            target = evaluated[0]

            try:
                vprint(f"Best iframe candidate index: {target.get('index')} with score {target.get('score')}", quiet)
                target_element = target.get("element")
                try:
                    # TODO: Experiment with delay, the chatbot window may take time to load
                    time.sleep(15)
                    if self.outcome_writer:
                        self.outcome_writer.save_element_screenshot("chatbot_widget_window", target_element)
                except:
                    vprint("Failed to capture screenshot of the best iframe candidate element.", quiet)
                driver.switch_to.frame(target_element)
                try:
                    if self.outcome_writer:
                        self.outcome_writer.save_page_screenshot("start_page_with_chatbot_window", driver)
                    html = driver.page_source
                    if self.outcome_writer:
                        self.outcome_writer.save_dom("iframe_dom", html)
                    result["success"] = True
                    result['html'] = html
                except:
                    result["error"] = "Failed to capture HTML from the best iframe candidate."
                driver.switch_to.default_content()
            except:
                result["error"] = "Failed to switch to the best iframe candidate."

        except Exception as e:
            result["error"] = str(e)

        return result