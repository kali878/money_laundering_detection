import logging
from pathlib import Path


_logger = None




def get_logger(name: str = "aml"): # singleton logger
    global _logger
    if _logger is not None:
        return _logger


    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    Formatter = logging.Formatter
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(ch)
    _logger = logger
    return logger




def ensure_dirs(*paths: Path):
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)