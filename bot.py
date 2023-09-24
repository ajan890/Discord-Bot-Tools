# bot.py
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # bot's discord token in .env
MONGO_URI = os.getenv('MONGO_URI')  # mongodb's uri in .env
MONGO_DATABASE = os.getenv('MONGO_DATABASE')  # name of database bot reads and writes to in .env
MONGO_BOT_COLLECTION = os.getenv('MONGO_BOT_COLLECTION')  # name of collection bot reads and writes to goes in .env

intents = discord.Intents.default()       # defines intents
intents.message_content = True            
client = discord.Client(intents=intents)  # defines client
tree = app_commands.CommandTree(client)   # defines slash command tree


# define commands
@tree.command(name="hello_world", description="Test Application Command")
async def hello_world(interaction):
    await interaction.response.send_message("Hello World!")


# set a channel for a bot to send messages; store channel id on MongoDB
@tree.command(name="set_channel", description="select a channel to send messages to")
async def set_channel(interaction, channel: str):
    """
        channel_name is CONSTANT; this is key written to the database.
        the value of this variable should be changed to represent what the channel is used for.
        e.g., "news_channel", if the bot posts news in that channel.
    """
    channel_name = "channel_name"
    mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    try:
        db = mongo_client[MONGO_DATABASE]
        collection = db[MONGO_BOT_COLLECTION]
        data_to_insert = {
            "key": channel_name,
            "channel_id": channel
        }

        # check if channel_name key already exists in database
        if collection.find_one({"key": data_to_insert["key"]}):
            # if found, update the value
            update_query = {"key": data_to_insert["key"]}
            collection.update_one(update_query, {'$set': data_to_insert})
            mongo_client.close()
            await interaction.response.send_message("Overwrote set channel to: " + channel + "!")
            return
        else:
            # if not found, create new key-value pair
            collection.insert_one(data_to_insert)
            mongo_client.close()
            await interaction.response.send_message("Successfully set channel to: " + channel + "!")
            return

    except Exception as e:
        mongo_client.close()
        print(e)
        await interaction.response.send_message("Error in writing channel to MongoDB")


# get a channel from MongoDB
@tree.command(name="get_channel", description="get channel bot messages are sent to")
async def get_channel(interaction, key: str):
    """
        the parameter 'key' is the key of the channel you want to search.
        your search should be the same as the variable 'channel_name' in the set method.
    """
    mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = mongo_client[MONGO_DATABASE]
    collection = db[MONGO_BOT_COLLECTION]
    query_result = collection.find_one({"key": key})

    if query_result:
        channel = query_result.get("channel_id")
        await interaction.response.send_message(key + " is currently set to " + channel)
    else:
        await interaction.response.send_message("Entry " + key + " was not found in database.")
    mongo_client.close()
    return


# run the bot
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
