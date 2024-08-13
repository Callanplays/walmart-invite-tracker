import discord
import os
from discord.ext import tasks, commands
from discord.utils import get
import json
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

invite_data_file = 'invite_data.json' 

if not os.path.exists(invite_data_file):
    with open(invite_data_file, 'w') as f:
        json.dump({}, f)

async def update_invite_data(guild: discord.Guild):
    invite_data = {}
    invites = await guild.invites()
    for invite in invites:
        if invite.inviter.id not in invite_data:
            invite_data[invite.inviter.id] = {
                'user_id': invite.inviter.id,
                'invites_count': invite.uses
            }
        else:
            invite_data[invite.inviter.id]['invites_count'] += invite.uses
    with open(invite_data_file, 'w') as f:
        json.dump(invite_data, f, indent=4)

async def fetch_invite_data():
    with open(invite_data_file, 'r') as f:
        invite_data = json.load(f)
    return invite_data

@bot.tree.command(name='invites', description='Display users with an active invite link and their invite count')
async def invited_count(interaction: discord.Interaction):
  await interaction.response.send_message("Fetching invited people data...")
  guild = interaction.guild
  await update_invite_data(guild)
  invite_data = await fetch_invite_data()
  embed = discord.Embed(title="Invited People Count", color=discord.Color.green())
  for user_id, data in invite_data.items():
      user = bot.get_user(int(user_id))
      if user:
          embed.add_field(name=f"{user.name}", value=f"Invites Count: {data['invites_count']}", inline=False)
      else:
          embed.add_field(name=f"User ID: {user_id}", value=f"Invites Count: {data['invites_count']}", inline=False)
  
  await interaction.edit_original_response(embed=embed)

@tasks.loop(minutes=1)
async def update_invite_roles():
  guild = bot.get_guild(940082444059693107)
  await update_invite_data(guild)
  invite_data = await fetch_invite_data()
  for user_id, data in invite_data.items():
    member = guild.get_member(int(user_id))
    if member:
      invites_count = data['invites_count']
      if invites_count >= 1:
        role = discord.utils.get(guild.roles, id=1273004175873151058)  
        if role not in member.roles:
          await member.add_roles(role)
      if invites_count >= 2:
        role = discord.utils.get(guild.roles, id=1273004199373832202)  
        if role not in member.roles:
          await member.add_roles(role)
      if invites_count >= 3:
        role = discord.utils.get(guild.roles, id=1262571225872470087)  
        if role not in member.roles:
          await member.add_roles(role)
      if invites_count >= 5:
        role = discord.utils.get(guild.roles, id=1262571248689479752)
        if role not in member.roles:
          await member.add_roles(role)
      if invites_count >= 20:
        role = discord.utils.get(guild.roles, id=1263916721790652559)  
        if role not in member.roles:
          await member.add_roles(role)

@bot.event
async def on_app_command_completion(interaction, command):
  print(f'{command.name} was run by {interaction.user}')

@bot.tree.command(name='ping', description='ping pong <3')
async def ping(interaction: discord.Interaction):
  latency = bot.latency * 1000 
  await interaction.response.send_message(
      f"Pong! {interaction.user.mention} {latency:.2f}ms latency!")

@bot.tree.command(name='about', description='About the bot')
async def about(interaction: discord.Interaction):
  embed = discord.Embed(title="Walmart Invite Tracker", description="A bot to track invites in your server", color=discord.Color.green())
  embed.add_field(name="About:", value="Walmart Invite Tracker is a bot coded by Callan for Legendary Games & chinkn. This bot's only purpose is to help server owners track invites in their server for free.", inline=False)
  embed.add_field(name="Features:", value="• Track invites\n• Assign roles based on invites\n• Invite leaderboard", inline=False)
  embed.set_footer(text="Callan | v0.1")
  await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
  try:
    await bot.change_presence(activity=discord.Activity(
      type=discord.ActivityType.listening,
      name="invites | by Callan v0.1"))
    synced = await bot.tree.sync()
    update_invite_roles.start()
    print('Invite Loop Started!')
    
    print(f'Synced {len(synced)} command(s)')
  except Exception as e:
    print(e)

bot.run("TOKEN REDACTED")