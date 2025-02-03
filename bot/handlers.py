import logging
import random
import re
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    Application
)
import requests
from .config import (
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    ERROR_MESSAGE,
    INVALID_EXPRESSION,
    WEATHER_USAGE
)
from .logger import log_command, log_message
from .messages import get_response_for_text

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    log_command(update, "start")
    try:
        await update.message.reply_text(WELCOME_MESSAGE)
    except Exception as e:
        logging.error(f"Error in start_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    log_command(update, "help")
    try:
        await update.message.reply_text(HELP_MESSAGE)
    except Exception as e:
        logging.error(f"Error in help_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /joke command"""
    log_command(update, "joke")
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Miscellaneous,Pun,Spooky,Christmas?safe-mode&type=twopart")
        if response.status_code == 200:
            data = response.json()
            if data['type'] == 'single':
                joke = data['joke']
            else:
                joke = f"{data['setup']}\n\n{data['delivery']}"
            await update.message.reply_text(f"😄 Here's a joke for you:\n\n{joke}")
        else:
            await update.message.reply_text(ERROR_MESSAGE)
    except Exception as e:
        logging.error(f"Error in joke_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /quote command"""
    log_command(update, "quote")
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            quote = f"{data['content']}\n- {data['author']}"
            await update.message.reply_text(f"✨ Here's your quote:\n\n{quote}")
        else:
            await update.message.reply_text(ERROR_MESSAGE)
    except Exception as e:
        logging.error(f"Error in quote_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /fact command"""
    log_command(update, "fact")
    try:
        response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        if response.status_code == 200:
            data = response.json()
            fact = data['text']
            await update.message.reply_text(f"🤓 Did you know?\n\n{fact}")
        else:
            await update.message.reply_text(ERROR_MESSAGE)
    except Exception as e:
        logging.error(f"Error in fact_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /roll command"""
    log_command(update, "roll")
    try:
        result = random.randint(1, 6)
        await update.message.reply_text(f"🎲 You rolled a {result}!")
    except Exception as e:
        logging.error(f"Error in roll_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /calc command"""
    log_command(update, "calc")
    try:
        # Get the expression from the message
        expression = ' '.join(context.args)
        if not expression:
            await update.message.reply_text(INVALID_EXPRESSION)
            return

        # Clean and validate the expression
        if not re.match(r'^[\d\+\-\*\/\(\)\s\.]+$', expression):
            await update.message.reply_text(INVALID_EXPRESSION)
            return

        # Calculate the result
        result = eval(expression)
        await update.message.reply_text(f"🧮 {expression} = {result}")
    except Exception as e:
        logging.error(f"Error in calc_command: {str(e)}")
        await update.message.reply_text(INVALID_EXPRESSION)

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /weather command"""
    log_command(update, "weather")
    try:
        if not context.args:
            await update.message.reply_text(WEATHER_USAGE)
            return

        city = ' '.join(context.args)
        # Using OpenWeatherMap API
        API_KEY = "4ee0f92143bc013e827f995be66e5677"  # Free API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']

            weather_msg = (
                f"🌍 Weather in {city}:\n"
                f"🌤️ Condition: {weather_desc.capitalize()}\n"
                f"🌡️ Temperature: {temp}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind Speed: {wind} m/s"
            )
            await update.message.reply_text(weather_msg)
        else:
            await update.message.reply_text("Sorry, I couldn't find weather information for that city.")
    except Exception as e:
        logging.error(f"Error in weather_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages"""
    log_message(update)
    try:
        # Check for pattern-matched responses
        response = get_response_for_text(update.message.text)
        if response:
            await update.message.reply_text(response)
        else:
            # Default echo behavior
            await update.message.reply_text(f"You said: {update.message.text}")
    except Exception as e:
        logging.error(f"Error in echo handler: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logging.error(f"Update {update} caused error {context.error}")
    try:
        await update.message.reply_text(ERROR_MESSAGE)
    except:
        pass

def register_handlers(application: Application):
    """Register all handlers with the application"""
    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("joke", joke_command))
    application.add_handler(CommandHandler("quote", quote_command))
    application.add_handler(CommandHandler("roll", roll_command))
    application.add_handler(CommandHandler("fact", fact_command))
    application.add_handler(CommandHandler("calc", calc_command))
    application.add_handler(CommandHandler("weather", weather_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Error handler
    application.add_error_handler(error_handler)