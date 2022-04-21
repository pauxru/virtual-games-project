# Dependencies
import time

from googleapiclient.discovery import build
from google.oauth2 import service_account


# Google sheets part ------------------------------------
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREADSHEET_ID = '14hQy0ITKmiMeZ_Env8d3oksy8SQ4W0HDGZolBYP6qvI'

service = build('sheets', 'v4', credentials=creds)


def write_to_sheets(pd_list, retry_count):
    # Call the sheets API
    sheet = service.spreadsheets()
    try:
        save_result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                            valueInputOption="RAW", range='Sheet1',
                                            body={'values': pd_list}).execute()
    except:
        if retry_count == 6:
            print("Unable to Save")
        else:
            time.sleep(1.2)
            write_to_sheets(pd_list, retry_count + 1)
    print("Saved")