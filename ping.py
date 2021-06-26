import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='>')
token = os.getenv("DISCORD_BOT_TOKEN")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_ready():
    print('Bot is ready.')

bot.run(token)