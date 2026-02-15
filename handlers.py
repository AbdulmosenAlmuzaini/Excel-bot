import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user, update_user_lang, register_user, log_interaction, get_stats, get_chat_history, clear_chat_history, get_user_state, update_user_state, log_feedback, log_chat, get_admin_logs, export_logs_to_excel
from i18n import get_text
from config import ADMIN_ID, MAX_FILE_SIZE_MB
from middleware import check_limits, get_faq_answer
from groq_client import GroqClient
from analysis import analyze_excel, is_valid_file
from logger import log_error, log_info

groq = GroqClient()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    register_user(user_id)
    
    keyboard = [
        [
            InlineKeyboardButton("English 🇺🇸", callback_data='lang_en'),
            InlineKeyboardButton("العربية 🇸🇦", callback_data='lang_ar')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # We don't know the language yet, so show the bilingual intro first
    welcome_text = get_text("bot_intro", "en") + "\n\n" + get_text("welcome", "en")
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang = query.data.split('_')[1]
    user_id = query.from_user.id
    update_user_lang(user_id, lang)
    clear_chat_history(user_id) # Clear history to avoid language leakage
    
    await query.edit_message_text(get_text("lang_selected", lang))
    await show_quick_start(query.message, context, lang)
    await query.message.reply_text(get_text("help", lang))

async def show_quick_start(message, context, lang):
    keyboard = [
        [InlineKeyboardButton(get_text("ex_avg", lang), callback_data='ex_avg')],
        [InlineKeyboardButton(get_text("ex_dup", lang), callback_data='ex_dup')],
        [InlineKeyboardButton(get_text("ex_sales", lang), callback_data='ex_sales')],
        [InlineKeyboardButton(get_text("ex_forecast", lang), callback_data='ex_forecast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(get_text("quick_start_prompt", lang), reply_markup=reply_markup)

async def example_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = get_user(user_id)
    lang = user[1] if user else "en"
    
    example_key = query.data # e.g., 'ex_avg'
    example_text = get_text(example_key, lang)
    
    # 1. Inform the user what's happening
    await query.message.reply_text(f"🚀 *{example_text}*", parse_mode="Markdown")
    
    # 2. Call Groq
    await query.message.reply_chat_action("typing")
    response = await groq.get_response(example_text, lang=lang)
    
    if response:
        await update_message_with_markdown_fallback(query, response, lang)
        log_interaction(user_id, f"EXAMPLE: {example_text}", response, "text")
        log_chat(user_id, f"EXAMPLE: {example_text}", response)
    else:
        await query.message.reply_text(get_text("error_generic", lang))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    lang = user[1] if user else "en"
    await update.message.reply_text(get_text("help", lang))

async def examples_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    lang = user[1] if user else "en"
    await update.message.reply_text(get_text("examples", lang))

async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [
            InlineKeyboardButton("English 🇺🇸", callback_data='lang_en'),
            InlineKeyboardButton("العربية 🇸🇦", callback_data='lang_ar')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = get_user(user_id)
    lang = user[1] if user else "en"
    await update.message.reply_text(get_text("select_lang", lang), reply_markup=reply_markup)

async def clarification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = get_user(user_id)
    lang = user[1] if user else "en"
    
    data = query.data.split('_')
    action = data[1] # analysis, formula, chart, forecast, cleaning
    
    state, user_context = get_user_state(user_id)
    user_context["goal"] = action
    
    # Transition based on choice
    if action == "formula":
        await query.edit_message_text(get_text("ask_column", lang))
        user_context["missing"] = ["column"]
    elif action == "analysis":
        await query.edit_message_text(get_text("ask_analysis_goal", lang))
        user_context["missing"] = ["goal_detail"]
    elif action == "forecast":
        await query.edit_message_text(get_text("ask_months", lang))
        user_context["missing"] = ["months"]
    elif action == "chart":
        await query.edit_message_text(get_text("ask_chart_cols", lang))
        user_context["missing"] = ["chart_cols"]
    else: # cleaning
        await query.edit_message_text(get_text("ask_column", lang))
        user_context["missing"] = ["column"]
        
    update_user_state(user_id, "CLARIFYING", user_context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user[1] if user else "en"
    query_text = update.message.text

    # 1. Check Limits
    is_allowed, msg_count = check_limits(user_id)
    if not is_allowed:
        await update.message.reply_text(get_text("limit_reached", lang))
        return

    # Proactive feedback: Every 10 messages
    if msg_count > 0 and msg_count % 10 == 0:
        keyboard = [
            [
                InlineKeyboardButton(get_text("feedback_rate_good", lang), callback_data='rate_good'),
                InlineKeyboardButton(get_text("feedback_rate_bad", lang), callback_data='rate_bad')
            ],
            [InlineKeyboardButton(get_text("feedback_rate_suggestion", lang), callback_data='rate_suggest')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_text("feedback_interaction_prompt", lang), reply_markup=reply_markup)

    # 2. State & Context
    state, user_context = get_user_state(user_id)

    # Process Wait Feedback state
    if state == "WAIT_FEEDBACK":
        log_feedback(user_id, "SUGGESTION", query_text)
        update_user_state(user_id, "NORMAL", {})
        await update.message.reply_text(get_text("feedback_thanks", lang))
        return

    if state == "CLARIFYING":
        # Handle clarification follow-up
        goal = user_context.get("goal")
        missing = user_context.get("missing", [])
        
        if missing:
            # Add gathered info to context
            key = missing.pop(0)
            user_context[key] = query_text
            user_context["missing"] = missing
            
        if not missing:
            # Everything gathered, resume
            update_user_state(user_id, "NORMAL", {})
            # Construct a rich prompt for AI
            prompt = f"User Goal: {goal}. Context: {user_context}. Original Query: {user_context.get('original_query','')}. User's latest info: {query_text}. Give a complete solution."
            await update.message.reply_chat_action("typing")
            response = await groq.get_response(prompt, lang=lang)
            if response:
                await update_message_with_markdown_fallback(update, response, lang)
                log_interaction(user_id, query_text, response, "text")
                log_chat(user_id, prompt, response)
            return
        else:
            # Still missing something (in a real complex case we'd ask the next question)
            update_user_state(user_id, "CLARIFYING", user_context)
            return

    # 3. Get Chat History (for NORMAL mode)
    history = get_chat_history(user_id)

    # 4. Intent Scoring
    score = groq.get_intent_score(query_text, history=history)
    
    # 5. Topic Filtering (Flexible & Context-aware)
    topic_status = groq.is_excel_related(query_text)
    is_related = (topic_status is True) or (history) or (topic_status == "vague")
    
    # 6. Rejection (Last step)
    # Only reject if certainly unrelated and score is very low
    if not is_related and score < 30:
        await update.message.reply_text(get_text("invalid_topic", lang))
        return

    # 7. Clarification (Preferred over rejection for borderline cases)
    # If score is low OR topic is vague AND not already in a thread
    if (score < 60 or topic_status == "vague") and not history:
        attempts = user_context.get("attempts", 0) + 1
        if attempts >= 2:
            await update.message.reply_text(get_text("escalation_msg", lang))
            update_user_state(user_id, "NORMAL", {"attempts": 0})
            return
            
        user_context = {"attempts": attempts, "original_query": query_text}
        update_user_state(user_id, "NORMAL", user_context) # Keep attempts count
        
        keyboard = [
            [InlineKeyboardButton(get_text("opt_analysis", lang), callback_data='clarify_analysis')],
            [InlineKeyboardButton(get_text("opt_formula", lang), callback_data='clarify_formula')],
            [InlineKeyboardButton(get_text("opt_chart", lang), callback_data='clarify_chart')],
            [InlineKeyboardButton(get_text("opt_forecast", lang), callback_data='clarify_forecast')],
            [InlineKeyboardButton(get_text("opt_cleaning", lang), callback_data='clarify_cleaning')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_text("clarification_intro", lang), reply_markup=reply_markup)
        return

    # 6. Check FAQ Cache
    faq_answer = get_faq_answer(query_text, lang)
    if faq_answer:
        await update.message.reply_text(faq_answer)
        log_interaction(user_id, query_text, "FAQ_CACHE", "faq")
        return

    # 7. Call Groq with History
    await update.message.reply_chat_action("typing")
    response = await groq.get_response(query_text, lang=lang, history=history)
    
    if response:
        await update_message_with_markdown_fallback(update, response, lang)
        log_interaction(user_id, query_text, response, "text")
        log_chat(user_id, query_text, response)
    else:
        await update.message.reply_text(get_text("error_generic", lang))

async def update_message_with_markdown_fallback(update, response, lang):
    try:
        await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        log_error(f"Markdown parsing error: {e}", category="FORMATTING")
        # Offer feedback on error
        keyboard = [[InlineKeyboardButton(get_text("feedback_rate_bad", lang) + " (Error)", callback_data='rate_bad')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response, reply_markup=reply_markup)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user[1] if user else "en"
    doc = update.message.document

    # 1. Check File Type
    if not is_valid_file(doc.file_name):
        await update.message.reply_text(get_text("invalid_topic", lang))
        return

    # 2. Check File Size
    if doc.file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        await update.message.reply_text(get_text("file_too_large", lang, MAX_FILE_SIZE_MB))
        return

    # 3. Check Limits
    is_allowed, msg_count = check_limits(user_id, is_file=True)
    if not is_allowed:
        await update.message.reply_text(get_text("file_limit_reached", lang))
        return

    # 4. Process File
    await update.message.reply_text(get_text("processing_file", lang))
    
    file = await context.bot.get_file(doc.file_id)
    file_path = f"downloads/{doc.file_name}"
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    await file.download_to_drive(file_path)
    
    # Analyze
    analysis_result = analyze_excel(file_path)
    
    # Send analysis to Groq for insights with explicit language
    prompt = f"Analyze this data summary and provide insights or forecasts:\n\n{analysis_result}"
    await update.message.reply_chat_action("typing")
    response = await groq.get_response(prompt, lang=lang)
    
    if response:
        try:
            await update.message.reply_text(response, parse_mode="Markdown")
        except Exception as e:
            # Fallback to plain text if Markdown parsing fails
            log_error(f"Markdown parsing error (doc): {e}", category="FORMATTING")
            await update.message.reply_text(response)
        log_interaction(user_id, f"FILE: {doc.file_name}", response, "file")
        log_chat(user_id, f"FILE: {doc.file_name} (Analysis: {analysis_result[:100]}...)", response)
    else:
        await update.message.reply_text(get_text("error_generic", lang))
    
    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
        
    user_count, total_logs, error_breakdown, chat_log_count = get_stats()
    
    # Format error breakdown
    err_text = ""
    total_errors = 0
    if error_breakdown:
        err_text = "\n\nError Breakdown:"
        for cat, count in error_breakdown:
            err_text += f"\n- {cat}: {count}"
            total_errors += count
            
    user = get_user(update.effective_user.id)
    lang = user[1] if user else "en"
    
    final_stats = get_text("admin_stats", lang, user_count, total_logs, total_errors) + err_text
    final_stats += f"\n\nTotal Chat Logs: {chat_log_count}"
    await update.message.reply_text(final_stats)

async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    args = context.args
    limit = 20
    target_user = None
    
    if args:
        if args[0].isdigit():
            limit = int(args[0])
        elif args[0] == "user" and len(args) > 1:
            target_user = int(args[1])
            if len(args) > 2 and args[2].isdigit():
                limit = int(args[2])
    
    logs = get_admin_logs(limit, target_user)
    if not logs:
        await update.message.reply_text("No logs found.")
        return
    
    msg = "Recent Chat Logs:\n"
    for log in logs:
        # id, user_id, user_message, bot_reply, timestamp
        msg += f"\n👤 User {log[1]} ({log[4]}):\nQ: {log[2][:100]}...\nA: {log[3][:100]}...\n---"
        if len(msg) > 3500: # Telegram message limit
            await update.message.reply_text(msg)
            msg = ""
    
    if msg:
        await update.message.reply_text(msg)

async def export_logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    await update.message.reply_text("Generating Excel report...")
    try:
        file_path = export_logs_to_excel()
        with open(file_path, 'rb') as f:
            await update.message.reply_document(document=f, filename=file_path)
        os.remove(file_path)
    except Exception as e:
        log_error(f"Export logs error: {e}")
        await update.message.reply_text("Failed to export logs.")

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user[1] if user else "en"
    
    keyboard = [
        [
            InlineKeyboardButton(get_text("feedback_rate_good", lang), callback_data='rate_good'),
            InlineKeyboardButton(get_text("feedback_rate_bad", lang), callback_data='rate_bad')
        ],
        [InlineKeyboardButton(get_text("feedback_rate_suggestion", lang), callback_data='rate_suggest')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(get_text("feedback_cmd_prompt", lang), reply_markup=reply_markup)

async def feedback_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user[1] if user else "en"
    
    await query.answer()
    
    if query.data == 'rate_good':
        log_feedback(user_id, "GOOD")
        await query.edit_message_text(get_text("feedback_thanks", lang))
    elif query.data == 'rate_bad':
        log_feedback(user_id, "BAD")
        await query.edit_message_text(get_text("feedback_thanks", lang))
    elif query.data == 'rate_suggest':
        update_user_state(user_id, "WAIT_FEEDBACK", {})
        await query.edit_message_text(get_text("feedback_ask_suggestion", lang))
