import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os
import logging
import asyncio

load_dotenv(find_dotenv())
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot = commands.Bot(command_prefix=os.getenv("BOT_PREFIX"), description='Consulting Bot.', case_insensitive=True, intents=discord.Intents.all())


@bot.event
async def on_connect():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


#Login and connect
async def main():
    token = os.getenv("bot_token")
    await bot.start(token)

asyncio.run(main())