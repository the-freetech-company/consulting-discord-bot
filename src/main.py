import discord
from discord.ext import commands
import asyncio
import logging
import os
import yaml
from pymongo import MongoClient
import datetime
import http.client as httplib
import json
# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='/home/src/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# load_dotenv(find_dotenv())
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot = commands.Bot(command_prefix=os.getenv("BOT_PREFIX"), description='Consulting Bot.', case_insensitive=True, intents=discord.Intents.all())

#MongoDB
mg = MongoClient('mongodb', 27017,
                username=os.environ['MONGO_USER'],
                password=os.environ['MONGO_PASSWORD'])

@bot.event
async def on_connect():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    await load()
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
async def main():
    token = os.getenv("DISCORD_SECRET")
    await bot.start(token)
@bot.event
async def on_guild_join(guild):
    try:
        print(guild.name)
        collection = mg['discord']['guilds']
        collection.insert_one({
            'guild_id': guild.id,
            'guild_name': guild.name,
            'guild_owner': guild.owner.id,
            'guild_owner_name': guild.owner.name,
            'guild_member_count': guild.member_count,
            'guild_created_at': guild.created_at,
            'bot_join_date': datetime.datetime.utcnow(),
            'has_api_key': False, 'google_api_key': None,
            'music_channel_id': None,
            'play_tracking_message_id': None,
            'autoplay_max_duration': None,
            'dj_lock': False,
            'dj_role_id': None,
            'dj_ids': [],
            'autoplay': False,
            
            })
    except:
        print("Guild already in database.")
    #find my server and my channel and send a message to it
    for guilds in bot.guilds:
        if guilds.id == 1058867981268041850:
            for channel in guilds.channels:
                if channel.id == 1058940782238777345:
                    await channel.send(f"Joined {guild.name}\nOwner: {guild.owner.name}#{guild.owner.discriminator}\nMember Count: {guild.member_count}\nCreated at: {guild.created_at}\nBot Join Date: {datetime.datetime.utcnow()}\n------------------------------------------------")
@bot.event
async def on_guild_remove(guild):
    try:
        print(guild.name)
        collection = mg['discord']['guilds']
        collection.delete_one({'guild_id': guild.id})
    except:
        print("Guild not in database.")
    #find my server and my channel and send a message to it
    for guilds in bot.guilds:
        if guilds.id == 1058867981268041850:
            for channel in guilds.channels:
                if channel.id == 1058940782238777345:
                    await channel.send(f"Left {guild.name}\nOwner: {guild.owner.name}#{guild.owner.discriminator}\nMember Count: {guild.member_count}\nCreated at: {guild.created_at}\nBot Join Date: {datetime.datetime.utcnow()}\n------------------------------------------------")
@bot.event
async def on_guild_update(before, after):
    try:
        collection = mg['discord']['guilds']
        collection.update_one({'guild_id': before.id}, {'$set': {'guild_name': after.name}, '$set': {'guild_owner': after.owner.id}, '$set': {'guild_owner_name': after.owner.name}, '$set': {'guild_member_count': after.member_count}, '$set': {'guild_created_at': after.created_at}})
    except:
        print("Guild not in database.")

@bot.command()
async def send(ctx, *, message):
    if ctx.author.id == 238047264839303179:
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == "general" or channel.name == "𝙂𝙀𝙉𝙀𝙍𝘼𝙇":
                    await channel.send(message)
    else:
        await ctx.send("You do not have permission to use this command.")

async def load():
    for file in os.listdir('home/src/cogs'):
        if file.endswith('.py'):
            print(f'Loading {file[:-3]} cog.')
            await bot.load_extension(f'cogs.{file[:-3]}')
            print(f'{file[:-3]} cog loaded.')

asyncio.run(main())