import logging


def setup_logger(name: str):
    """Set up and return a logger with a standard format."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
