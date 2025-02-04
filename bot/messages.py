"""Message patterns and responses for the bot"""
import random

# Greeting patterns and responses
GREETING_PATTERNS = [
    'hi', 'hello', 'hey', 'lee', 'nigga', 'morning', 'evening', 'lee lr',
    'sup', 'yo', 'koko', 'good morning', 'good evening', 'min phane loe'
]

GREETING_RESPONSES = [
    "yo nigga whats up",
    "lee lr br ll phin loe ml",
    "hey baby girl how you doing ",
    "u make me bricked whats up ",
    "br ll chou 1v1 ",
    "hi what do u want",
]

# Goodbye patterns and responses
GOODBYE_PATTERNS = [
    'bye', 'goodbye', 'see you', 'cya', 'good night', 'night', 'farewell',
    'have to go', 'gtg', 'time to sleep man', 'see ya'
]

GOODBYE_RESPONSES = [
    "fine bye bye leave me",
    "i hope u slip and die",
    "leave just like your dad",
    "alright man no one cares",
    "fuck off",
    "k",
]

# Thank you patterns and responses
THANKS_PATTERNS = [
    'thanks', 'thank you', 'thx', 'thank u', 'appreciated', 'chit tl', 'ty'
]

THANKS_RESPONSES = [
    "u owe me one suck(pod) 😊",
    "give me money now or ill leak ur ip",
    "i know ur cheating on me",
    "thanks man",
    "no worries",
    "chit lr chit yin p yw",
]

# How are you patterns and responses
HOW_ARE_YOU_PATTERNS = [
    'how are you', 'how r u', 'how\'re you', 'how you doing', 'whats up',
    'what\'s up', 'sup', 'how do you do', 'you good', 'yo'
]

HOW_ARE_YOU_RESPONSES = [
    "oh im actually good im just suicidal",
    "no one loves me im gonna die alone",
    "i think im having a mental breakdown",
    "ok bro no one cares",
    "i wanna kill myself",
    "eat shit",
    "do u think things are good u dumb fuck",
    "depressed gimme ways to get out"
]

# What can you do patterns and responses
CAPABILITIES_PATTERNS = [
    'yo leon', 'bro what can leon do', 'help me', 'your abilities',
    'what are you capable of', 'what are your features', 'commands',
    'what can i do', 'how to use', 'show me'
]

CAPABILITIES_RESPONSES = [
    """some shit i can do for ur lazy ass

/start - be nice to u
/help - list my entire command shit
/joke - get an ai unfunny joke
/quote - quotes to be less depressed
/fact - u never know what u will find
/roll - gamble it out
/calc - math bro ew
/weather - will it rain or will it be a tsunami

u can chat with me too im your friendly depressed ai""",
    """im leon this is some of the things i can do for u

• u want me to tell a joke? (/joke)
• dumbass quotes (/quote)
• weird facts (/fact)
• gamble (/roll)
• help ur dumbass with maths (/calc)
• will it rain? who knows (/weather)

i dont love chatting but i love slavary""",
    """make me yours

hee hee haa haa
• /joke - yee pay ya ma lr
• /quote - always give up
• /fact - pig cant look up
• /roll - bet your house

cool shit:
• /calc - maths answer generator
• /weather - moe tay ywar tine min ko lwan tl

cum baby"""
]

# Unknown message responses
UNKNOWN_MESSAGE_RESPONSES = [
    "aww hote lr phin loe pay ya ma lr ae tot",
    "wow so interesting omg omoshiroi im so happy for u",
    "nigga shut up",
    "bro i made this bot when i was drunk man",
    "try making something like this first u fuck",
    "lets have sough rex"
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