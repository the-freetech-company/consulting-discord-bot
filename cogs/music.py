import wavelink
import discord
from discord.ext import commands
import asyncio
import os
import logging

class Music(commands.Cog):
    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='lavalink',
                                            port=2333,
                                            password='youshallnotpass')
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.connect_nodes())

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')