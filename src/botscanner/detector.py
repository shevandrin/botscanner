from selenium.webdriver.remote.webdriver import WebDriver
from .utils import vprint
import time
from .finders.SimpleDOMChatbotWindowFinder import SimpleDOMChatbotWindowFinder
from .finders.ShadowDOMChatbotWindowFinder import ShadowDOMChatbotWindowFinder
from .finders.IframeChatbotWindowFinder import IframeChatbotWindowFinder
from .models.CandidateManager import CandidateManagerAnchor, CandidateManager
from .models.BaseCandidate import ChatbotAnchorCandidate
from .finders.SimpleChatbotAnchorFinder import SimpleDOMChatbotAnchorFinder
from .finders.ComputedStyleChatbotAnchorFinder import ComputedStyleChatbotAnchorFinder


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

        finders = [SimpleDOMChatbotAnchorFinder(),
                   ComputedStyleChatbotAnchorFinder()]

        cand_manager = CandidateManagerAnchor(driver, self.outcome_writer, quiet)

        for finder in finders:
            found = finder.find(driver, quiet = True)
            cand_manager.add_candidates(found)

        cand_manager.process()
        selected_candidate = cand_manager.select_candidate()
        
        return selected_candidate


    def capture_chatbot_window(self, driver: WebDriver, candidate: ChatbotAnchorCandidate, quiet: bool = True) -> dict:
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
            candidate.element.click()

            driver.implicitly_wait(30)

            finders = [SimpleDOMChatbotWindowFinder(),
                       ShadowDOMChatbotWindowFinder(),
                       IframeChatbotWindowFinder()]
            cands = []
            cand_manager = CandidateManager(driver, self.outcome_writer, quiet)

            for finder in finders:
                found = finder.find(driver, quiet = True)
                cands.extend(found)
                cand_manager.add_candidates(found)

            cand_manager.process()
            selected_candidate = cand_manager.select_candidate()

            page_html = driver.page_source
            if self.outcome_writer:
                self.outcome_writer.save_dom("start_page_dom", page_html)

            time.sleep(2)
            if self.outcome_writer:
                self.outcome_writer.save_page_screenshot("start_page_with_chatbot_window", driver)

            # TODO: go to the best candidate take its html and picture
            # it make sence for shadow and iframe?

        except Exception as e:
            vprint(f"Error during chatbot window capture: {e}", quiet)
            selected_candidate = None            

        return selected_candidate