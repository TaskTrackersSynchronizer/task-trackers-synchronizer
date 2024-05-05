import logging
import sys

from app.core.config import config

handler = logging.StreamHandler(sys.stdout)
gunicorn_logger = logging.getLogger("gunicorn.error")
logger = logging.getLogger(config.service_name)
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)
logger.propagate = False
logger.addHandler(handler)

# Make all log formats consistent
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
    "%d/%m/%Y %I:%M:%S %p",
)

for handler in logger.handlers:
    handler.setFormatter(formatter)
