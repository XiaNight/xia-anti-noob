import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('ODU4NDE1ODA2ODc0NjQ4NjA4.YNd0BA.uNSXveUm98w5uOEbtuYFaNBbps4')