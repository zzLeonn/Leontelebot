"""Message patterns and responses for the bot"""
import random

# Greeting patterns and responses
GREETING_PATTERNS = [
    'hi', 'hello', 'hey', 'howdy', 'hola', 'morning', 'evening', 'afternoon',
    'sup', 'yo', 'hiya', 'good morning', 'good evening', 'good afternoon'
]

GREETING_RESPONSES = [
    "👋 Hey there! How can I help you today?",
    "Hello! Nice to see you! 😊",
    "Hi there! Hope you're having a great day! ✨",
    "Hey! I'm here if you need anything! 🌟",
    "Greetings! How may I assist you? 🤖",
    "Hello! Ready to chat! 💬",
]

# Goodbye patterns and responses
GOODBYE_PATTERNS = [
    'bye', 'goodbye', 'see you', 'cya', 'good night', 'night', 'farewell',
    'have to go', 'gtg', 'catch you later', 'see ya'
]

GOODBYE_RESPONSES = [
    "Goodbye! Have a great day! 👋",
    "See you later! Take care! ✨",
    "Bye! Come back soon! 🌟",
    "Farewell! It was nice chatting! 😊",
    "Catch you later! Stay awesome! 🚀",
    "Have a good one! See you around! 💫",
]

# Thank you patterns and responses
THANKS_PATTERNS = [
    'thanks', 'thank you', 'thx', 'thank u', 'appreciated', 'gracias', 'ty'
]

THANKS_RESPONSES = [
    "You're welcome! 😊",
    "Anytime! Happy to help! ✨",
    "No problem at all! 🌟",
    "My pleasure! 💫",
    "Glad I could help! 🤖",
    "You're most welcome! 💝",
]

# How are you patterns and responses
HOW_ARE_YOU_PATTERNS = [
    'how are you', 'how r u', 'how\'re you', 'how you doing', 'whats up',
    'what\'s up', 'sup', 'how do you do', 'how are things', 'yo'
]

HOW_ARE_YOU_RESPONSES = [
    "I'm doing great, thanks for asking! How about you? 😊",
    "All systems operational and feeling fantastic! How are you? 🤖",
    "I'm having a wonderful day! Hope you are too! ✨",
    "I'm good! Always happy to chat with you! 🌟",
    "Doing well and ready to help! How's your day going? 💫",
    "I'm excellent! Thanks for checking on me! 💝",
    "Yo! I'm totally vibing! What's new with you? 🎵",
    "Living my best bot life! How about you? 🌈",
]

# What can you do patterns and responses
CAPABILITIES_PATTERNS = [
    'what can you do', 'what do you do', 'help me', 'your abilities',
    'what are you capable of', 'what are your features', 'commands',
    'what can i do', 'how to use', 'show me'
]

CAPABILITIES_RESPONSES = [
    """Here's what I can do for you! 🌟

/start - Start our chat
/help - See all my commands
/joke - Get a funny joke
/quote - Get an inspiring quote
/fact - Learn something new
/roll - Roll a dice
/calc - Do some math
/weather - Check the weather

You can also just chat with me! I love making new friends! 🤖✨""",
    """I'm your friendly bot assistant! Here are my skills 🎯

• Tell you jokes (/joke)
• Share inspiring quotes (/quote)
• Teach you fun facts (/fact)
• Roll a dice (/roll)
• Help with calculations (/calc)
• Check weather (/weather)

Plus, I love chatting! What would you like to try? 🚀""",
    """Let me show you what I can do! 🌈

🎭 Entertainment:
• /joke - Fun jokes
• /quote - Daily inspiration
• /fact - Interesting facts
• /roll - Roll the dice

🛠️ Utilities:
• /calc - Calculator
• /weather - Weather updates

Want to try any of these? 😊"""
]

# Unknown message responses
UNKNOWN_MESSAGE_RESPONSES = [
    "I'm intrigued! Tell me more about that! 🤔",
    "That's interesting! Want to try one of my commands? Use /help to see what I can do! ✨",
    "Cool! By the way, I know lots of fun facts and jokes. Want to hear one? Try /fact or /joke! 🌟",
    "Interesting! I'd love to chat more about that! I can also help with other things - just type /help to see how! 🎯",
    "Nice! While we're chatting, would you like to hear a joke or get an inspiring quote? Just use /joke or /quote! 💫",
    "That's fascinating! I can also help you with weather updates, calculations, and more! Type /help to explore! 🌈"
]

def get_response_for_text(text: str) -> str:
    """Get appropriate response based on the input text"""
    text = text.lower().strip()

    if any(pattern in text for pattern in GREETING_PATTERNS):
        return random.choice(GREETING_RESPONSES)

    if any(pattern in text for pattern in GOODBYE_PATTERNS):
        return random.choice(GOODBYE_RESPONSES)

    if any(pattern in text for pattern in THANKS_PATTERNS):
        return random.choice(THANKS_RESPONSES)

    if any(pattern in text for pattern in HOW_ARE_YOU_PATTERNS):
        return random.choice(HOW_ARE_YOU_RESPONSES)

    if any(pattern in text for pattern in CAPABILITIES_PATTERNS):
        return random.choice(CAPABILITIES_RESPONSES)

    # Instead of returning None for unknown messages, return a friendly response
    return random.choice(UNKNOWN_MESSAGE_RESPONSES)