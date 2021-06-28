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
    
    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    @bot.description(description = '正在聽 .help')

    @bot.command()
    async def help(ctx, value: str):
        await ctx.send('.help for help\n.TG for Trash Get\n.TA for add trash, ')

    @bot.command(name = 'TA', help = '.TA my_trash', description = 'description', usage = 'usage', brief = 'brief')
    async def TA(ctx, value: str):
        print('Executing Trash Talk')
        GS.AppendValue('TrashTalk', value)
        await ctx.send('Successfully added TRASH into our system!')
            
    @bot.command(name = 'TG', help = '.TG')
    async def TG(ctx):
        trashes = GS.GetRange('TrashTalk!A:A', majorDimension='COLUMNS')[0]
        randomInt = random.randint(0, len(trashes) - 1)
        await ctx.send(trashes[randomInt])

    @bot.command(name = 'TC', help = 'Translate sentence for 5 times: .TC 5 I tea bag no bus')
    async def TC(ctx, times: int, *value: str):
        if times > 30: # Safty guard.
            times = 30
        await ctx.send(XSF.fetch(list(value), times))

    @bot.event
    async def on_ready():
        print('Bot is ready.')

    bot.run(token)