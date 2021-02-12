from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'

'''

499637180067-tp273vuq6rl452umu4j3nggh9eofi5t1.apps.googleusercontent.com

k7A-d-Ztm0GbKOyIGN-lmh_-

'''

class GoogldSheet():

    service = None

    # The target spreadsheet we are using
    spreadsheet_id = '1BCssfTKEBnOSO41Zq2XkGlbfNZJ5qCPeSzlfJersjzw'

    def __init__(self):
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

    def AppendValue(self, sheet, value):
        values = None
        if type(value) == list:
            values = [
                value
                # Additional rows ...
            ]
        else:
            values = [
                [
                    value
                ]
                # Additional rows ...
            ]
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
    def CreateIfNotExist(self, sheet):
        if not self.CheckIfSheetExists(sheet):
            self.AddSheet(sheet)
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
    def GetAllSheetNames(self):
        names = []
        sheets = self.GetSheetData()['sheets']
        for sheet in sheets:
            names.append(sheet['properties']['title'])
        return names

    def GetSheetData(self):
        sheet = self.service.spreadsheets()
        result = sheet.get(spreadsheetId=self.spreadsheet_id)
        return result.execute()

    def GetSheet(self, range, majorDimension='ROWS'):

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

    print(GS.GetSheet('Users!B' + str(0 + 1)))

    # print(GS.GetAllUserName())
