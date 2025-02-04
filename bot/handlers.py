import os
from dotenv import load_dotenv  # Import the load_dotenv function
import requests
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
import logging

# Load environment variables from the .env file
load_dotenv()

from bot.logger import log_command
from config import WELCOME_MESSAGE, HELP_MESSAGE, ERROR_MESSAGE
from bot.messages import get_response_for_text


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables for API keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
if not GOOGLE_SEARCH_ENGINE_ID:
    raise ValueError("GOOGLE_SEARCH_ENGINE_ID environment variable is not set.")
    raise ValueError("No Google API key found in environment variables.")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "f67799191a4754602")

# Utility function to search for images/GIFs using Google Custom Search API
def search_images(query, search_type="image"):
    """
    Search for images or GIFs using the Google Custom Search API.
    :param query: The search query (e.g., "cat")
    :param search_type: The type of search ("image" or "gif")
    :return: A list of image URLs or an empty list if no results are found.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": query,
        "searchType": search_type,
        "num": 5,  # Number of results to return
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract image URLs from the response
        image_urls = [item["link"] for item in data.get("items", []) if "link" in item]
        return image_urls
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching images: {e}")
        return []

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command(update, "start")
    """Handle the /start command"""
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    await update.message.reply_text(HELP_MESSAGE)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /cancel command"""
    await update.message.reply_text("Operation cancelled.")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /weather command"""
    if not context.args:
        await update.message.reply_text("Please provide a city name (e.g., /weather London)")
        return

    city = " ".join(context.args)
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    if not weather_api_key:
        await update.message.reply_text("Weather API key is not set.")
        return

    # Build the URL for the OpenWeatherMap API.
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses.
        data = response.json()

        # Extract useful data
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Format the reply message.
        reply_text = (
            f"Weather in {city}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {description.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
    except requests.exceptions.HTTPError as http_err:
        reply_text = f"HTTP error occurred: {http_err}"
    except Exception as e:
        reply_text = f"Error fetching weather data: {e}"

    await update.message.reply_text(reply_text)

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /image command"""
    if not context.args:
        await update.message.reply_text("Please provide a search term (e.g., /image cat)")
        return

    query = " ".join(context.args)
    image_urls = search_images(query, search_type="image")

    if not image_urls:
        await update.message.reply_text("No images found. Try another search term.")
        return

    # Send the first image
    await update.message.reply_photo(image_urls[0])

async def gif_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /gif command"""
    if not context.args:
        await update.message.reply_text("Please provide a search term (e.g., /gif cat)")
        return

    query = " ".join(context.args)
    image_urls = search_images(query, search_type="gif")

    if not image_urls:
        await update.message.reply_text("No GIFs found. Try another search term.")
        return

    # Send the first GIF
    await update.message.reply_animation(image_urls[0])


async def poll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /poll command"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /poll Question Option1 Option2 [Option3...]")
        return
    question = context.args[0]
    options = context.args[1:]
    # Add logic to create a poll
    await update.message.reply_text(f"Poll created: {question} with options {', '.join(options)}")

async def karma_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /karma command"""
    user_id = update.message.from_user.id
    # Add logic to fetch karma points for the user
    await update.message.reply_text(f"Your karma points: 100 (example)")

async def give_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /give command"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to give karma.")
        return
    giver_id = update.message.from_user.id
    receiver_id = update.message.reply_to_message.from_user.id
    # Add logic to give karma
    await update.message.reply_text(f"Karma given to user {receiver_id} (example)")

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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general messages using our response system"""
    text = update.message.text
    response = get_response_for_text(text)
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error: {context.error}", exc_info=True)
    try:
        if update.message:
            await update.message.reply_text(ERROR_MESSAGE)
    except:
        pass

def register_handlers(application):
    """Register all handlers with the application"""
    # Command handlers
    application.add_handler(CommandHandler("start", start_command))  # Handles the /start command
    application.add_handler(CommandHandler("help", help_command))  # Handles the /help command
    application.add_handler(CommandHandler("cancel", cancel_command))  # Handles the /cancel command
    application.add_handler(CommandHandler("preferences", preferences_command))  # Handles the /preferences command
    application.add_handler(CommandHandler("weather", weather_command))  # Handles the /weather command
    application.add_handler(CommandHandler("poll", poll_command))  # Handles the /poll command
    application.add_handler(CommandHandler("karma", karma_command))  # Handles the /karma command
    application.add_handler(CommandHandler("give", give_command))  # Handles the /give command
    application.add_handler(CommandHandler("gif", gif_command))  # Handles the /gif command
    application.add_handler(CommandHandler("image", image_command))  # Handles the /image command

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(handle_vote, pattern="^vote_"))  # Handles vote callbacks
    application.add_handler(CallbackQueryHandler(handle_preference_callback, pattern="^(pref|lang)_"))  # Handles preference callbacks

    # General message handler for other messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Handles general text messages

    # Error handler
    application.add_error_handler(error_handler)  # Handles errors