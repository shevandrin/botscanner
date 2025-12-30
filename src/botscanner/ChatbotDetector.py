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
from .evaluators.get_location_chatbot_window import extract_bounding_box
from.evaluators.get_location_chatbot_anchor import get_location_chatbot_anchor


class ChatbotDetector:
    """Handles detection of chatbot widget on web pages."""
    def __init__(self, outcome_writer, logger):
        self.outcome_writer = outcome_writer
        self.logger = logger
        self.selected_anchor = None
        self.selected_window = None

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
        self.selected_anchor = cand_manager.select_candidate()
        self.selected_anchor.location = get_location_chatbot_anchor(driver, self.selected_anchor.element)
        
        return self.selected_anchor


    def capture_chatbot_window(self, driver: WebDriver, cand_manager: CandidateManager) -> dict:
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
        if not self.selected_anchor:
            self.logger.warning("No chatbot launcher candidate provided. The botscanner is stopping.")
            return None
        self.logger.info(f"Clicking on chatbot launcher element: {self.selected_anchor.to_dict()}")                 
        try: 
            click_chatbot_launcher(self.selected_anchor.element, driver, self.logger)

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
            self.selected_window = cand_manager.select_candidate()
            self.selected_window.bounding_box = extract_bounding_box(driver, self.selected_window.element)

            page_html = driver.page_source
            if self.outcome_writer:
                self.outcome_writer.save_dom("start_page_dom", page_html)

            time.sleep(2)
            if self.outcome_writer:
                self.outcome_writer.save_page_screenshot("start_page_with_chatbot_window", driver)


        except Exception as e:
            self.logger.error(f"Error during chatbot window capture: {e}")
            self.selected_window = None          

        return self.selected_window