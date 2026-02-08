from database import check_and_update_limits, get_user
from config import DAILY_MSG_LIMIT, DAILY_FILE_LIMIT, FAQ_CACHE
from i18n import get_text
from logger import log_info

def check_limits(user_id, is_file=False):
    msg_count, file_count = check_and_update_limits(user_id, is_file)
    
    if is_file:
        return file_count <= DAILY_FILE_LIMIT
    return msg_count <= DAILY_MSG_LIMIT

def get_faq_answer(query, lang):
    query_lower = query.lower()
    for key, answers in FAQ_CACHE.items():
        if key in query_lower:
            return answers.get(lang, answers["en"])
    return None
