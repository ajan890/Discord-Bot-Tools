# bot.py
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import discord
from discord import app_commands
from constants import TOKEN, MONGO_URI, MONGO_DATABASE
from set_channel_base import set_channel, get_channel

intents = discord.Intents.default()       # defines intents
intents.message_content = True            
client = discord.Client(intents=intents)  # defines client
tree = app_commands.CommandTree(client)   # defines slash command tree


# define commands
@tree.command(name="hello_world", description="Test Application Command")
async def hello_world(interaction):
    await interaction.response.send_message("Hello World!")


# example implementation of set_channel from set_channel_base.py.
# you can have multiple set_xxxxxx_channel commands on discord that just call set_channel with a different channel name
@tree.command(name="set_bot_channel", description="select a channel to send messages to")
async def set_bot_channel(interaction, channel: str):
    await set_channel(interaction, channel, 'bots')


# example implementation of get_channel from set_channel_base.py.
# you can have multiple get_xxxxxx_channel commands on discord that just call get_channel with a different channel name
@tree.command(name="get_bot_channel", description="get channel bot messages are sent to")
async def get_bot_channel(interaction):
    await get_channel(interaction, 'bots')


# TODO: maybe add some protections on this method because it's dangerous
@tree.command(name="delete_server_data", description="delete all server data stored in database")
async def delete_server_data(interaction):
    mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = mongo_client[MONGO_DATABASE]
    collection = db[str(interaction.guild.id)]
    collection.drop()
    await interaction.response.send_message("Server data was deleted from database.")


# run the bot
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
