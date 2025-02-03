from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
import re
import logging

async def handle_prefix_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages that start with .nigga"""
    try:
        # Extract the text after .nigga
        text = update.message.text
        match = re.match(r'\.nigga\s*(.*)', text, re.IGNORECASE)  # Case insensitive matching
        if match:
            content = match.group(1).strip()
            if content:
                logging.info(f"Processing .nigga command with content: {content}")
                await update.message.reply_text(f"You said: {content}")
            else:
                await update.message.reply_text("Please add some text after .nigga")
    except Exception as e:
        logging.error(f"Error in handle_prefix_message: {str(e)}")
        await update.message.reply_text("An error occurred while processing your message.")

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

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general messages"""
    await update.message.reply_text(f"You said: {update.message.text}")

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

    # Add handler for .nigga prefix messages - place before the general echo handler
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex(r'(?i)\.nigga.*') & ~filters.COMMAND,  # Case insensitive regex
        handle_prefix_message
    ))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(handle_vote, pattern="^vote_"))
    application.add_handler(CallbackQueryHandler(handle_preference_callback, pattern="^(pref|lang)_"))

    # General message handler for other messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Error handler
    application.add_error_handler(error_handler)