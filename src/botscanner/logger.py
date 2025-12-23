import logging
from pathlib import Path

def setup_logger(
    log_file: str,
    level=logging.DEBUG,
):
    logger = logging.getLogger("botscanner")
    logger.setLevel(level)

    logger.handlers.clear()

    # File handler (always on)
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
