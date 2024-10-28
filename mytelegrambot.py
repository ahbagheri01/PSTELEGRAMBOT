import telebot
from dotenv import load_dotenv
import sys
import os
from utils.LLM import OLLAMA_LLM
from utils.mydatabase import *
from utils.myqueue import ReverseQueue as qu 
# Initialize the Ollama client

# Set up configuration using .env file
def set_configs(env_file):
    load_dotenv(env_file)
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN", "NONE"),
        "use_tts": os.getenv("USE_TTS", "false"),
        "SQL_USER": os.getenv("SQL_USER","psbot"),
        "SQL_PASS": os.getenv("SQL_PASS","psbot2024@")
    }

config = set_configs(sys.argv[1])
os.environ["BOT_TOKEN"] = config["BOT_TOKEN"]
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
db = DB(host = "localhost", user = config["SQL_USER"], password = config["SQL_PASS"], database = "psbot")
db.create_tables()
db.print_db()

# Define the PS class for managing the bot and LLM interactions
class PS:
    def __init__(self, config, bot, llm) -> None:
        self.config = config
        self.bot = bot
        self.llm = llm
        self.user_id = {}

    def add_task(self, message):
        self.bot.reply_to(message, "Howdy, how are you doing?")

    def chat(self, message):
        res = self.llm.chat(message)
        m = res
        if len(m) > 2048:
            for x in range(0, len(m), 2048):
                self.bot.reply_to(message, text=m[x:x+2048])
        else:
            self.bot.reply_to(message, text=m)
    
    def add_task(self, message):
        text = message.text[9:]
        print(text)
        res = self.llm.prompt(text)
        print(res)
        self.bot.reply_to(message, res)


        


# Initialize PS class
ollama_client = OLLAMA_LLM(host="localhost", port="11434")
ps = PS(config, bot, ollama_client)




# Define bot commands
@bot.message_handler(commands=['start', 'help', 'add_task'])
def send_welcome(message):
    if not db.user_exists_by_telegram_id(message.from_user.id):
        db.insert_user(message.from_user.username, message.from_user.id)
    if message.text.startswith("/add_task"):
        res = ps.add_task(message)        
    else:
        bot.reply_to(message, "Welcome! I'm your bot. How can I assist you today?")

# Echo and pass all other messages to the LLM chat function
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    if not db.user_exists_by_telegram_id(message.from_user.id):
        db.insert_user(message.from_user.username, message.from_user.id)
    ps.chat(message)

# Start the bot
print("Bot is ready and polling...")
# ps.chat("Hello")
bot.infinity_polling()
