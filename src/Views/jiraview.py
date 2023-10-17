from discord import Embed, SelectOption, SelectMenu, Button, ActionRow
import asyncio
from helpers.jiraHelpers import updateIssueStatus
import discord
class JiraView(discord.ui.View):
    def __init__(self, loop):
        self.loop = loop  # Store the loop for future use
        self.__stopped = self.loop.create_future()
        self.value = None
        super().__init__()

    @discord.ui.button(label='Acknowledge', style=discord.ButtonStyle.primary, row=0)
    async def acknowledge(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        original_embed = interaction.message.embeds[0]
        #Add a field for users working on this issue. if it exists already, append the user to the list
        if len(original_embed.fields) >= 7:
            original_embed.set_field_at(6, name='Contributers: ', value=f'{original_embed.fields[6].value}, {user.mention}', inline=True)
        else:
            original_embed.add_field(name='Contributers: ', value=user.mention, inline=True)
        await interaction.message.edit(embed=original_embed)
        await interaction.response.send_message('Acknowledged Task', ephemeral=True)

    @discord.ui.button(label='Mark Complete', style=discord.ButtonStyle.success, row=0)
    async def markComplete(self, interaction: discord.Interaction, button: discord.ui.Button):
        original_embed = interaction.message.embeds[0]
        original_embed.set_field_at(2, name='Status', value='Done', inline=True)
        if updateIssueStatus(original_embed.footer.text, 'Done'):
            key = original_embed.footer.text
            summary = original_embed.title
            await interaction.message.edit(embed=original_embed)
            await interaction.response.send_message(f'Marked task [{summary}] [{key}] as Complete', ephemeral=True)
            self.stop()
            self.clear_items()
            await interaction.message.delete()
            embed = Embed(
                title=f"Completed - {summary}",
                description=f"Marked complete by {interaction.user.mention}",
                color=0x0d00ff,
                url=f"https://the-freetech-company.atlassian.net/browse/{key}"
            )
            embed.add_field(name="Reporter", value=original_embed.fields[4].value, inline=True)
            await interaction.channel.send(embed=embed)
        else:
            await interaction.response.send_message('Failed to mark task as complete', ephemeral=True)


    @discord.ui.button(label='Send to..', style=discord.ButtonStyle.secondary, row=0)
    async def SendTo(self, interaction: discord.Interaction, button: discord.ui.Button):        
        select = JiraSelect(interaction=interaction)
        self.clear_items()
        self.add_item(select)
        await interaction.response.send_message('Where would you like to move this task', view=self)

class JiraSelect(discord.ui.Select):
    def __init__(self, interaction: discord.Interaction = None):
        self.interaction = interaction
        options = [
            discord.SelectOption(label='To Do', description='Send task to To Do'),
            discord.SelectOption(label='In Progress', description='Send task to In Progress'),
        ]
        super().__init__(placeholder='Choose Where to send the task to.', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        original_embed = self.interaction.message.embeds[0]
        key = original_embed.footer.text
        if updateIssueStatus(key, self.values[0]):
            original_embed.set_field_at(2, name='Status', value=self.values[0], inline=True)
            await interaction.response.send_message(f'Task sent to {self.values[0]}')
        else:
            await interaction.response.send_message(f'Failed to send task to {self.values[0]}')
        