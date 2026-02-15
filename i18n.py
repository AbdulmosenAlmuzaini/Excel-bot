STRINGS = {
    "en": {
        "bot_intro": "Welcome to the Excel & Google Sheets Expert Bot! 🚀\nI can help you build advanced formulas, analyze complex data, create charts, and forecast trends. 📊\n\nأهلاً بك في بوت خبير الإكسل وجداول بيانات جوجل! 🚀\nأستطيع مساعدتك في بناء معادلات متقدمة، تحليل بيانات معقدة، إنشاء رسوم بيانية، وتوقع الاتجاهات المستقبلية. 📊\n\n⚠️ *Messages may be logged for improvement purposes.*",
        "welcome": "Please select your preferred language / يرجى اختيار لغتك المفضلة:",
        "lang_selected": "Language set to English.",
        "help": "I can help you with Excel formulas, Google Sheets functions, and data analysis. Just ask your question or upload an Excel file.",
        "examples": "Try asking:\n- How to use INDEX/MATCH?\n- Give me a formula to calculate age from birthday.\n- How to freeze rows in Google Sheets?",
        "limit_reached": "You have reached your daily limit. Please try again tomorrow.",
        "file_limit_reached": "You can only upload one file per day.",
        "invalid_topic": "I'm sorry, I can only answer questions related to Excel and Google Sheets.",
        "processing_file": "Analyzing your file... please wait.",
        "file_too_large": "The file is too large. Maximum size is {}MB.",
        "admin_stats": "User Count: {}\nTotal Requests: {}\nErrors Logged: {}",
        "error_generic": "An error occurred. Please try again later.",
        "select_lang": "Select Language",
        "clarification_intro": "I want to help you accurately 😊\nCould you please clarify what you want to do?",
        "clarification_options": "Please choose one:",
        "opt_analysis": "📊 Data Analysis",
        "opt_formula": "🧮 Formula",
        "opt_chart": "📈 Chart",
        "opt_forecast": "🔮 Forecast",
        "opt_cleaning": "🗂 Data Cleaning",
        "ask_column": "Which column contains your data? (e.g., A, B, C...)",
        "ask_analysis_goal": "What do you want to analyze? (Average, ranking, comparison...)",
        "ask_months": "How many past months of data do you have?",
        "ask_chart_cols": "Which columns should be used for the chart?",
        "escalation_msg": "To help you better, please upload your Excel file or share a screenshot.",
        "feedback_cmd_prompt": "We value your feedback! Please rate your experience so far:",
        "feedback_thanks": "Thank you for your feedback! It helps us improve for everyone. 😊",
        "feedback_rate_good": "👍 Good",
        "feedback_rate_bad": "👎 Bad",
        "feedback_rate_suggestion": "💡 Suggestion",
        "feedback_ask_suggestion": "Please type your suggestion or comment briefly:",
        "feedback_interaction_prompt": "You've been using the bot for a while! Was my last answer helpful?",
        "system_prompt_rules": """
**Response Style (VERY IMPORTANT):**
1. **Simple & Direct**: Provide ONE simple, clear way to do it first. Do NOT use superlatives like "fastest", "best", or "most direct".
2. **Progressive Detail**: After the simple answer, ask the user if they would like to see an alternative method or more details.
   - Example: "Here is a simple way to do this: ... Would you like another approach?"
3. **Format**: Use Markdown for formulas and code blocks.
4. **Language**: Answer ONLY in English. Do NOT use any other language.

**Handling Vague Requests:**
If the request is unclear:
- Do NOT refuse immediately.
- Ask 2-3 specific guided questions to clarify (e.g., "What application are you using?", "Which columns are involved?").
""",
        "logging_disclaimer": "⚠️ *Messages may be logged for improvement purposes.*",
        "quick_start_prompt": "Try one of these examples 💡:",
        "ex_avg": "Calculate Average",
        "ex_dup": "Remove Duplicates",
        "ex_sales": "Analyze Sales",
        "ex_forecast": "Forecast Trends"
    },
    "ar": {
        "bot_intro": "أهلاً بك في بوت خبير الإكسل وجداول بيانات جوجل! 🚀\nأستطيع مساعدتك في بناء معادلات متقدمة، تحليل بيانات معقدة، إنشاء رسوم بيانية، وتوقع الاتجاهات المستقبلية. 📊\n\n⚠️ *قد يتم تسجيل الرسائل لأغراض تحسين الخدمة.*",
        "welcome": "يرجى اختيار لغتك المفضلة / Please select your preferred language:",
        "lang_selected": "تم ضبط اللغة إلى العربية.",
        "help": "يمكنني مساعدتك في صيغ Excel، ووظائف Google Sheets، وتحليل البيانات. فقط اطرح سؤالك أو ارفع ملف Excel.",
        "examples": "جرب سؤال:\n- كيف أستخدم INDEX/MATCH؟\n- أعطني صيغة لحساب العمر من تاريخ الميلاد.\n- كيف أقوم بتثبيت الصفوف في Google Sheets؟",
        "limit_reached": "لقد وصلت إلى الحد اليومي المسموح به. يرجى المحاولة مرة أخرى غداً.",
        "file_limit_reached": "يمكنك رفع ملف واحد فقط في اليوم.",
        "invalid_topic": "عذراً، أستطيع الإجابة فقط على الأسئلة المتعلقة بـ Excel و Google Sheets.",
        "processing_file": "جاري تحليل الملف... يرجى الانتظار.",
        "file_too_large": "حجم الملف كبير جداً. الحد الأقصى هو {} ميجابايت.",
        "admin_stats": "عدد المستخدمين: {}\nإجمالي الطلبات: {}\nالأخطاء المسجلة: {}",
        "error_generic": "حدث خطأ ما. يرجى المحاولة لاحقاً.",
        "select_lang": "اختر اللغة",
        "clarification_intro": "أريد مساعدتك بدقة 😊\nهل يمكنك توضيح ما تريد القيام به؟",
        "clarification_options": "يرجى اختيار أحد الخيارات:",
        "opt_analysis": "📊 تحليل بيانات",
        "opt_formula": "🧮 معادلة/صيغة",
        "opt_chart": "📈 رسم بياني",
        "opt_forecast": "🔮 توقعات",
        "opt_cleaning": "🗂 تنظيف بيانات",
        "ask_column": "ما هو العمود الذي يحتوي على بياناتك؟ (مثال: A, B, C...)",
        "ask_analysis_goal": "ماذا تريد أن تحلل؟ (متوسط، ترتيب، مقارنة...)",
        "ask_months": "كم عدد الأشهر السابقة المتوفرة لديك؟",
        "ask_chart_cols": "ما هي الأعمدة التي تريد استخدامها للرسم البياني؟",
        "escalation_msg": "لمساعدتك بشكل أفضل، يرجى رفع ملف Excel أو مشاركة لقطة شاشة.",
        "feedback_cmd_prompt": "نحن نقدر رأيك! يرجى تقييم تجربتك حتى الآن:",
        "feedback_thanks": "شكراً جزيلاً لتقييمك! هذا يساعدنا على تحسين الخدمة للجميع. 😊",
        "feedback_rate_good": "👍 ممتاز",
        "feedback_rate_bad": "👎 سيء",
        "feedback_rate_suggestion": "💡 اقتراح",
        "feedback_ask_suggestion": "يرجى كتابة اقتراحك أو ملاحظتك باختصار:",
        "feedback_interaction_prompt": "لقد استخدمت البوت لفترة! هل كانت إجابتي الأخيرة مفيدة لك؟",
        "system_prompt_rules": """
**أسلوب الإجابة (هام جداً):**
1. **بسيط ومباشر**: قدم طريقة واحدة بسيطة وواضحة للقيام بذلك أولاً. لا تستخدم صيغ التفضيل مثل "أسرع حل" أو "أفضل طريقة".
2. **التدرج في التفاصيل**: بعد الإجابة البسيطة، اسأل المستخدم إذا كان يرغب في رؤية طريقة بديلة أو مزيد من التفاصيل.
   - مثال: "إليك طريقة بسيطة للقيام بذلك: ... هل تود رؤية طريقة أخرى؟"
3. **التنسيق**: استخدم Markdown للصيغ وأكواد البرمجة.
4. **اللغة**: أجب باللغة العربية فقط. لا تستخدم أي لغة أخرى.

**التعامل مع الطلبات غير الواضحة:**
إذا كان الطلب غير واضح:
- لا ترفض الطلب فوراً.
- اطرح 2-3 أسئلة توضيحية محددة (مثال: "ما هو التطبيق الذي تستخدمه؟"، "ما هي الأعمدة المعنية؟").
""",
        "logging_disclaimer": "⚠️ *قد يتم تسجيل الرسائل لأغراض تحسين الخدمة.*",
        "quick_start_prompt": "جرب أحد هذه الأمثلة 💡:",
        "ex_avg": "حساب المتوسط",
        "ex_dup": "حذف التكرارات",
        "ex_sales": "تحليل المبيعات",
        "ex_forecast": "توقعات الاتجاهات"
    }
}

def get_text(key, lang="en", *args):
    text = STRINGS.get(lang, STRINGS["en"]).get(key, key)
    if args:
        return text.format(*args)
    return text
