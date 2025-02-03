import os
import fcntl
from telegram.ext import ApplicationBuilder
from .config import TELEGRAM_TOKEN
from .handlers import register_handlers

def create_bot():
    """Initialize and configure the bot application"""
    # Create a lock file to prevent multiple instances
    lock_file = '/tmp/telegram_bot.lock'

    try:
        # Try to acquire the lock
        lock_fd = open(lock_file, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

        # Create the Application instance
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        # Register all handlers
        register_handlers(application)

        return application
    except IOError:
        raise RuntimeError("Another instance of the bot is already running")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize bot: {str(e)}")