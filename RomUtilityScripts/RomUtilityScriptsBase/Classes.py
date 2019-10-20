import os
import json
import gspread
from lxml import etree as ET
from oauth2client.service_account import ServiceAccountCredentials
from . import settings
from . import Utils


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
        os.makedirs('./Output', exist_ok=True)

    def connect(self, credentials=None):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        if not credentials:
            if settings.KEYFILE_TEXT:
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(settings.KEYFILE_TEXT, strict=False), scope)
            else:
                credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.KEYFILE, scope)
        self.gc = gspread.authorize(credentials)

    def open(self, spreadsheet):
        self.ss = self.gc.open(spreadsheet)

    def get_headers(self, worksheet=None):
        if not worksheet:
            worksheet = self.ss.get_worksheet(0)
        return worksheet.row_values(1)


class SbcWriter:
    @staticmethod
    def build_root(tag=None):
        if not tag:
            tag = 'Definitions'
        root = f'<{tag} xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"/>'
        return ET.fromstring(root)

    @staticmethod
    def write_sbc(root, outfile):
        Utils.clean_and_indent(root)
        ET.ElementTree(root).write(outfile, xml_declaration=True, method="xml", encoding="UTF-8")
