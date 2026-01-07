from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from botscanner.evaluators.eval_iframe_chatbot_window import _evaluate_iframe_candidate
from botscanner.evaluators.eval_anchor_chatbot_widget import _evaluate_anchor_candidate
from selenium.webdriver.remote.webelement import WebElement
from botscanner.utils import _is_element_clickable
from selenium.webdriver.common.action_chains import ActionChains


@dataclass
class BaseCandidate:
    index: int
    source: str
    context: str
    element: Any
    tag: str
    html: str
    clickable: Optional[bool] = None
    strategy: Optional[str] = None
    dom_name: str = "base_candidate"
    dom_snapshot: Optional[str] = None

    score: int = 0
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    
    def make_dom_snapshot(self, driver) -> None:
        """
        Capture the DOM snapshot of the candidate's element.
        """
        try:
            if isinstance(self.element, WebElement):
                if self.tag == "iframe":
                    driver.switch_to.frame(self.element)
                    self.dom_snapshot = driver.page_source
                    driver.switch_to.parent_frame()
                    return
                self.dom_snapshot = self.element.get_attribute("outerHTML")
            else:
                self.dom_snapshot = str(self.element)
        except Exception as e:
            self.dom_snapshot = None
        

    def evaluate(self) -> None:
        """
        Evaluate the candidate and update its score and evidence.
        Override in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "source": self.source,
            "context": self.context,
            "tag": self.tag,
            "html": self.html,
            "score": self.score,
            "evidence": self.evidence,
            "clickable": self.clickable,
            "strategy": self.strategy,
            **self.metadata,
        }
    
    def save_screenshot_element(self, logger, driver, writer) -> None:
        """
        Save a screenshot of the candidate's web element.
        """
        if isinstance(self.element, WebElement):
            try:
                file_name = f"screenshot_{self.dom_name}_{self.index}"
                writer.save_element_screenshot(file_name, self.element, logger, driver)
                logger.info(f"Screenshot for element {self.index} saved to {file_name}")
            except Exception as e:
                logger.error(f"Failed to save screenshot for element {self.index}: {e}")

            
    def save_dom(self, logger, driver, writer) -> None:
        """
        Save the DOM content of the candidate.
        """
        try:
            file_name = f"dom_{self.dom_name}_{self.index}"
            writer.save_dom(file_name, self.html)
            logger.info(f"Dom content for element {self.index} saved to {file_name}")
            
            if self.tag == "iframe" and isinstance(self.element, WebElement):
                driver = self.element._parent
                driver.switch_to.frame(self.element)
                iframe_html = driver.page_source
                iframe_file_name = f"dom_{self.dom_name}_{self.index}_iframe"
                writer.save_dom(iframe_file_name, iframe_html)
                logger.info(f"Iframe DOM content for element {self.index} saved to {iframe_file_name}")
                driver.switch_to.parent_frame()
        except Exception as e:
            logger.error(f"Failed to save DOM content for element {self.index}: {e}")

@dataclass
class ChatbotWindowCandidate(BaseCandidate):
    result_json_name: str = "chatbot_window_candidates"
    dom_name: str = "chatbot_window_candidate"
    bounding_box: Optional[Dict[str, Any]] = None
    def evaluate(self):
        result = _evaluate_iframe_candidate(self.to_dict())
        self.score = result["score"]
        self.evidence = result["evidence"]
        return self
    
@dataclass
class ChatbotWindowCandidateJS(ChatbotWindowCandidate):
    result_json_name: str = "chatbot_window_js_candidates"
    dom_name: str = "chatbot_window_shadow_candidate"


@dataclass
class ChatbotAnchorCandidate(BaseCandidate):
    clickable: Optional[bool] = None
    result_json_name: str = "anchor_candidates"
    dom_name: str = "anchor_candidate"
    location: Optional[str] = None
    
    def __post_init__(self):
        if self.clickable is None and isinstance(self.element, WebElement):
            try:
                self.clickable = _is_element_clickable(self.element)
            except Exception:
                self.clickable = False

    def evaluate(self, logger=None):
        try:
            result = _evaluate_anchor_candidate(self.to_dict())
            self.score = result["score"]
            self.evidence = result["evidence"]
            if logger:
                logger.info(f"Evaluated anchor candidate {self.index} with score {self.score}")
            return self
        except Exception as e:
            if logger:
                logger.error(f"Error evaluating anchor candidate {self.index}: {e}")
            raise e
        
    def get_location_value(self, driver) -> str:
        from botscanner.evaluators.get_location_chatbot_anchor import get_location_chatbot_anchor
        if isinstance(self.element, WebElement):
            self.location = get_location_chatbot_anchor(driver, self.element)
        return self.location
    
    def click_action(self, driver, logger) -> None:
        from botscanner._detector_utils import click_chatbot_launcher
        if isinstance(self.element, WebElement):
            try:
                click_chatbot_launcher(self.element, driver, logger)
                logger.info(f"Clicked on anchor candidate {self.index}")
            except Exception as e:
                logger.error(f"Error clicking on anchor candidate {self.index}: {e}")
                raise e
    
@dataclass
class ChatbotAnchorCandidateJS(ChatbotAnchorCandidate):
    result_json_name: str = "anchor_js_candidates"
    dom_name: str = "anchor_js_candidate"

    def save_screenshot_element(self, logger, driver, writer):
        name = f"screenshot_{self.dom_name}_{self.index}"

        try:
            writer.save_screenshot_js_element(
                name=name, 
                driver=driver,
                bounding=self.metadata.get("bounding"),
                logger=logger)
            logger.info(f"Screenshot for JS element {self.index} saved to {name}")
        except Exception as e:
            logger.error(f"Failed to save screenshot for JS element {self.index}: {e}")

        return self
    

    def get_location_value(self, driver) -> str:
        bounding = self.metadata.get("bounding", {})
        if not bounding:
            return "unknown"
        viewport_width = driver.execute_script("return window.innerWidth")
        viewport_height = driver.execute_script("return window.innerHeight")

        cx = bounding["x"] + bounding["width"] / 2
        cy = bounding["y"] + bounding["height"] / 2

        horizontal = "left" if cx < viewport_width / 2 else "right"
        vertical = "top" if cy < viewport_height / 2 else "bottom"

        return f"{vertical}-{horizontal}"
    

    def click_action(self, driver, logger):
        """
        Clicks a chatbot launcher candidate using identifiers or bounding box.
        Returns True on success, False otherwise.
        """

        bounding = self.metadata.get("bounding", {})
        if not bounding:
            return False

        x = bounding["x"] + bounding["width"] / 2
        y = bounding["y"] + bounding["height"] / 2
        print( f"Clicking at coordinates: ({x}, {y})" )

        try:
            result = driver.execute_script(
                """
                const host = document.elementFromPoint(arguments[0], arguments[1]);
                if (!host || !host.shadowRoot) {
                    return { ok:false, reason:"no shadowRoot" };
                }

                // Find clickable inside shadow root
                const btn = host.shadowRoot.querySelector(
                    'button,[role="button"],div[role="button"]'
                );

                if (!btn) {
                    return { ok:false, reason:"no button in shadowRoot" };
                }

                btn.click();
                return { ok:true, clicked: btn.tagName };
                """,
                x, y
            )
            print(result)
            return True
        except Exception as e:
            if logger:
                logger.error(f"Shadow click failed: {e}")
            return False