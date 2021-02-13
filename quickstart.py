from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

'''
spreadsheet 是整個檔案，會有一個id 就是 spreadsheet_id
sheet 是在一個試算表內的分頁，用名字呼叫
range是搜尋的關鍵字，包刮分頁名稱跟欄位
例如1: 'Sheet1!A0:E7'
就是搜尋在Sheet1裡面 左上從A0到右下E7裡面的資料，包刮E7，回傳二維陣列

範例2: 'Sheet1!A'也就是取得整條A的資料
範例3: 'Sheet1!A0'取得A0的資料

可參考 https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get?apix_params=%7B%22spreadsheetId%22%3A%221BCssfTKEBnOSO41Zq2XkGlbfNZJ5qCPeSzlfJersjzw%22%7D
'''

# 權限設定，可以看https://developers.google.com/sheets/api/guides/authorizing
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogldSheet():

    service = None

    #我只會用到一個試算表，所以我把spreadsheet_id存在這裡
    # The target spreadsheet we are using
    spreadsheet_id = '1BCssfTKEBnOSO41Zq2XkGlbfNZJ5qCPeSzlfJersjzw'

    def __init__(self): # 這邊在處理建立連線的東西，我看不懂，但是他會設定好service可以用
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    #更新一個特定除存格，sheet是分頁，cell是欄位。範例：UpdateCell('Sheet1', 'C3', 30)
    def UpdateCell(self, sheet, cell, value):
        # The A1 notation of the values to update.
        range_ = sheet + '!' + cell

        # How the input data should be interpreted.
        value_input_option = 'RAW'  # TODO: Update placeholder value. 
        value_range_body = {
            "values": [
                [
                    value
                ]
            ]
        }
        request = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()

    #從下方新增一行資料到sheet, value可以是陣列，也可以是其他的
    def AppendValue(self, sheet, value):
        values = None
        if type(value) == list: # 如果value是list，那就把values設定成輸入近來的list
            values = [
                value
                # Additional rows ...
            ]
        else: # 如果不是，就把values設定成長度為1的陣列，內容是輸入值value
            values = [
                [
                    value
                ]
                # Additional rows ...
            ]
        # 以下就是把資料整理傳給service執行
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=sheet,
            valueInputOption='RAW',
            body=body).execute()
        
        print('{0} cells appended.'.format(result \
                                            .get('updates') \
                                            .get('updatedCells')))
    #創立一個新的分頁如果分頁不存在
    def CreateIfNotExist(self, sheet):
        if not self.CheckIfSheetExists(sheet):
            self.AddSheet(sheet)

    #創立一個新的分頁
    def AddSheet(self, title):
        body = {
          'requests': [
            {
              "addSheet": {
                "properties": {
                  "title": title,
                  # "gridProperties": {
                  #   "rowCount": 20,
                  #   "columnCount": 12
                  # },
                  "tabColor": {
                    "red": 1.0,
                    "green": 0.3,
                    "blue": 0.4
                  }
                }
              }
            }
          ]
        }
        sheet = self.service.spreadsheets()
        result = sheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body)
        result.execute()
    def CheckIfSheetExists(self, sheet_name):
        if sheet_name not in self.GetAllSheetNames():
            return False
        else:
            return True
    #取得所有分頁名稱
    def GetAllSheetNames(self):
        names = []
        sheets = self.GetSheetData()['sheets']
        for sheet in sheets:
            names.append(sheet['properties']['title'])
        return names
    #取得分頁資料
    def GetSheetData(self):
        sheet = self.service.spreadsheets()
        result = sheet.get(spreadsheetId=self.spreadsheet_id)
        return result.execute()
    #取得範圍內資料
    def GetRange(self, range, majorDimension='ROWS'):

        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=range,
                                    majorDimension=majorDimension).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return [[]] # return empty rows and columes
        return values

if __name__ == '__main__':

    GS = GoogldSheet()
    # GS.AddIfUserNotExist('TestUSER2')
    # print(GS.GetSheet('Cb8e23eab96206bc49a752bb10b2ae7af' + '!B1', majorDimension='COLUMNS'))

    print(GS.GetRange('Users!B' + str(0 + 1)))

    # print(GS.GetAllUserName())
