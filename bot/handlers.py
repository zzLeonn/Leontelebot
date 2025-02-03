import logging
import random
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, ChatMember
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    Application,
    CallbackQueryHandler
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

# Store user points/karma
user_points = {}
# Store user preferences
user_preferences = {}
# Store active polls
active_polls = {}

async def check_group_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if bot has necessary permissions in a group"""
    try:
        if update.effective_chat.type in ['group', 'supergroup']:
            bot_member = await context.bot.get_chat_member(
                update.effective_chat.id,
                context.bot.id
            )
            return bot_member.status in ['administrator', 'member']
        return True
    except Exception as e:
        logging.error(f"Error checking permissions: {str(e)}")
        return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    log_command(update, "start")
    try:
        if not await check_group_permissions(update, context):
            return
        await update.message.reply_text(WELCOME_MESSAGE)
    except Exception as e:
        logging.error(f"Error in start_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    log_command(update, "help")
    try:
        if not await check_group_permissions(update, context):
            return
        await update.message.reply_text(HELP_MESSAGE)
    except Exception as e:
        logging.error(f"Error in help_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /joke command"""
    log_command(update, "joke")
    try:
        if not await check_group_permissions(update, context):
            return
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
        if not await check_group_permissions(update, context):
           return
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
        if not await check_group_permissions(update, context):
            return
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
        if not await check_group_permissions(update, context):
            return
        result = random.randint(1, 6)
        await update.message.reply_text(f"🎲 You rolled a {result}!")
    except Exception as e:
        logging.error(f"Error in roll_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /calc command"""
    log_command(update, "calc")
    try:
        if not await check_group_permissions(update, context):
            return
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
        if not await check_group_permissions(update, context):
            return
        if not context.args:
            await update.message.reply_text(WEATHER_USAGE)
            return

        city = ' '.join(context.args)
        API_KEY = os.environ.get("OPENWEATHER_API_KEY")

        if not API_KEY:
            await update.message.reply_text("Weather service is currently unavailable. Please try again later.")
            return

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

async def poll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /poll command"""
    log_command(update, "poll")
    try:
        if not await check_group_permissions(update, context):
            return
        # Check if there are arguments
        if not context.args or len(context.args) < 3:
            await update.message.reply_text(
                "Please provide a question and at least 2 options.\n"
                "Usage: /poll Question? Option1 Option2 [Option3...]"
            )
            return

        # First argument is the question
        question = context.args[0].replace('_', ' ')
        options = [opt.replace('_', ' ') for opt in context.args[1:]]

        # Create keyboard with options
        keyboard = []
        for idx, option in enumerate(options):
            keyboard.append([InlineKeyboardButton(
                option, callback_data=f"vote_{update.message.message_id}_{idx}"
            )])

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Initialize poll results
        active_polls[update.message.message_id] = {
            'question': question,
            'options': options,
            'votes': {i: [] for i in range(len(options))}
        }

        await update.message.reply_text(
            f"📊 Poll: {question}\n\nClick to vote:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error in poll_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle poll votes"""
    query = update.callback_query
    try:
        # Extract poll ID and choice from callback data
        _, poll_id, choice = query.data.split('_')
        poll_id = int(poll_id)
        choice = int(choice)

        if poll_id not in active_polls:
            await query.answer("This poll has expired!")
            return

        poll = active_polls[poll_id]
        user_id = query.from_user.id

        # Remove user's previous vote if any
        for votes in poll['votes'].values():
            if user_id in votes:
                votes.remove(user_id)

        # Add new vote
        poll['votes'][choice].append(user_id)

        # Create results message
        results = f"📊 Poll: {poll['question']}\n\nResults:\n"
        for idx, option in enumerate(poll['options']):
            votes = len(poll['votes'][idx])
            results += f"\n{option}: {votes} vote(s)"

        # Update message with new results
        await query.message.edit_text(
            results,
            reply_markup=query.message.reply_markup
        )
        await query.answer("Your vote has been recorded!")

    except Exception as e:
        logging.error(f"Error in handle_vote: {str(e)}")
        await query.answer("An error occurred while processing your vote.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages"""
    log_message(update)
    try:
        # Only respond to messages in private chats or when mentioned in groups
        if update.effective_chat.type != 'private':
            # Check if bot was mentioned or message is a reply to bot's message
            if not (update.message.entities and any(
                entity.type == 'mention' and context.bot.username in update.message.text[entity.offset:entity.offset + entity.length]
                for entity in update.message.entities
            )):
                return

        if not await check_group_permissions(update, context):
            return

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

async def gif_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /gif command"""
    log_command(update, "gif")
    try:
        if not await check_group_permissions(update, context):
            return
        if not context.args:
            await update.message.reply_text("Please provide a search term (e.g., /gif cat)")
            return

        search_term = ' '.join(context.args)
        API_KEY = os.environ.get("TENOR_API_KEY")
        if not API_KEY:
            await update.message.reply_text("Tenor API key not configured. Please contact the bot administrator.")
            return

        limit = 1
        url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={API_KEY}&limit={limit}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                gif_url = data['results'][0]['media_formats']['gif']['url']
                await update.message.reply_animation(gif_url)
            else:
                await update.message.reply_text("Sorry, I couldn't find any GIFs for that search term.")
        else:
            await update.message.reply_text(ERROR_MESSAGE)
    except Exception as e:
        logging.error(f"Error in gif_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /image command"""
    log_command(update, "image")
    try:
        if not await check_group_permissions(update, context):
            await update.message.reply_text("I don't have permission to send media in this group!")
            return

        if not context.args:
            await update.message.reply_text("Please provide a search term (e.g., /image nature)")
            return

        search_term = ' '.join(context.args)
        API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY")
        SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")

        if not API_KEY or not SEARCH_ENGINE_ID:
            await update.message.reply_text("Google Search API not properly configured. Please contact the bot administrator.")
            return

        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_term}&searchType=image&safe=active"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and data['items']:
                # Get first 5 images or less if fewer results are available
                num_images = min(5, len(data['items']))
                images = []
                for i in range(num_images):
                    image_url = data['items'][i]['link']
                    images.append(InputMediaPhoto(media=image_url))

                try:
                    # Send as a media group if multiple images, single photo otherwise
                    if len(images) > 1:
                        await update.message.reply_media_group(media=images)
                    else:
                        await update.message.reply_photo(images[0].media)
                except Exception as media_error:
                    logging.error(f"Error sending media: {str(media_error)}")
                    await update.message.reply_text("Sorry, I couldn't send the images. Please make sure I have permission to send media in this group.")
            else:
                await update.message.reply_text("Sorry, I couldn't find any images for that search term.")
        else:
            logging.error(f"Google Search API error: {response.status_code} - {response.text}")
            await update.message.reply_text("Sorry, there was an error searching for images. Please try again later.")
    except Exception as e:
        logging.error(f"Error in image_command: {str(e)}")
        await update.message.reply_text("An error occurred while processing your request. Please try again later.")

async def karma_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /karma command - check your karma points"""
    log_command(update, "karma")
    try:
        if not await check_group_permissions(update, context):
            return
        user_id = update.effective_user.id
        points = user_points.get(user_id, 0)
        await update.message.reply_text(f"🌟 Your karma points: {points}")
    except Exception as e:
        logging.error(f"Error in karma_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def give_karma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /give command - give karma to another user"""
    log_command(update, "give")
    try:
        if not await check_group_permissions(update, context):
            return
        if not update.message.reply_to_message:
            await update.message.reply_text("Please reply to a message to give karma to that user!")
            return

        giver_id = update.effective_user.id
        receiver_id = update.message.reply_to_message.from_user.id

        if giver_id == receiver_id:
            await update.message.reply_text("You can't give karma to yourself!")
            return

        # Initialize points if needed
        if receiver_id not in user_points:
            user_points[receiver_id] = 0

        # Give one point
        user_points[receiver_id] += 1
        await update.message.reply_text(f"✨ Karma point given! They now have {user_points[receiver_id]} points!")
    except Exception as e:
        logging.error(f"Error in give_karma: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def preferences_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /preferences command"""
    log_command(update, "preferences")
    try:
        if not await check_group_permissions(update, context):
           return
        user_id = update.effective_user.id

        # Initialize preferences if not set
        if user_id not in user_preferences:
            user_preferences[user_id] = {
                'custom_welcome': None,
                'language': 'en',
                'notifications': True
            }

        prefs = user_preferences[user_id]
        keyboard = [
            [InlineKeyboardButton("Set Welcome Message", callback_data="pref_welcome")],
            [InlineKeyboardButton("Toggle Notifications", callback_data="pref_notif")],
            [InlineKeyboardButton("Language", callback_data="pref_lang")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            "🔧 Your Preferences:\n\n"
            f"Welcome Message: {prefs['custom_welcome'] or 'Default'}\n"
            f"Language: {prefs['language']}\n"
            f"Notifications: {'On' if prefs['notifications'] else 'Off'}"
        )

        await update.message.reply_text(message, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"Error in preferences_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def handle_preference_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle preference menu callbacks"""
    query = update.callback_query
    user_id = query.from_user.id

    try:
        if query.data == "pref_notif":
            # Toggle notifications
            if user_id not in user_preferences:
                user_preferences[user_id] = {'notifications': True}
            user_preferences[user_id]['notifications'] = not user_preferences[user_id].get('notifications', True)
            status = "on" if user_preferences[user_id]['notifications'] else "off"
            await query.message.edit_text(f"Notifications turned {status}!")

        elif query.data == "pref_welcome":
            # Enter state for setting welcome message
            context.user_data['setting_welcome'] = True
            await query.message.edit_text("Please send your custom welcome message:")

        elif query.data == "pref_lang":
            # Show language options
            keyboard = [
                [InlineKeyboardButton("English", callback_data="lang_en")],
                [InlineKeyboardButton("Spanish", callback_data="lang_es")],
                [InlineKeyboardButton("French", callback_data="lang_fr")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text("Select your language:", reply_markup=reply_markup)

        elif query.data.startswith("lang_"):
            # Set language preference
            lang = query.data.split("_")[1]
            if user_id not in user_preferences:
                user_preferences[user_id] = {}
            user_preferences[user_id]['language'] = lang
            await query.message.edit_text(f"Language set to: {lang}")

        await query.answer()
    except Exception as e:
        logging.error(f"Error in handle_preference_callback: {str(e)}")
        await query.answer("An error occurred!")

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
    application.add_handler(CommandHandler("poll", poll_command))
    application.add_handler(CommandHandler("gif", gif_command))
    application.add_handler(CommandHandler("image", image_command))

    # Add new command handlers
    application.add_handler(CommandHandler("karma", karma_command))
    application.add_handler(CommandHandler("give", give_karma))
    application.add_handler(CommandHandler("preferences", preferences_command))

    # Callback query handler for poll votes
    application.add_handler(CallbackQueryHandler(handle_vote, pattern="^vote_"))

    # Add callback query handler for preferences
    application.add_handler(CallbackQueryHandler(handle_preference_callback, pattern="^(pref|lang)_"))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Error handler
    application.add_error_handler(error_handler)