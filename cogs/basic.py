import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='hello_world', description='Says hello.')
    async def hello(self, ctx):
        await ctx.send('Hello World!')
        
async def setup(bot):
    await bot.add_cog(Basic(bot))