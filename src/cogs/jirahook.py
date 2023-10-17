from discord.ext import commands
from flask import Flask, request
import threading
import asyncio
from discord import Embed, SelectOption, SelectMenu, Button, ActionRow
import datetime
import requests
from requests.auth import HTTPBasicAuth
import discord
import json
from Views.jiraview import JiraView
app = Flask(__name__)

class JiraHook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.flask_thread = threading.Thread(target=self.run_flask)
        self.flask_thread.start()
        self.users = {
            "Chase Letourneau": "238047264839303179",
            "Jacob Zorniak": "1124459897216585881",
            "Erin Thomas": "1158639238477262919",
            "Adam Siwiec": "638745610001842240",
            "Sachin Pathak": "1019010782974988309"
        }
    def run_flask(self):
        @app.route('/jira-webhook', methods=['POST'])
        def jira_webhook():
            data = json.loads(request.data)
            event_type_name = data.get('issue_event_type_name', 'Unknown')
            print(f"Received webhook: {data}")  # Print the entire webhook payload


            ########################################################################
            # POSTS WHEN AN ISSUE IS ASSIGNED TO SOMEBODY, OR ASSIGNMENT IS CHANGED #
            ########################################################################
            changelog = data.get('changelog', {}).get('items', [])

            assignee_changed = False
            for item in changelog:
                if item['field'] == "assignee":
                    assignee_changed = True
                    break

            if assignee_changed:
                
                issue_data = data.get('issue', {})
                fields = issue_data.get('fields', {}) if issue_data else {}
                parent_data = issue_data.get('parent', {})

                fields_data = parent_data.get('fields', {})
                summary_data = fields_data.get('summary', 'N/A')

                issue_avatar = issue_data.get('fields', {}).get('assignee', {}).get('avatarUrls', {}).get('48x48', 'N/A')

                issue_key = issue_data.get('key', 'N/A') if issue_data else 'N/A'
                issue_summary = fields.get('summary', 'N/A') if fields else 'N/A'
                issue_description = fields.get('description', 'N/A') if fields else 'N/A'
                issue_priority = fields.get('priority', {}).get('name', 'N/A') if fields.get('priority') else 'N/A'
                issue_status = fields.get('status', {}).get('name', 'N/A') if fields.get('status') else 'N/A'
                issue_due_date = fields.get('duedate', 'N/A') if fields else 'N/A'
                issue_assignee = fields.get('assignee', {}).get('displayName', 'N/A') if fields.get('assignee') else 'N/A'
                issue_creator = fields.get('creator', {}).get('displayName', 'N/A') if fields.get('creator') else 'N/A'
                issue_project = fields.get('project', {}).get('name', 'N/A') if fields.get('project') else 'N/A'
                issue_epic = issue_data.get('fields', {}).get('parent', {}).get('fields', {}).get('summary', 'N/A')
                issue_reporter = fields.get('reporter', {}).get('displayName', 'N/A') if fields.get('reporter') else 'N/A'

                if issue_reporter in self.users:
                    issue_reporter = self.bot.get_user(int(self.users[issue_reporter])).mention
                status_changed_to = "N/A"
                if 'changelog' in data:
                    for item in data['changelog']['items']:
                        if item['field'] == "status":
                            status_changed_to = item['toString']

                channel = self.bot.get_channel(1163512379972264090)  # Replace with your channel ID

                if channel:
                    color = 0xFFFFFF  # Default color

                    if "issue_created" in event_type_name:
                        color = 0x00ff00
                    elif "issue_deleted" in event_type_name:
                        color = 0xff0000
                    elif "issue_updated" in event_type_name and issue_status == "Completed":
                        color = 0x0000ff

                    embed = Embed(
                            title=issue_summary,
                            description=f"**Issued by**: {issue_creator} \n**Project:** {issue_project}\n**Epic:** {issue_epic}\n**Key:** {issue_key}",
                            color=0x0d00ff,
                            url=f"https://the-freetech-company.atlassian.net/browse/{issue_key}"
                        )
                    embed.set_thumbnail(url=issue_avatar)
                    embed.add_field(name="Due by", value=issue_due_date, inline=True)
                    if issue_assignee in self.users:
                        user = self.bot.get_user(int(self.users[issue_assignee]))
                        embed.add_field(name="Assigned To", value=f"{user.mention}", inline=True)
                    else:
                        embed.add_field(name="Assigned To", value=issue_assignee, inline=True)
                    embed.add_field(name="Status", value=issue_status, inline=True)
                    embed.add_field(name="Priority", value=issue_priority, inline=True)
                    embed.add_field(name="Reporter", value=issue_reporter, inline=True)
                    embed.add_field(name="Description", value=issue_description, inline=False)
                    embed.set_footer(text=issue_key)
                    embed.timestamp = datetime.datetime.utcnow()
                    
                    ######################################################
                    #  END --------- POSTS WHEN AN ISSUE IS ASSIGNED TO SOMEBODY, OR ASSIGNMENT IS CHANGED #
                    ######################################################
            event_loop = self.bot.loop
            async def send_embed():
                view = JiraView(event_loop)
                await channel.send(f"You have been assigned a task {user.mention}.", embed=embed, view=view),
            asyncio.run_coroutine_threadsafe(
                send_embed(),
                self.bot.loop
            )

            return 'OK', 200

        app.run(port=5000)

    @commands.command(name='hello_jira', description='Says hello.')
    async def hello(self, ctx):
        await ctx.send('Hello Worlddd!')
    



async def setup(bot):
    await bot.add_cog(JiraHook(bot))
