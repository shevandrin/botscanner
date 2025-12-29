from botscanner.utils import wait_for_dom_change
from selenium.webdriver.remote.webdriver import WebDriver
import time
from .finders.window.SimpleDOMChatbotWindowFinder import SimpleDOMChatbotWindowFinder
from .finders.window.ShadowDOMChatbotWindowFinder import ShadowDOMChatbotWindowFinder
from .finders.window.IframeChatbotWindowFinder import IframeChatbotWindowFinder
from .models.CandidateManager import CandidateManagerAnchor, CandidateManager
from .models.BaseCandidate import ChatbotAnchorCandidate
from .finders.anchor.SimpleChatbotAnchorFinder import SimpleDOMChatbotAnchorFinder
from .finders.anchor.ComputedStyleChatbotAnchorFinder import ComputedStyleChatbotAnchorFinder
from .finders.anchor.ShadowChatbotAnchor import ShadowChatbotAnchor
from .finders.anchor.ViewedStyleAnchorFinder import ViewedStyleChatbotAnchorFinder
from .finders.window.FrameworkChatbotWindowFinder import FrameworkChatbotWindowFinder
from ._detector_utils import click_chatbot_launcher


class ChatbotDetector:
    """Handles detection of chatbot widget on web pages."""
    def __init__(self, outcome_writer, logger):
        self.outcome_writer = outcome_writer
        self.logger = logger

    def discover_chatbot(self, driver: WebDriver, cand_manager: CandidateManagerAnchor) -> None:
        """
        Discover chatbot anchors that launch chatbot widgets.

        Returns:
            (candidate_element_or_None, stats_json)
        """
        self.logger.info("Discovering chatbot launcher elements (anchors)...")

        finders = [SimpleDOMChatbotAnchorFinder(),
                   ComputedStyleChatbotAnchorFinder(),
                   #ShadowChatbotAnchor(),
                   ViewedStyleChatbotAnchorFinder(),
                   ]

        for finder in finders:
            found = finder.find(driver, self.logger)
            cand_manager.add_candidates(found)

        cand_manager.process()
        selected_candidate = cand_manager.select_candidate()
        print(selected_candidate)
        
        return selected_candidate


    def capture_chatbot_window(self, driver: WebDriver, candidate: ChatbotAnchorCandidate, cand_manager: CandidateManager) -> dict:
        """
        Clicks the chatbot launcher element and captures the opened chatbot widget window.
        Handles iframes, shadow DOM, and regular DOM elements.
        
        Args:
            driver: The active Selenium WebDriver instance
            launcher_element: The element that opens the chatbot widget
            
        Returns:
            Dictionary containing the chatbot window details and HTML
        """
        self.logger.info("Capturing chatbot window is starting...")
        if not candidate:
            self.logger.warning("No chatbot launcher candidate provided. The botscanner is stopping.")
            return None
        self.logger.info(f"Clicking on chatbot launcher element: {candidate.to_dict()}")                 
        try: 
            click_chatbot_launcher(candidate.element, driver, self.logger)

            #driver.implicitly_wait(30)
            wait_for_dom_change(driver)

            finders = [SimpleDOMChatbotWindowFinder(),
                       FrameworkChatbotWindowFinder(),
                       #ShadowDOMChatbotWindowFinder(),
                       IframeChatbotWindowFinder(),
                       ]

            for finder in finders:
                found = finder.find(driver, self.logger)
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
            # it make sense for shadow and iframe?

        except Exception as e:
            self.logger.error(f"Error during chatbot window capture: {e}")
            selected_candidate = None            

        return selected_candidate