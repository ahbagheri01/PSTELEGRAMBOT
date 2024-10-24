import telebot
from dotenv import load_dotenv
import sys
import os
from LLM import OLLAMA_LLM
from mydatabase import *
from myqueue import ReverseQueue as qu 
# Initialize the Ollama client

# Set up configuration using .env file
def set_configs(env_file):
    load_dotenv(env_file)
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN", "NONE"),
        "use_tts": os.getenv("USE_TTS", "false"),
        "SQL_USER": os.getenv("SQL_USER",""),
        "SQL_PASS": os.getenv("SQL_PASS","")
    }

config = set_configs(sys.argv[1])
os.environ["BOT_TOKEN"] = config["BOT_TOKEN"]
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
db = DB(localhost = "localhost", usr = "psbot", pas = "psbot")
db.print_db()

# Define the PS class for managing the bot and LLM interactions
class PS:
    def __init__(self, config, bot, llm) -> None:
        self.config = config
        self.bot = bot
        self.llm = llm

    def add_task(self, message):
        self.bot.reply_to(message, "Howdy, how are you doing?")

    def chat(self, message):
        res = self.llm.chat(message)
        self.bot.reply_to(message, res)

# Initialize PS class
ollama_client = OLLAMA_LLM(host="localhost", port="11434")
ps = PS(config, bot, ollama_client)




# Define bot commands
@bot.message_handler(commands=['start', 'help', 'add_task'])
def send_welcome(message):
    print(message.text)
    bot.reply_to(message, "Welcome! I'm your bot. How can I assist you today?")

# Echo and pass all other messages to the LLM chat function
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    ps.chat(message)

# Start the bot
print("Bot is ready and polling...")
# ps.chat("Hello")
bot.infinity_polling()
