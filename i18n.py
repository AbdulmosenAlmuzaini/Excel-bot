STRINGS = {
    "en": {
        "bot_intro": "Welcome to the Excel & Google Sheets Expert Bot! 🚀\nI can help you build advanced formulas, analyze complex data, create charts, and forecast trends. 📊\n\nأهلاً بك في بوت خبير الإكسل وجداول بيانات جوجل! 🚀\nأستطيع مساعدتك في بناء معادلات متقدمة، تحليل بيانات معقدة، إنشاء رسوم بيانية، وتوقع الاتجاهات المستقبلية. 📊",
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
        "system_prompt_rules": """
**Response Structure (VERY IMPORTANT):**
1. **Quick Solution**: Start with the fastest/most direct formula or answer immediately (e.g., "Quick Solution: =UNIQUE(A:A)").
2. **Details & Alternatives**: After the quick solution, provide brief explanations, alternatives, or conditional cases.
3. Use Markdown for formulas and code.
4. Answer ONLY in English. Do NOT use any other language.

**Handling Vague Requests:**
If the user's request is unclear, vague, or not obviously about Excel/Sheets:
- Do NOT refuse immediately if there's a chance it's related.
- Instead, ask 2-3 specific guided clarification questions (e.g., "Are you trying to analyze data or build a formula?", "What application are you using (Excel or Google Sheets)?", "Could you specify the columns involved?").
- Be helpful and proactive in guiding them.
"""
    },
    "ar": {
        "bot_intro": "أهلاً بك في بوت خبير الإكسل وجداول بيانات جوجل! 🚀\nأستطيع مساعدتك في بناء معادلات متقدمة، تحليل بيانات معقدة، إنشاء رسوم بيانية، وتوقع الاتجاهات المستقبلية. 📊",
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
        "system_prompt_rules": """
**هيكل الإجابة (هام جداً):**
1. **الحل السريع**: ابدأ بأسرع وأبشر صيغة أو إجابة مباشرة فوراً (مثال: "أسرع حل: =UNIQUE(A:A)").
2. **التفاصيل والبدائل**: بعد الحل السريع، قدم شروحات موجزة، بدائل، أو حالات مشروطة.
3. استخدم Markdown للصيغ والأكواد.
4. أجب باللغة العربية فقط. لا تستخدم أي لغة أخرى.

**التعامل مع الطلبات غير الواضحة:**
إذا كان طلب المستخدم غير واضح أو غامض أو لا يبدو متعلقاً بـ Excel/Sheets بشكل صريح:
- لا ترفض الطلب فوراً إذا كان هناك احتمال لتعلقه بالمجال.
- بدلاً من ذلك، اطرح 2-3 أسئلة توضيحية محددة (مثال: "هل تحاول تحليل بيانات أم إنشاء صيغة؟"، "ما هو التطبيق الذي تستخدمه (Excel أم Google Sheets)؟"، "هل يمكنك تحديد الأعمدة المعنية؟").
- كن متعاوناً ومبادراً في توجيه المستخدم.
"""
    }
}

def get_text(key, lang="en", *args):
    text = STRINGS.get(lang, STRINGS["en"]).get(key, key)
    if args:
        return text.format(*args)
    return text
