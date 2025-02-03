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
    'what\'s up', 'sup', 'how do you do', 'how are things'
]

HOW_ARE_YOU_RESPONSES = [
    "I'm doing great, thanks for asking! How about you? 😊",
    "All systems operational and feeling fantastic! How are you? 🤖",
    "I'm having a wonderful day! Hope you are too! ✨",
    "I'm good! Always happy to chat with you! 🌟",
    "Doing well and ready to help! How's your day going? 💫",
    "I'm excellent! Thanks for checking on me! 💝",
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
    
    return None
