from pathlib import Path
from typing import Optional
from botscanner.launcher import launch_page
from botscanner.detector import ChatbotDetector
from botscanner.outcomes.writer import OutcomeWriter


def run_scan(url: str, output_dir: Optional[Path] = None, quiet: bool = True):
    """
    Scan a URL for the presence of chatbot widget and write results to an output directory.
    This function launches a web browser, initializes a chatbot detector, discovers any chatbots on the page, and writes the findings to the specified output directory.
    Args:
        url (str): The URL of the web page to scan for chatbots.
        output_dir (Path | None, optional): The directory path where scan results will be written.
            Defaults to None.
        quiet (bool, optional): If True, suppresses output during the discovery process.
            Defaults to True.
    Returns:
         // TODO: specify return
    """

    driver = launch_page(url)

    outcome_manager = OutcomeWriter(url, output_dir)

    detector = ChatbotDetector(outcome_manager)

    candidate, stats, candidates_log = detector.discover_chatbot(driver, quiet=quiet)

    detector.capture_chatbot_window(driver, candidate, quiet=quiet)

    return None