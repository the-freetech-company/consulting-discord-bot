import re
import discord
from discord.ext import commands


class dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='dm', description='Starts a DM with another user.')
    async def startDM(self, ctx, user: discord.User):
        guild = ctx.guild
        channel_name_raw = f'{ctx.author.name}-{user.name}'
        channel_name = re.sub(r"[^a-zA-Z0-9\-_]+", '', channel_name_raw)
        category = discord.utils.get(guild.categories, name='Direct Messages')
        overwrites =  {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True)
        }
        
        for channel in category.text_channels:
            if channel.name == channel_name:
                await ctx.send('You already have a DM with this user.')
                return
        await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)

async def setup(bot):
    await bot.add_cog(dm(bot))