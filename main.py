import discord
import os
import asyncio
from discord.ui import Button, View, Select
from discord.ext import commands
from discord.utils import get
import collections
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ["TOKEN"]
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_app_command_completion(interaction, command):
  print(f'{command.name} was run by {interaction.user}')

@bot.tree.command(name='ping', description='ping pong <3')
async def ping(interaction: discord.Interaction):
  latency = bot.latency * 1000  # Convert to milliseconds
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
    for filename in os.listdir("walmart-invite-tracker/cogs"):
      if filename.endswith(".py"):
        try:
          await bot.load_extension(f"cogs.{filename[:-3]}")
          print(f"{filename} was loaded.")
        except Exception as e:
          print(f"Oh no! {e}")
          print(f"{filename} could not be loaded.")
    await bot.change_presence(activity=discord.Activity(
      type=discord.ActivityType.listening,
      name="invites | by Callan v0.1"))
    synced = await bot.tree.sync()
    
    print(f'Synced {len(synced)} command(s)')
  except Exception as e:
    print(e)

bot.run(TOKEN)