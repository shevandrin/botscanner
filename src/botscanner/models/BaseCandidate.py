from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from botscanner.evaluators.eval_iframe_chatbot_window import _evaluate_iframe_candidate
from botscanner.evaluators.eval_anchor_chatbot_widget import _evaluate_anchor_candidate
from selenium.webdriver.remote.webelement import WebElement
from botscanner.utils import _is_element_clickable


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
    
@dataclass
class ChatbotAnchorCandidateJS(ChatbotAnchorCandidate):
    result_json_name: str = "anchor_js_candidates"
    dom_name: str = "anchor_js_candidate"

    def save_screenshot_element(self, logger, driver, writer):
        from PIL import Image
        SCROLL_TO_BBOX_JS = """
        window.scrollTo(
        arguments[0] - window.innerWidth / 2,
        arguments[1] - window.innerHeight / 2
        );
        """

        bbox = self.metadata["bounding"]
        driver.execute_script(
            SCROLL_TO_BBOX_JS,
            bbox["x"],
            bbox["y"]
        )

        full_path = "full_page.png"
        driver.save_screenshot(full_path)

        x = int(bbox["x"])
        y = int(bbox["y"])
        w = int(bbox["width"])
        h = int(bbox["height"])

        img = Image.open(full_path)

        element_img = img.crop((x, y, x + w, y + h))
        element_img.save("chatbot_launcher.png")

        return self