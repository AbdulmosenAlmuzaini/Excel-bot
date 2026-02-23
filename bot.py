from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TELEGRAM_BOT_TOKEN
from handlers import start, language_callback, help_command, examples_command, lang_command, handle_message, handle_document, admin_stats, clarification_callback, feedback_command, feedback_callback, logs_command, export_logs_command, example_callback, learn_command, learning_callback, video_lang_callback
from database import init_db
from logger import log_info, log_error
import html
import json

async def error_handler(update: object, context: object) -> None:
    log_error(f"Exception while handling an update: {context.error}")
    
    # Log the error to the user if it's an update we can respond to
    if update and hasattr(update, 'effective_message') and update.effective_message:
        from i18n import get_text
        user_id = update.effective_user.id if update.effective_user else None
        # We don't have the lang here easily, but we can try to get it or default to en
        await update.effective_message.reply_text("عذراً، حدث خطأ داخلي. تم إبلاغ المطور.\nSorry, an internal error occurred.")

def main():
    init_db()
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("examples", examples_command))
    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CommandHandler("stats", admin_stats))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(CommandHandler("learn", learn_command))
    application.add_handler(CommandHandler("logs", logs_command))
    application.add_handler(CommandHandler("export_logs", export_logs_command))
    
    application.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    application.add_handler(CallbackQueryHandler(clarification_callback, pattern='^clarify_'))
    application.add_handler(CallbackQueryHandler(feedback_callback, pattern='^rate_'))
    application.add_handler(CallbackQueryHandler(video_lang_callback, pattern='^vlang_'))
    application.add_handler(CallbackQueryHandler(example_callback, pattern='^ex_'))
    application.add_handler(CallbackQueryHandler(learning_callback, pattern='^learn_'))
    
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Error handler
    application.add_error_handler(error_handler)

    log_info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
