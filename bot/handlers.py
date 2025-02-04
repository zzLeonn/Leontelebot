import os
from dotenv import load_dotenv 
import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
     ConversationHandler,
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


POLL_QUESTION, POLL_OPTIONS, ADD_OPTION = range(3)

async def poll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start poll creation conversation."""
    # Initialize poll data in user_data
    context.user_data['poll'] = {"question": None, "options": []}
    await update.message.reply_text("Please send the poll question:")
    return POLL_QUESTION

async def poll_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the poll question input."""
    poll = context.user_data.get('poll', {})
    poll['question'] = update.message.text
    context.user_data['poll'] = poll

    # Show inline keyboard to add options or finish poll
    keyboard = [
        [InlineKeyboardButton("Add Option", callback_data="add_option")],
        [InlineKeyboardButton("Finish Poll", callback_data="finish_poll")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Poll Question: {poll['question']}\n"
        "Now, click 'Add Option' to add an option, or 'Finish Poll' if you're done.",
        reply_markup=reply_markup
    )
    return POLL_OPTIONS

async def poll_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks for poll creation."""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    data = query.data

    if data == "add_option":
        # Prompt user to send a new option as text
        await query.message.reply_text("Please send the new poll option:")
        return ADD_OPTION

    elif data == "finish_poll":
        # Finalize poll creation and show the poll summary
        poll = context.user_data.get('poll', {})
        question = poll.get('question', 'No question')
        options = poll.get('options', [])
        if not options:
            await query.message.reply_text("You need to add at least one option.")
            return POLL_OPTIONS
        options_list = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options))
        await query.message.reply_text(
            f"Poll created!\nQuestion: {question}\nOptions:\n{options_list}"
        )
        return ConversationHandler.END

async def add_option_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive new poll option and update the poll summary."""
    new_option = update.message.text
    poll = context.user_data.get('poll', {})
    poll.setdefault('options', []).append(new_option)
    context.user_data['poll'] = poll

    # Build a summary of the poll
    options_list = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(poll['options']))
    keyboard = [
        [InlineKeyboardButton("Add Option", callback_data="add_option")],
        [InlineKeyboardButton("Finish Poll", callback_data="finish_poll")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Poll Question: {poll.get('question')}\n"
        f"Options:\n{options_list}\n\n"
        "Click 'Add Option' to add more or 'Finish Poll' to complete.",
        reply_markup=reply_markup
    )
    return POLL_OPTIONS

async def cancel_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the poll creation process."""
    await update.message.reply_text("Poll creation cancelled.")
    return ConversationHandler.END

def get_poll_conversation_handler():
    """Return the ConversationHandler for poll creation."""
    return ConversationHandler(
        entry_points=[CommandHandler("poll", poll_command)],
        states={
            POLL_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, poll_question_handler)],
            POLL_OPTIONS: [CallbackQueryHandler(poll_callback_handler)],
            ADD_OPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_option_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel_poll)]
    )

karma_data = {}

async def karma_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /karma command"""
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # Initialize karma if the user doesn't exist in the dictionary
    if user_id not in karma_data:
        karma_data[user_id] = {"username": username, "karma": 0}

    # Fetch the user's karma
    karma = karma_data[user_id]["karma"]

    # Reply with the user's karma points
    await update.message.reply_text(f"@{username}, your karma points: {karma}")

async def track_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Track user messages and update karma."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # Initialize karma if the user doesn't exist in the dictionary
    if user_id not in karma_data:
        karma_data[user_id] = {"username": username, "karma": 0}

    # Award 1 karma point for sending a message
    karma_data[user_id]["karma"] += 1

async def give_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /give command"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to give karma.")
        return

    giver_id = update.message.from_user.id
    receiver_id = update.message.reply_to_message.from_user.id

    # Ensure both users exist in the karma data
    if giver_id not in karma_data:
        karma_data[giver_id] = {"username": update.message.from_user.username, "karma": 0}
    if receiver_id not in karma_data:
        karma_data[receiver_id] = {"username": update.message.reply_to_message.from_user.username, "karma": 0}

    # Transfer 1 karma point from giver to receiver
    if karma_data[giver_id]["karma"] > 0:
        karma_data[giver_id]["karma"] -= 1
        karma_data[receiver_id]["karma"] += 1
        await update.message.reply_text(
            f"@{karma_data[giver_id]['username']} gave 1 karma to @{karma_data[receiver_id]['username']}!"
        )
    else:
        await update.message.reply_text("You don't have enough karma to give.")

async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle vote callbacks"""
    query = update.callback_query
    await query.answer("Vote registered!")

async def handle_preference_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callbacks from the preferences menu."""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    data = query.data
    response_text = "Unknown preference option."

    if data == "pref_language":
        # Here you might display a sub-menu to select a language.
        response_text = "Language settings: Choose your preferred language."
    elif data == "pref_notifications":
        # Toggle notifications (this is just a placeholder).
        response_text = "Notifications toggled."
    elif data == "pref_theme":
        # Change theme option (this is just a placeholder).
        response_text = "Theme changed."
    
    # Optionally, update the message or send a new one:
    await query.edit_message_text(text=response_text)


async def preferences_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle preferences command by showing an inline keyboard menu."""
    keyboard = [
        [InlineKeyboardButton("Set Language", callback_data="pref_language")],
        [InlineKeyboardButton("Toggle Notifications", callback_data="pref_notifications")],
        [InlineKeyboardButton("Change Theme", callback_data="pref_theme")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Preferences Menu:\nChoose an option:", reply_markup=reply_markup)

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
    # Remove the plain /poll command handler since we are using a ConversationHandler for polls
    # application.add_handler(CommandHandler("poll", poll_command))
    application.add_handler(CommandHandler("karma", karma_command))  # Handles the /karma command
    application.add_handler(CommandHandler("give", give_command))  # Handles the /give command
    application.add_handler(CommandHandler("gif", gif_command))  # Handles the /gif command
    application.add_handler(CommandHandler("image", image_command))  # Handles the /image command
    
    # Add the poll conversation handler for a more interactive poll creation process
    application.add_handler(get_poll_conversation_handler())

    # General text message handler (if not already registered)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(handle_vote, pattern="^vote_"))  # Handles vote callbacks
    application.add_handler(CallbackQueryHandler(handle_preference_callback, pattern="^pref_"))  # Handles preference callbacks

    # Error handler
    application.add_error_handler(error_handler)  # Handles errors
