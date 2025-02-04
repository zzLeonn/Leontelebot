import logging
import sys
from bot import create_bot

# Configure logging before anything else
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,  # Use INFO for production, DEBUG for development
    handlers=[
        logging.StreamHandler(sys.stdout)
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