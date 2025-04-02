import logging

def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers (can happen if Cloud Run reloads the module)
    if not logger.handlers:
        handler = logging.StreamHandler()  # Cloud Run automatically captures stdout
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger()