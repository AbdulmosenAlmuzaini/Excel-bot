from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TELEGRAM_BOT_TOKEN
from handlers import start, language_callback, help_command, examples_command, lang_command, handle_message, handle_document, admin_stats, clarification_callback, feedback_command, feedback_callback, logs_command, export_logs_command, example_callback, learn_command, learning_callback
from database import init_db
from logger import log_info, log_error

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
    application.add_handler(CallbackQueryHandler(example_callback, pattern='^ex_'))
    application.add_handler(CallbackQueryHandler(learning_callback, pattern='^learn_'))
    
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    log_info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
