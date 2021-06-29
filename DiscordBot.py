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

    admins = [556399119787229202, 456714424573493260]

    def CheckPermission(id:int):
        if id in admins:
            return True
        return False
    
    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    # @bot.command()
    # async def help(ctx):
    #     await ctx.send('.help for help\n.TG for Trash Get\n.TA for add trash, ')

    @bot.command(name = 'TA', description = 'Add trash to database.', usage = '', help = '<value:string>')
    async def TA(ctx, value: str):
        if not CheckPermission(ctx.author.id):
            await ctx.send('You have no permission to do that.')
            return
        print('Executing Trash Talk')
        GS.AppendValue('TrashTalk', value)
        await ctx.send('Successfully added TRASH into our system!')
            
    @bot.command(name = 'TG', description = 'Get random trash from database.', usage = 'No input value required.', help = '')
    async def TG(ctx):
        if not CheckPermission(ctx.author.id):
            await ctx.send('You have no permission to do that.')
            return
        trashes = GS.GetRange('TrashTalk!A:A', majorDimension='COLUMNS')[0]
        randomInt = random.randint(0, len(trashes) - 1)
        await ctx.send(trashes[randomInt])

    @bot.command(name = 'XS', description = 'X stands for, convert short terms to random full words', usage = '', help = '<times:int> <value:string>')
    async def XS(ctx, times: int, value: str):
        if len(value) > 7:
            await ctx.send('Value too long, would cause lag.')
            return
        if times > 30: # Safty guard.
            times = 30
        print('fething: ', value, times)
        fetch = XSF.fetch(value, times)
        print('fetched: ', fetch)
        await ctx.send(fetch)

    @bot.command(name = 'RT', description = 'Random Translate', usage = '', help = '<times:int> <sentense:string*>')
    async def RT(ctx, times: int, *value: str):
        if times > 30: # Safty guard.
            times = 30
        value_list = list(value)
        value_whole = ' '
        value_whole = value_whole.join(value_list)
        print('transforming: ', value_whole)
        transformed = XSF.idea_transformer(value_whole, times)
        print('transformed: ', transformed)
        await ctx.send(transformed)

    @bot.command()
    async def ME(ctx):
        await ctx.send(ctx.author.id)

    @bot.command()
    async def CTX(ctx, value: str):
        if not CheckPermission(ctx.author.id):
            await ctx.send('You have no permission to do that.')
            return
        exec('ctx.send(ctx.{})')

    @bot.event
    async def on_ready():
        print('Bot is ready.')

    bot.run(token)