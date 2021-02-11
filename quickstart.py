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

    def GetSheet(self, spreadsheetId, range):

        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheetId, range=range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))

        # result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        # rows = result.get('values', [])
        # print('{0} rows retrieved.'.format(len(rows)))

    def UpdateSheet(self, spreadsheet_id, table, cell, value):

        # The A1 notation of the values to update.
        range_ = table + '!' + cell

        # How the input data should be interpreted.
        value_input_option = 'RAW'  # TODO: Update placeholder value.

        value_range_body = {
            "values": [
                [
                    value
                ]
            ]
        }

        request = self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()

    def AddSheet(self, spreadsheet_id, title):
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
        result = sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        result.execute()
        # print(result)

if __name__ == '__main__':

    MySheet = '1BCssfTKEBnOSO41Zq2XkGlbfNZJ5qCPeSzlfJersjzw'

    GS = GoogldSheet()
    GS.AddSheet(MySheet, 'Sheet2')