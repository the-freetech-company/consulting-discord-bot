import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os
import logging
import asyncio

load_dotenv(find_dotenv())
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot = commands.Bot(command_prefix=os.getenv("BOT_PREFIX"), description='Consulting Bot.', case_insensitive=True, intents=discord.Intents.all())


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

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
            print(f'{file[:-3]} cog loaded.')

asyncio.run(main())