import logging
import sys
from rich.logging import RichHandler


def get_logger():

    logger = logging.getLogger("api-gk-app")
    log_format = "%(asctime)s - %(levelname)s - [%(pathname)s:%(lineno)d]\n%(message)s"

    logging.basicConfig(
        format=log_format,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    if not logger.level:
        log_level_value = getattr(logging, 'DEBUG', logging.INFO)
        logger.setLevel(log_level_value)
    
    return logger

logger = get_logger()