import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from . import settings


def col(letters):
    """ Convert column letters into zero-indexed number """
    letters = letters.lower()
    num = 0
    for l in letters[:-1]:
        num += (ord(l) - 96) * 26
    num += (ord(letters[-1]) - 96)
    return num - 1


def enum(*sequential):
    enums = dict(zip(sequential, range(len(sequential))))
    return enums


class SheetCon(object):
    gc = None
    ss = None

    def __init__(self, credentials=None):
        self.connect(credentials=credentials)

    def connect(self, credentials=None):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        if not credentials:
            if settings.KEYFILE_TEXT:
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(settings.KEYFILE_TEXT))
            else:
                credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.KEYFILE, scope)
        self.gc = gspread.authorize(credentials)

    def open(self, spreadsheet):
        self.ss = self.gc.open(spreadsheet)

    def get_headers(self, worksheet=None):
        if not worksheet:
            worksheet = self.ss.get_worksheet(0)
        return worksheet.row_values(1)
