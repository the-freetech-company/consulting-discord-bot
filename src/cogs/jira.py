import discord
from discord.ext import commands
import requests
from requests.auth import HTTPBasicAuth

class Jira(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='issue', description='Creates a Jira ticket.')
    async def hello(self, ctx, title, project, epic, *, description):
        await ctx.send('Hello World!')
        
async def setup(bot):
    await bot.add_cog(Jira(bot))