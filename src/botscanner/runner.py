from pathlib import Path
from typing import Optional
from botscanner.launcher import launch_page
from botscanner.detector import ChatbotDetector
from botscanner.outcomes.writer import OutcomeWriter#
from botscanner.logger import setup_logger


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

    outcome_manager = OutcomeWriter(url, output_dir)
    log_file = outcome_manager.scan_dir / f"log_{outcome_manager.domain}.log"
    logger = setup_logger(log_file)
    logger.info("Botscanner is running...")  

    driver = launch_page(url)



    detector = ChatbotDetector(outcome_manager)

    candidate = detector.discover_chatbot(driver, quiet=quiet)

    detector.capture_chatbot_window(driver, candidate, quiet=quiet)

    return driver