from constants import MONGO_URI, MONGO_DATABASE
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


async def set_channel(interaction, channel: str, channel_name: str):
    mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    try:
        db = mongo_client[MONGO_DATABASE]
        collection = db[str(interaction.guild.id)]

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


async def get_channel(interaction, key: str):
    mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = mongo_client[MONGO_DATABASE]
    collection = db[str(interaction.guild.id)]
    query_result = collection.find_one({"key": key})

    if query_result:
        channel = query_result.get("channel_id")
        await interaction.response.send_message(key + " is currently set to " + channel)
    else:
        await interaction.response.send_message("Entry " + key + " was not found in database.")
    mongo_client.close()
    return

