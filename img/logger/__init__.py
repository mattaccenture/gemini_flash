import logging
import sys

from logger.formatter import ColoredFormatter


def get_logger(module_name):
    """
    Create and configure a logger with specified format.

    Args:
    - module_name (str): The name of the module where the logger will be used.

    Returns:
    - logging.Logger: Configured logger object.
    """

    logger = logging.getLogger(module_name)

    handler = logging.StreamHandler(sys.stderr)
    log_format = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"

    date_format = "%Y-%m-%d %H:%M:%S"
    colored_formatter = ColoredFormatter(log_format, date_format)

    handler.setFormatter(colored_formatter)

    logger.addHandler(handler)

    LoggingLevel = logging.getLevelName("DEBUG")
    logger.setLevel(LoggingLevel)
    logger.propagate = False

    return logger

