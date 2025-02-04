import logging
import sys
from bot import create_bot

# Configure logging before anything else
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("bot.log"),  # Log to a file
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        application = create_bot()
        application.run_polling()
        logger.info("Bot stopped gracefully")
    except RuntimeError as e:
        logger.critical(f"Runtime error: {str(e)}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Bot process terminated")