import logging
from telegram import Update

def log_command(update: Update, command: str):
    """Log command usage"""
    user = update.effective_user
    chat = update.effective_chat
    logging.info(
        f"Command /{command} used by user {user.id} ({user.username}) "
        f"in chat {chat.id}"
    )

def log_message(update: Update):
    """Log received messages"""
    user = update.effective_user
    chat = update.effective_chat
    message = update.message.text
    logging.info(
        f"Message received from user {user.id} ({user.username}) "
        f"in chat {chat.id}: {message}"
    )
