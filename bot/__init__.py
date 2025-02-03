from telegram.ext import ApplicationBuilder
from .config import TELEGRAM_TOKEN
from .handlers import register_handlers

def create_bot():
    """Initialize and configure the bot application"""
    # Create the Application instance
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Register all handlers
    register_handlers(application)
    
    return application
