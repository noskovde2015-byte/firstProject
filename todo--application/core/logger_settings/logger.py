import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger():
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, "app.log")

    logger = logging.getLogger("fastapi-app")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when="midnight", interval=1, backupCount=2, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d - %(funcName)s()] - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()