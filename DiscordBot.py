'''Line Bot API'''
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

'''Google Modules'''
from google_trans_new import google_translator

'''Custome Modules'''
from message import *
from new import *
from Function import *
from XStandForGenerator import *
from EventHandlerModule import *
from quickstart import *

'''Standard Modules'''
from datetime import datetime
import tempfile
import datetime
import random
import json
import time
import sys
import os

'''Discord Bot Modules'''
import discord
from discord.ext import commands


XSF = XStandFor()
GS = GoogldSheet()

class DiscordBot:

    bot = commands.Bot(command_prefix='>')

    def __init__(self):
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        self.bot.run(self.token)

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    @bot.event
    async def on_ready():
        print('Bot is ready.')