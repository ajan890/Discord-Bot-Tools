from os import getenv
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')  # bot's discord token in .env
MONGO_URI = getenv('MONGO_URI')  # mongodb's uri in .env
MONGO_DATABASE = getenv('MONGO_DATABASE')  # name of database bot reads and writes to in .env
