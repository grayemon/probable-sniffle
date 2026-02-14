from utils.logger import setup_logger

logger = setup_logger()
logger.info("Hello World")
logger.warning("This is a warning")
logger.error("This is an error")
logger.critical("This is a critical error")
