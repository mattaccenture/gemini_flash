import logging
from functools import partial


def _color(color: str, msg: str) -> str:
    return f"{color}{msg}\x1b[0m"


class Colors(object):
    grey = partial(_color, "\x1b[38;5;240m")
    white = partial(_color, "\x1b[37m")
    yellow = partial(_color, "\x1b[33m")
    red = partial(_color, "\x1b[31m")
    magneta = partial(_color, "\x1b[35m")


class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt):
        logging.Formatter.__init__(self, fmt, datefmt)

        self.color = {
            logging.DEBUG: Colors.grey,
            logging.INFO: Colors.white,
            logging.WARNING: Colors.yellow,
            logging.ERROR: Colors.red,
            logging.CRITICAL: Colors.magneta,
        }

    def format(self, record) -> str:
        msg = super(ColoredFormatter, self).format(record)

        return self.color.get(record.levelno)(msg)

