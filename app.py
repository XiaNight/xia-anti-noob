'''Line Bot API'''
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


'''3rd Party Modules'''
from google_trans_new import google_translator


'''Custome Modules'''
from message import *
from new import *
from Function import *
from XStandForGenerator import *
from EventHandlerModule import *
from PoemGenerator import *
from quickstart import *
from DiscordBot import *


'''Standard Modules'''
from datetime import datetime
import tempfile
import datetime
import asyncio
import random
import json
import time
import sys
import os

'''Discord Bot Modules'''
import discord
from discord.ext import commands


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Secret
handler = WebhookHandler('613e26ffd74fdb430ae58f71af00eedc')

class Data:
    data = {}

    # Add sourceID to data
    def AddGroup(self, sourceID):
        self.data[sourceID] = {}
        self.data[sourceID]['users'] = {}
        '''s
            Kick    Give-Op Commands
        1:  N       N       N           normal user
        2:  Y       N       N           management
        3:  Y       Y       N           owner
        4:  Y       Y       Y           developer
        '''
        self.AddUserToGroup(sourceID, 'Ud631fff6ef744ccc6fce86b5e1d1b4bb', 4) # Add myself to the group as a dev.

        self.DisableDebug(sourceID) # Default debug mode is disabled.

    # Add user to a group/room.
    def AddUserToGroup(self, sourceID, userID, level = 1):
        if sourceID not in self.data:
            self.AddGroup(sourceID)
        self.data[sourceID]['users'][userID] = {'permission': level}
    
    # Get all user IDs in a group/room.
    def GetUsers(self, sourceID):
        return self.data[sourceID]

    # Updates a uses, called when user have actions.
    def UserUpdate(self, sourceID, userID):
        if userID not in self.data[sourceID]['users']:
            self.AddUserToGroup(sourceID, userID)

    # Updates a group, called when group/room have actions.
    def GroupUpdate(self, sourceID):
        if sourceID not in self.data:
            self.AddGroup(sourceID)
    
    # Get a user's permission level in a group/room.
    def GetUserPermmisionLevel(self, sourceID, userID):
        if userID in self.data[sourceID]['users']:
            return self.data[sourceID]['users'][userID]['permission']
        else:
            return 0

    # Enables debug for a group/room.
    def EnableDebug(self, sourceID):
        self.data[sourceID]["debug"] = True

    # Disables debug for a group/room. Default for a group.
    def DisableDebug(self, sourceID):
        self.data[sourceID]["debug"] = False

    def GetDebugMode(self, sourceID):
        return self.data[sourceID]["debug"]

# Monitor all /callback Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

EH = EventHandler()

@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    EH.OnEventGet(event)

@handler.add(MemberLeftEvent)
def handle_member_left(event):
    EH.OnEventGet(event)

# Compute Message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    EH.OnEventGet(event)

@handler.add(FollowEvent)
def handle_follow(event):
    EH.OnEventGet(event)

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    EH.OnEventGet(event)

@handler.add(JoinEvent)
def handle_join(event):
    EH.OnEventGet(event)

@handler.add(LeaveEvent)
def handle_leave():
    EH.OnEventGet(event)

def SendTextMessage(replyToken, text):
    message = TextSendMessage(text=text)
    line_bot_api.reply_message(replyToken, message)

def FromTimestamp(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# return (successfullness, error message)
def SaveSectionJson(sourceID, key, value):

    if not os.path.exists('group_data'):
        os.makedirs('group_data')

    path = 'group_data/' + sourceID + '.json'
    data = None

    if not os.path.exists(path):
        with open(path, 'w') as outfile:
            outfile.write('{}')

    try:
        with open(path) as json_file:
            data = json.load(json_file)
            data[key] = value
    except Exception as e:
        pass
    

    with open(path, 'w') as outfile:
        json.dump(data, outfile)

def ReadSectionJson(sourceID):
    path = 'group_data/' + sourceID + '.json'
    with open(path) as json_file:
        data = json.load(json_file)
        return data

bot = None

def runDiscordBot():
    DiscordBot()

def runLineBot():
    print('running Line bot!')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def CreateBots():
    type = os.getenv("TYPE")
    if(type == 'LINE'):
        runLineBot()
    elif(type == 'DISCORD'):
        runDiscordBot()
    elif(type == None):
        print("Type not set!!!!")

if __name__ == "__main__":
    print('Setting up bot(s)!')
    CreateBots()
    print('All Bot(s) Started!')