import httpx
from config import GROQ_API_KEY, SYSTEM_PROMPT
from logger import log_error, log_info
from youtube_client import YouTubeClient

class GroqClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.system_prompt = SYSTEM_PROMPT
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.yt_client = YouTubeClient()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_response(self, user_query, lang="en", history=None):
        if not self.api_key:
            log_error("GROQ_API_KEY is missing", category="AI")
            return "Error: API Key missing."

        # 1. Check for relevant YouTube tutorial first
        video_suggestion = ""
        relevant_video = self.yt_client.find_relevant_video(user_query)
        if relevant_video:
            video_url = f"https://www.youtube.com/watch?v={relevant_video['id']}"
            from i18n import get_text
            video_suggestion = get_text("video_suggestion_prefix", lang, relevant_video['title'], video_url)
            log_info(f"Found relevant YouTube video for '{user_query}': {relevant_video['title']}", category="YouTube")

        # Hardcoded base prompt
        base_prompt = """
You are an expert in Microsoft Excel, Google Sheets, Data Analysis, and Forecasting.
Answer ONLY questions related to Excel, Google Sheets, or data analysis. 
If a question is unrelated, politely decline in the chosen language.
"""
        # Dynamic rules from i18n
        from i18n import get_text
        prompt_rules = get_text("system_prompt_rules", lang)
        
        system_prompt = base_prompt.strip() + "\n\n" + prompt_rules.strip()
        
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_query})

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.5,
            "max_tokens": 1024
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, headers=self.headers, json=payload, timeout=30.0)
                if response.status_code != 200:
                    log_error(f"Groq API Error {response.status_code}: {response.text}", category="AI")
                    return None
                data = response.json()
                response_text = data["choices"][0]["message"]["content"]
                return f"{video_suggestion}{response_text}"
        except Exception as e:
            log_error(f"Groq Request Exception: {e}", category="NETWORK")
            return None

    def get_intent_score(self, text, history=None):
        import re
        text_lower = text.lower()
        score = 0
        
        # 1. Keywords (Split into Core and Broad)
        core_keywords = ["excel", "vlookup", "hlookup", "pivot", "vba", "macro", "index", "match", "xlsx", "google sheets", "spreadsheet"]
        broad_keywords = ["sheet", "formula", "chart", "table", "cell", "row", "column", "data", "analysis", "forecast", "stats", "filter", "unique", "google", "office", "csv", "dashboard", "summarize", "aggregate", "group"]
        
        ar_core = ["اكسل", "إكسل", "معادلة", "صيغة", "دالة", "ماكرو", "سبريدشيت"]
        ar_broad = ["جدول", "جداول", "بيانات", "عمود", "صف", "خلية", "تنسيق", "تحليل", "توقع", "شرط", "مجموع", "بحث", "فلترة", "تصفية", "فرز", "تقرير", "تلخيص", "تجميع"]
        
        has_core = any(kw in text_lower for kw in core_keywords + ar_core)
        has_broad = any(kw in text_lower for kw in broad_keywords + ar_broad)
        
        if has_core:
            score += 35
        elif has_broad:
            score += 15
        
        # 2. Column references & Natural Language Columns
        col_pattern = r'[A-Z]{1,2}\d+|[A-Z]{1,2}:[A-Z]{1,2}'
        if re.search(col_pattern, text.upper()):
            score += 30
        elif any(kw in text_lower for kw in ["column", "columns", "عمود", "أعمدة"]):
            score += 15
            
        # 3. Goals (sum, average, compare, top, best, total, trend, growth, increase, decrease, etc.)
        goals = ["sum", "average", "avg", "compare", "forecast", "sort", "filter", "rank", "count", "min", "max", "unique", "match", "top", "best", "worst", "highest", "lowest", "total", "calculate", "each", "every", "trend", "performance", "growth", "increase", "decrease", "difference"]
        ar_goals = ["مجموع", "متوسط", "مقارنة", "توقع", "فرز", "تصفية", "ترتيب", "عد", "أصغر", "أكبر", "أفضل", "أعلى", "أسوأ", "أقل", "إجمالي", "احسب", "كل", "توجه", "أداء", "نمو", "زيادة", "نقص", "فرق"]
        if any(g in text_lower for g in goals + ar_goals):
            score += 25
                
        # 4. Length & Detail (Year/Month detection)
        words = text.split()
        if any(kw in text_lower for kw in ["year", "month", "days", "سنة", "شهر", "أيام"]):
            score += 10 # Bonus for time units which imply data series
            
        if len(words) >= 15:
            score += 30
        elif len(words) >= 8:
            score += 20
        elif len(words) >= 4:
            score += 10
            
        # 5. Question starters & Contextual phrases
        starters = ["how", "what", "provide", "give", "create", "show", "help", "can", "i have", "i want", "is there", "my data"]
        ar_starters = ["كيف", "ماذا", "أعطني", "اريد", "أريد", "ممكن", "ساعدني", "كيفية", "عندي", "لدي", "أريد", "هل هناك", "بياناتي"]
        if any(text_lower.startswith(s) or (s in text_lower[:15]) for s in starters + ar_starters):
            score += 15
                
        # 6. Context-based bonus
        if history and len(history) > 0:
            score += 20
            
        return min(score, 100)

    def is_excel_related(self, text):
        # Increased leniency: return True if it has ANY keyword OR if it's short (likely a question starter)
        keywords = [
            # English (Expanded with analytical terms)
            "excel", "sheet", "formula", "vlookup", "hlookup", "pivot", "chart", "table", "cell", "row", "column", 
            "data", "analysis", "forecast", "sum", "if", "office", "google", "sheets", "csv", "xlsx", "stats",
            "filter", "unique", "index", "match", "macro", "vba", "script", "dashboard", "report", "graph",
            "lookup", "text", "date", "count", "average", "min", "max", "sort", "validation", "sidebar",
            "best", "worst", "highest", "lowest", "compare", "trend", "year", "month", "performance", "growth",
            "increase", "decrease", "difference", "calculate", "summarize", "aggregate", "group",
            # Arabic (Expanded with analytical terms)
            "اكسل", "إكسل", "جدول", "جداول", "بيانات", "معادلة", "صيغة", "دالة", "عمود", "صف", "خلية", 
            "تنسيق", "تحليل", "توقع", "شرط", "مجموع", "متوسط", "بحث", "فلترة", "تصفية", "فرز", "تقرير",
            "دوال", "شيت", "سبريدشيت", "ماكرو", "رسم_بياني", "تحقق", "مخطط",
            "أفضل", "أسوأ", "أعلى", "أقل", "مقارنة", "توجه", "سنة", "شهر", "أداء", "نمو", "زيادة", "نقص",
            "فرق", "احسب", "تحليل", "تلخيص", "تجميع"
        ]
        text_lower = text.lower()
        
        # If any keyword matches
        if any(kw in text_lower for kw in keywords):
            return True
            
        # If the message is very short (e.g. "hi", "how to") it might be an intro
        if len(text.split()) <= 4:
            return "vague" # Return a specific state for vague/short messages
            
        return False
