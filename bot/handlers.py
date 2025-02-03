from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
import logging
from .messages import get_response_for_text

async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle vote callbacks"""
    query = update.callback_query
    await query.answer("Vote registered!")

async def handle_preference_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle preference callbacks"""
    query = update.callback_query
    await query.answer("Preference updated!")

async def preferences_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle preferences command"""
    await update.message.reply_text("Preferences menu")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general messages using our response system"""
    text = update.message.text
    response = get_response_for_text(text)
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logging.error(f"Update {update} caused error {context.error}")
    try:
        if update.message:
            await update.message.reply_text("An error occurred while processing your request.")
    except:
        pass

def register_handlers(application):
    """Register all handlers with the application"""
    # Command handlers
    application.add_handler(CommandHandler("preferences", preferences_command))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(handle_vote, pattern="^vote_"))
    application.add_handler(CallbackQueryHandler(handle_preference_callback, pattern="^(pref|lang)_"))

    # General message handler for other messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    application.add_error_handler(error_handler)