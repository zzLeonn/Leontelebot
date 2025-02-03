import os

# Bot Configuration
TELEGRAM_TOKEN = "8151451706:AAEbkxGi5LuvECuDeATtA4y0fs08dUpe2yM"

# Command descriptions
COMMANDS = {
    'start': 'Start the bot',
    'help': 'Show help message',
    'joke': 'Get a random joke',
    'quote': 'Get an inspirational quote',
    'roll': 'Roll a dice (1-6)',
    'fact': 'Get a random interesting fact',
    'calc': 'Calculate a math expression (e.g., /calc 2+2)',
    'weather': 'Get weather for a city (e.g., /weather London)',
}

# Bot messages
WELCOME_MESSAGE = """
👋 Hello! I'm Leon, your friendly bot assistant.
Use /help to see what I can do!
"""

HELP_MESSAGE = """
Here are the commands I understand:

/start - Start interacting with me
/help - Show this help message
/joke - Get a random joke
/quote - Get an inspirational quote
/roll - Roll a dice
/fact - Get an interesting fact
/calc [expression] - Calculate math expression
/weather [city] - Get weather for a city

You can also send me any message and I'll echo it back!
"""

ERROR_MESSAGE = "Sorry, I encountered an error processing your request. Please try again."
INVALID_EXPRESSION = "Sorry, I couldn't understand that expression. Please use simple math operations (e.g., /calc 2+2)"
WEATHER_USAGE = "Please provide a city name (e.g., /weather London)"