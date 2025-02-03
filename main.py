import logging
import sys
from bot import create_bot

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    try:
        # Create and run the bot
        application = create_bot()
        application.run_polling()
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)