# heroku login
# heroku git:remote -a xia-anti-noob
# git init

# git add .
# git commit -am'ok'
# git push heroku master

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
from quickstart import *


'''Standard Modules'''
import tempfile
import datetime
import random
import json
import time
import sys
import os

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('cwBEnoA7OI09xMRwZj2JGgVLTiCY8h2fraLjFmwDMHx+JXKuewOBE5eh6xUCIt+1VQOoPVmUlow5xkZDY1oPY7yYPFcd9rN2JqtwCGH3X9Q59VnjPuC4dOqgvXpfW9P3JOgAjgkg+kVFh8yl4wEBJAdB04t89/1O/w1cDnyilFU=')
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

class EventHandler:

    data = Data()

    #Event
    event = None

    sourceID = None
    replyToken = None
    replyTokenUsed = False

    debugMode = False

    def __init__(self):
        pass

    def OnEventGet(self, event):
        self.event = event
        
        try:
            self.GetSource() # Get event source.
            self.data.GroupUpdate(self.sourceID) # Update group statistics.
            self.replyToken = self.event.reply_token
            self.replyTokenUsed = False

            debugMode = self.data.GetDebugMode(self.sourceID)
            if event.type == 'message':
                self.MessageEvent()
            if event.type == 'memberJoined':
                self.MemberJoinEvent()
            if event.type == 'memberLeft':
                self.MemberLeaveEvent()
            if event.type == 'join':
                self.JoinEvent()

            if self.debugMode:
                self.Debug() # Run debug if active.

            self.Default() # Defaule operation for a event.

        except Exception as e: # Error handler
            print(sys.exc_info())
            self.Print(str(e))

    # Return true if user's permission level is reached the required.
    def CheckPermissionLevel(self, userID, permRequire, logWarning = True):
        userPerm = self.data.GetUserPermmisionLevel(self.sourceID, userID)
        if userPerm >= permRequire:
            return True
        else:
            if logWarning:
                self.Print("Permission denied, you have no permission to do this action.")
                self.Print("Your level: " + str(userPerm) + " Required level: " + str(permRequire))
            return False
    
    def CheckKeyWord(self, keyword, userCmd, permission = 1, logWarning = True):
        if userCmd == keyword:
            if self.CheckPermissionLevel(self.GetUserID(), permission, logWarning=logWarning):
                return True
        return False

    # When user/group/room sends a message.
    def MessageEvent(self):
        self.data.UserUpdate(self.sourceID, self.GetUserID())
        perm = self.data.GetUserPermmisionLevel(self.sourceID, self.GetUserID())

        userIndex = None

        if self.event.source.type == 'user':
            # Add user to Users if user not exist.
            usernames = GS.GetSheet('Users!A:A', majorDimension='COLUMNS')[0] # Get all usernames in sheet 'Users'.
            if self.GetUserID() not in usernames:
                GS.AppendValue('Users', [self.GetUserID(), 1, self.event.timestamp])
                userIndex = len(usernames)
            else:
                userIndex = usernames.index(self.GetUserID())
        else:
            # Create sheet if not exist
            if not GS.CheckIfSheetExists(self.sourceID): # If group id were not in the list
                GS.AddSheet(self.sourceID)

            # Add user to group if user not exist.
            usernames = GS.GetSheet(self.sourceID + '!A:A', majorDimension='COLUMNS')[0] # Get all usernames in the group.
            if self.GetUserID() not in usernames: # If username were not in the list.
                GS.AppendValue(self.sourceID, [self.GetUserID(), 1, self.event.timestamp])
                userIndex = len(usernames)
            else:
                userIndex = usernames.index(self.GetUserID())

        msg = self.event.message.text
        if msg[0] == '#': # Raw python code executing.
            if self.CheckPermissionLevel(self.GetUserID(), 4, logWarning=False): # Requires developer level to execute.
                exec(compile(msg[1:],"-","exec"))
        elif msg[0] == '$': # Commands here.
            command = msg[1:]
            if self.CheckKeyWord('help', command, 2):
                self.Print('$EnableDebug to enable debug\n$DisableDebug to disable debug\nstart with # to execute raw python code.')
            if self.CheckKeyWord('EnableDebug', command, 4):
                self.EnableDebug()
            if self.CheckKeyWord('DisableDebug', command, 4):
                self.DisableDebug()
        elif msg[0] == '%':
            splits = msg[1:].split(' ')
            if len(splits) < 2:
                self.Print('Not enough arguments')
                return
            userInput = splits[0]
            times = splits[1]
            times = int(times)
            self.Print(XSF.fetch(userInput, times))
            # output = XSF.fetch(userInput, times)
            # for t in output:
            #     self.Print(t)
            #     pass
            pass

    # Gets the source of the event and store it.
    def GetSource(self):
        if self.event.source.type == 'user':
            self.sourceID = self.event.source.user_id
        elif self.event.source.type == 'group':
            self.sourceID = self.event.source.group_id
        elif self.event.source.type == 'room':
            self.sourceID = self.event.source.room_id

    # Get user ID if there is one.
    def GetUserID(self):
        try:
            return self.event.source.user_id
        except:
            print('No user_id in this event')
            return None

    # When member joined a group/room
    def MemberJoinEvent(self):
        self.Print('User Joined')

        self.data.AddUserToGroup(self.sourceID, self.GetUserID(), 1)

        userProfile = self.event.joined.members[0]

        self.Print('User ID: ' + userProfile.user_id)

        profile = line_bot_api.get_profile(userProfile.user_id)

        self.Print('User Display Name: ' + profile.display_name)
        self.Print('User ID: ' + profile.user_id)
        self.Print('User Picture URL: ' + profile.picture_url)
        self.Print('User Status Message: ' + profile.status_message)

        pass

    # Whem member leaves a group/room
    def MemberLeaveEvent(self):
        self.Print('User Left')

        userProfile = self.event.left.members[0]

        self.Print('User ID: ' + userProfile.user_id)

        profile = line_bot_api.get_profile(userProfile.user_id)
        
        recallMessage = 'You have left the group: rejoin the group by entering this website: https://line.me/R/ti/g/IS1dFUCScA'

        line_bot_api.push_message(userProfile.user_id, TextSendMessage(text=recallMessage))

        self.Print('User Display Name: ' + profile.display_name)
        self.Print('User ID: ' + profile.user_id)
        self.Print('User Picture URL: ' + profile.picture_url)
        self.Print('User Status Message: ' + profile.status_message)
        pass

    # When bot joins a group/room.
    def JoinEvent(self):
        self.Print('Bot Joined')
        self.data.AddGroup(self.sourceID)
        pass
    
    # When user added bot as friend.
    def FollowEvent(self): 
        pass

    # Default operation for an event.
    def Default(self):
        pass

    # Prints out user profile.
    def PrintUserProfile(self):
        pass

    # Log out text as a message to the source.
    def Print(self, text):
        message = TextSendMessage(text=str(text))
        if self.replyTokenUsed:
            line_bot_api.push_message(self.sourceID, message)
        else:
            self.replyTokenUsed = True
            line_bot_api.reply_message(self.replyToken, message)

    # Debug action.
    def Debug(self):
        self.Print(str(self.event))
    # Enables debug.
    def EnableDebug(self):
        self.Print('Debug Enabled')
        self.debugMode = True
    # Disables debug.
    def DisableDebug(self):
        self.Print('Debug Disabled')
        self.debugMode = False

EH = EventHandler()
XSF = XStandFor()
GS = GoogldSheet()

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

    msg = event.message.text
    if 'new fact' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif 'new action' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif 'vip' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif 'horse' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif 'pictures' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif 'functions' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    elif '尖頭' in msg:
        message = sharp_head_image_message()
        line_bot_api.reply_message(event.reply_token, message)

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

# def FromJson(text):
#     exec('return ' + text)

# def ToJson(text):
#     return str(text)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    print('Bot Ready')
