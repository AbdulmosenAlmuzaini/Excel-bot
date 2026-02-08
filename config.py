import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

DAILY_MSG_LIMIT = int(os.getenv("DAILY_MSG_LIMIT", 50))
DAILY_FILE_LIMIT = int(os.getenv("DAILY_FILE_LIMIT", 1))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 5))

# FAQ Cache for common Excel/Sheets questions
FAQ_CACHE = {
    "vlookup": {
        "en": "VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])\nExample: =VLOOKUP(\"Apple\", A2:B10, 2, FALSE)",
        "ar": "VLOOKUP(قيمة_البحث, مصفوفة_الجدول, رقم_فهرس_العمود, [بحث_المدى])\nمثال: =VLOOKUP(\"Apple\", A2:B10, 2, FALSE)"
    },
    "sum": {
        "en": "SUM(number1, [number2], ...)\nExample: =SUM(A1:A10)",
        "ar": "SUM(الرقم1, [الرقم2], ...)\nمثال: =SUM(A1:A10)"
    },
    "if": {
        "en": "IF(logical_test, value_if_true, value_if_false)\nExample: =IF(A1>10, \"Good\", \"Bad\")",
        "ar": "IF(اختبار_منطقي, القيمة_إذا_تحقق, القيمة_إذا_لم_يتحقق)\nمثال: =IF(A1>10, \"ممتاز\", \"ضعيف\")"
    }
}

# Groq System Prompt
SYSTEM_PROMPT = """
You are an expert in Microsoft Excel, Google Sheets, Data Analysis, and Forecasting.
Answer ONLY questions related to Excel, Google Sheets, or data analysis. 
If a question is unrelated, politely decline in the same language as the user.

**Response Structure (VERY IMPORTANT):**
1. **Quick Solution**: Start with the fastest/most direct formula or answer immediately (e.g., "أسرع حل: =UNIQUE(A:A)").
2. **Details & Alternatives**: After the quick solution, provide brief explanations, alternatives, or conditional cases (e.g., "وإذا احتجت فلترة حسب شرط: ...").
3. Use Markdown for formulas and code.
4. Keep the initial response extremely concise for users who want a quick fix.
"""
