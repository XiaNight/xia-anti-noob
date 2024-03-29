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
from PoemGeneratorModule import *
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

# Channel Access Token
line_bot_api = LineBotApi('cwBEnoA7OI09xMRwZj2JGgVLTiCY8h2fraLjFmwDMHx+JXKuewOBE5eh6xUCIt+1VQOoPVmUlow5xkZDY1oPY7yYPFcd9rN2JqtwCGH3X9Q59VnjPuC4dOqgvXpfW9P3JOgAjgkg+kVFh8yl4wEBJAdB04t89/1O/w1cDnyilFU=')

XSF = XStandFor()
GS = GoogldSheet()
PG = PoemGenerator()

class EventHandler:
    
    #Event
    event = None

    sourceID = None
    replyToken = None
    replyTokenUsed = False

    debugMode = False
    
    sourceJSON = None

    def __init__(self):
        pass

    def OnEventGet(self, event):
        self.event = event
        
        try:
            self.GetSource() # Get event source.
            self.replyToken = self.event.reply_token
            self.replyTokenUsed = False

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
            print(str(e))
            print('An error has occurred')
            self.Print('An error has occurred')

    # Return true if user's permission level is reached the required.
    def CheckPermissionLevel(self, userID, user_permission, required_permission, logWarning = True):
        if user_permission >= required_permission:
            return True
        else:
            if logWarning:
                self.Print("Permission denied, you have no permission to do this action." + \
                    "Your level: " + str(user_permission) + " Required level: " + str(required_permission))
            return False
    
    def CheckKeyWord(self, keyword, userCmd, user_permission, required_permission = 1, logWarning = True):
        if userCmd == keyword:
            if self.CheckPermissionLevel(userID=self.GetUserID(), \
                                        user_permission=user_permission, \
                                        required_permission=required_permission, \
                                        logWarning=logWarning):
                return True
        return False

    # When user/group/room sends a message.
    def MessageEvent(self):
        # userIndex = None
        # print('Handling messageEvent, type = ' + self.event.source.type)
        # if self.event.source.type == 'user':
        #     # Add user to Users if user not exist.
        #     print('Check if user exist in Users')
        #     usernames = self.GetAllUsernames('Users') # Get all usernames in sheet 'Users'.
        #     if self.GetUserID() not in usernames:
        #         print('Adding user to Users')
        #         GS.AppendValue('Users', [self.GetUserID(), 1, self.event.timestamp])
        #         userIndex = len(usernames)
        #     else:
        #         print('User exist in Users.')
        #         userIndex = usernames.index(self.GetUserID()) # Get user index in usernames.
        #         perm = int(GS.GetRange('Users!B' + str(userIndex + 1))[0][0]) # +1 because sheet row starts with 1.
        # else:
        #     # Create sheet if not exist
        #     print('Check if sheet exist')
        #     if not GS.CheckIfSheetExists(self.sourceID): # If group id were not in the list.
        #         print('Adding new sheet')
        #         GS.AddSheet(self.sourceID)
        #     else:
        #         print('Sheet exist.')

        #     # Add group to GroupJson if not exist.
        #     print('Check if group exist in GroupJSON.')
        #     groups = self.GetAllUsernames('GroupJSON')
        #     print('Found {0} groups in group'.format(len(groups)))
        #     if self.sourceID not in groups:
        #         print('Adding group to GroupJSON.')
        #         defaultJson = {'debug_mode': False, 'KeyWords': {}}
        #         GS.AppendValue('GroupJSON', [self.sourceID, str(defaultJson)])
        #     else:
        #         print('Group exist in GroupJSON.')
        #         sourceIndex = groups.index(self.sourceID)
        #         sourceJSON = GS.GetRange('GroupJSON!B' + str(sourceIndex + 1))[0][0] # +1 because sheet row starts with 1.

        #     # Add user to group if user not exist.
        #     print('Check if user exist in group.')
        #     usernames = self.GetAllUsernames(self.sourceID)
        #     print('Found {0} users in group'.format(len(usernames)))
        #     if self.GetUserID() not in usernames: # If username were not in the list.
        #         print('Adding user to group.')
        #         GS.AppendValue(self.sourceID, [self.GetUserID(), 1, self.event.timestamp])
        #         userIndex = len(usernames)
        #     else:
        #         print('User exist in group.')
        #         userIndex = usernames.index(self.GetUserID()) # Get user index in usernames.
        #         perm = int(GS.GetRange(self.sourceID + '!B' + str(userIndex + 1))[0][0]) # +1 because sheet row starts with 1.
        #     print('Group check done.')
        
        perm = 4

        msg = self.event.message.text
        if msg[0] == '#': # Raw python code executing.
            if self.CheckPermissionLevel(self.GetUserID(), perm, 4, logWarning=False): # Requires developer level to execute.
                exec(compile(msg[1:],"-","exec"))
        elif msg[0] == '$': # Commands here.
            command = msg[1:]
            if self.CheckKeyWord('help', command, perm, 2):
                self.Print('$EnableDebug to enable debug\n$DisableDebug to disable debug\nstart with # to execute raw python code.')
            if self.CheckKeyWord('EnableDebug', command, perm, 4):
                self.EnableDebug()
            if self.CheckKeyWord('DisableDebug', command, perm, 4):
                self.DisableDebug()
        elif msg[0] == '%': # X stands for
            print('Executing X stands for')
            splits = msg[1:].split(' ')
            if len(splits) < 2:
                self.Print('Not enough arguments')
                return
            userInput = splits[0]
            times = splits[1]
            times = int(times)
            if times > 30: # Safty guard.
                times = 30
            self.Print(XSF.fetch(userInput, times))
        elif msg[0] == '&': # translate input multiple times
            print('Executing Idea_Transformer')
            splits = msg[1:].split(' ')
            userInputTimesSplits = msg[1:].split('&')
            userInput = XSF.Merge(splits).split('&')[0]
            print(userInput)
            print(userInputTimesSplits) 
            times = 5
            if len(userInputTimesSplits) >= 2:
                times = int(userInputTimesSplits[-1])
            if times > 30: # Safty guard.
                times = 30
            self.Print(XSF.idea_transformer(userInput, times))
        elif msg[0] == ')':
            print('Executing Trash Talk')
            if(msg[1].lower() == 'a'):
                GS.AppendValue('TrashTalk', msg[2:])
                self.Print('Successfully added TRASH into our system!')
            if(msg[1].lower() == 'g'):
                trashes = GS.GetRange('TrashTalk!A:A', majorDimension='COLUMNS')[0]
                randomInt = random.randint(0, len(trashes) - 1)
                self.Print(trashes[randomInt])
                pass
        elif msg[0] == '^':
            splits = msg[1:].split('^')
            parmsLength = len(splits)

            mode = 1
            minSize = 4
            maxSize = 4
            minSentense = 4
            maxSentense = 7

            if parmsLength > 0:
                mode = int(splits[0])

            if parmsLength > 1:
                minSize = int(splits[1])


            if mode == 2:
                if parmsLength > 2:
                    maxSize = int(splits[2])
                if parmsLength > 3:
                    minSentense = int(splits[3]) + 1
                if parmsLength > 4:
                    maxSentense = int(splits[4]) + 1


            minSize = min(minSize, 9)
            maxSize = min(maxSize, 10)
            minSentense = min(minSentense, 9)
            maxSentense = min(maxSentense, 10)

            print('Executing Poem Generator')

            poem = None
            if mode == 1:
                poem = PG.GetPoem(minSize, False)
            if mode == 2:
                poem = PG.GetScatterPoem(minSize, maxSize, minSentense, maxSentense)
            self.Print(poem)

    # Get all usernames in the sheet.
    def GetAllUsernames(self, sheet):
        return GS.GetRange(sheet + '!A:A', majorDimension='COLUMNS')[0]

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

if __name__ == '__main__':
    EH = EventHandler()