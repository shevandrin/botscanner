__version__ = "0.1.0"


from .runner import run_scan
from .launcher import launch_page, check_ip
from ._detector_utils import _get_html_from_element
from ._launcher_utils import _handle_cookie_consent, _click_element_from_data, _check_robots_txt
from .utils import _is_element_clickable
from .evaluators.get_location_chatbot_anchor import get_location_chatbot_anchor
from .finders.framework_patterns import _find_windows_candidates_by_framework


print(f"botscanner package initialized (version {__version__})")