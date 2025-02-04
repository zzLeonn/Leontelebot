import os
from telegram.ext import ApplicationBuilder
from .config import TELEGRAM_TOKEN
from .handlers import register_handlers

def create_bot():
    """Initialize and configure the bot application"""
    try:
        # Create the Application instance
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        # Register all handlers
        register_handlers(application)

        return application

    except Exception as e:
        raise RuntimeError(f"Failed to initialize bot: {str(e)}")

def run_bot():
    """Run the bot application"""
    application = create_bot()

    try:
        # Start the bot
        application.run_polling()
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        print("Bot is shutting down...")
    finally:
        # Ensure the application stops gracefully
        if application:
            application.stop()

if __name__ == "__main__":
    run_bot()