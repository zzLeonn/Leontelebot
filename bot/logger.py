import logging
from telegram import Update

def log_command(update: Update, command: str):
    """Log command usage with additional context."""
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        logging.warning("Invalid update: user or chat not found.")
        return

    logging.info(
        f"Command /{command} used by user {user.id} ({user.username or 'no username'}) "
        f"in chat {chat.id} (type: {chat.type})."
    )

def log_message(update: Update):
    """Log received messages with additional context."""
    user = update.effective_user
    chat = update.effective_chat
    message = update.message.text if update.message else "No message content"

    if not user or not chat:
        logging.warning("Invalid update: user or chat not found.")
        return

    logging.info(
        f"Message received from user {user.id} ({user.username or 'no username'}) "
        f"in chat {chat.id} (type: {chat.type}): {message}"
    )

def log_error(update: Update, error: str):
    """Log errors with context."""
    user = update.effective_user if update else None
    chat = update.effective_chat if update else None

    logging.error(
        f"Error occurred for user {user.id if user else 'unknown'} "
        f"in chat {chat.id if chat else 'unknown'}: {error}"
    )