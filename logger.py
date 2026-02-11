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

def log_error(error_msg, user_id=None, category="INTERNAL"):
    if user_id:
        logger.error(f"[{category}] User {user_id}: {error_msg}")
    else:
        logger.error(f"[{category}] {error_msg}")
    
    # Log to DB as well
    try:
        from database import log_error_to_db
        log_error_to_db(user_id, category, error_msg)
    except Exception as e:
        logger.error(f"Failed to log error to DB: {e}")

def log_info(info_msg):
    logger.info(info_msg)
