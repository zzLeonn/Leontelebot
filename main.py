import logging
from bot import create_bot

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )
    
    # Create and run the bot
    application = create_bot()
    application.run_polling()
