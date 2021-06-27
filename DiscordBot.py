'''Google Modules'''
from google_trans_new import google_translator

'''Custome Modules'''
from Function import *
from XStandForGenerator import *
from quickstart import *

'''Standard Modules'''
import os

'''Discord Bot Modules'''
import discord
from discord.ext import commands

def DiscordBot():

    bot = commands.Bot(command_prefix='.')
    XSF = XStandFor()
    GS = GoogldSheet()

    print('running discord bot!')
    token = os.getenv("DISCORD_BOT_TOKEN")
    bot.run(token)

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    @bot.command()
    async def TA(ctx, value: str):
        print('Executing Trash Talk')
        GS.AppendValue('TrashTalk', value)
        await ctx.send('Successfully added TRASH into our system!')
            
    @bot.command()
    async def TG(ctx):
        trashes = GS.GetRange('TrashTalk!A:A', majorDimension='COLUMNS')[0]
        randomInt = random.randint(0, len(trashes) - 1)
        await ctx.send(trashes[randomInt])
        
    @bot.event
    async def on_ready():
        print('Bot is ready.')