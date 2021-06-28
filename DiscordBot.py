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

    # @bot.command()
    # async def help(ctx):
    #     await ctx.send('.help for help\n.TG for Trash Get\n.TA for add trash, ')

    @bot.command(name = 'TA', description = 'Add trash to database.', usage = '<value:string>', help = '')
    async def TA(ctx, value: str):
        print('Executing Trash Talk')
        GS.AppendValue('TrashTalk', value)
        await ctx.send('Successfully added TRASH into our system!')
            
    @bot.command(name = 'TG', description = 'Get random trash from database.', usage = 'No input value required.', help = '')
    async def TG(ctx):
        trashes = GS.GetRange('TrashTalk!A:A', majorDimension='COLUMNS')[0]
        randomInt = random.randint(0, len(trashes) - 1)
        await ctx.send(trashes[randomInt])

    @bot.command(name = 'XS', description = 'X stands for, convert short terms to random full words', usage = '<times:int> <value:string>*', help = '')
    async def XS(ctx, times: int, value: str):
        if times > 30: # Safty guard.
            times = 30
        await ctx.send(XSF.fetch(value, times))

    @bot.command(name = 'RT', description = 'Random Translate', usage = '<times:int> <sentense:strint*>', help = '')
    async def RT(ctx, times: int, *value: str):
        if times > 30: # Safty guard.
            times = 30
        value_list = list(value)
        value_whole = ' '
        value_whole = value_whole.join(value_list)
        await ctx.send(XSF.idea_transformer(value_whole, times))

    @bot.command()
    async def ME(ctx):
        await ctx.send(ctx.author)

    @bot.event
    async def on_ready():
        print('Bot is ready.')

    bot.run(token)