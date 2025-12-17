__version__ = "0.1.0"


from .runner import run_scan
from .launcher import launch_page, check_ip
from ._detector_utils import _find_elements_by_computed_style, _get_html_from_element, _is_element_interactive, _find_cursor_is_pointer, _find_elements_by_anchors, test_function, _find_iframes
from ._launcher_utils import _handle_cookie_consent, _click_element_from_data, _check_robots_txt
from .utils import _is_element_clickable
from .evaluators.get_location_chatbot_anchor import get_location_chatbot_anchor

print(f"botscanner package initialized (version {__version__})")