import logging
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ExcelBot")

def log_error(error_msg, user_id=None):
    if user_id:
        logger.error(f"User {user_id}: {error_msg}")
    else:
        logger.error(error_msg)

def log_info(info_msg):
    logger.info(info_msg)
