import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_ready():
    print('Bot is ready.')

bot.run('ODU4NDE1ODA2ODc0NjQ4NjA4.YNd0BA.hKscGsFjELU7HnZiiOizifb7yIE')