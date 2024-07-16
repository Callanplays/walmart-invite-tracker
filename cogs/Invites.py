import discord
from discord.ext import tasks, commands
import json
import os

class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.invite_data_file = 'invite_data.json'  # JSON file to store invite data
        self.update_invite_roles.start() # Start the task loop
        print('Invite Updating Loop started successfully')
        # Initialize invite data file if not exists
        if not os.path.exists(self.invite_data_file):
            with open(self.invite_data_file, 'w') as f:
                json.dump({}, f)

    async def update_invite_data(self, guild: discord.Guild):
        invite_data = {}
        # Fetch invites and update invite_data
        invites = await guild.invites()
        for invite in invites:
            if invite.inviter.id not in invite_data:
                invite_data[invite.inviter.id] = {
                    'user_id': invite.inviter.id,
                    'invites_count': invite.uses
                }
            else:
                invite_data[invite.inviter.id]['invites_count'] += invite.uses
        
        # Write updated data to JSON file
        with open(self.invite_data_file, 'w') as f:
            json.dump(invite_data, f, indent=4)

    async def fetch_invite_data(self):
        # Read invite data from JSON file
        with open(self.invite_data_file, 'r') as f:
            invite_data = json.load(f)
        return invite_data

    @discord.app_commands.command(name='invites', description='Display invited users and their invite count')
    async def invited_count(self, interaction: discord.Interaction):
        await interaction.response.send_message("Fetching invited people data...")
        guild = interaction.guild
        await self.update_invite_data(guild)
        invite_data = await self.fetch_invite_data()

        # Create an embed for better presentation
        embed = discord.Embed(title="Invited People Count", color=discord.Color.green())
        for user_id, data in invite_data.items():
            user = self.bot.get_user(int(user_id))
            if user:
                embed.add_field(name=f"{user.name}", value=f"Invites Count: {data['invites_count']}", inline=False)
            else:
                embed.add_field(name=f"User ID: {user_id}", value=f"Invites Count: {data['invites_count']}", inline=False)
        
        await interaction.edit_original_response(embed=embed)

    @tasks.loop(minutes=1)
    async def update_invite_roles(self):
        guild = self.bot.get_guild(940082444059693107)
        await self.update_invite_data(guild)
        invite_data = await self.fetch_invite_data()

        for user_id, data in invite_data.items():
            member = guild.get_member(int(user_id))
            if member:
                invites_count = data['invites_count']
                if invites_count >= 3:
                    role = discord.utils.get(guild.roles, id=1262571225872470087)  # Replace ROLE_ID_3 with the ID of the "3 invites" role
                    if role not in member.roles:
                        await member.add_roles(role)
                if invites_count >= 5:
                    role = discord.utils.get(guild.roles, id=1262571248689479752)  # Replace ROLE_ID_5 with the ID of the "5 invites" role
                    if role not in member.roles:
                        await member.add_roles(role)
   

async def setup(bot):
    await bot.add_cog(Invites(bot))
