import logging
from loguru import logger
from prometheus_client import Counter
import urllib3

error_counter = Counter("rt2_error_counter", "Number of errors", ["error_type"])


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 7
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        error_counter.labels(record.levelname).inc()
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())



def setup_logger(level: str = "info"):
    urllib3.disable_warnings()
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR
        }
    # setting the standard logger to use loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=levels[level.lower()])
