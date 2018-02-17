import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
    ss = None

    def connect(self):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('../Mistvalin-b3c187e87518.json', scope)
        gc = gspread.authorize(credentials)

        self.ss = gc.open('Potion Ingredients')

    def get_teas(self):
        teas_ws = self.ss.worksheet('Teas')
        return [x[:col('E') + 1] for x in teas_ws.get_all_values()[1:] if any(x[:col('E') + 1])]

    def get_extracts(self):
        teas_ws = self.ss.worksheet('Teas')
        return [x[col('G'):col('K') + 1] for x in teas_ws.get_all_values()[1:] if any(x[col('G'):col('K') + 1])]

    def get_essences(self):
        teas_ws = self.ss.worksheet('Teas')
        return [x[col('M'):col('Q') + 1] for x in teas_ws.get_all_values()[1:] if any(x[col('M'):col('Q') + 1])]

    def get_ingreds(self):
        ingred_ws = self.ss.worksheet('Ingredients')
        return [x[:col('K') + 1] for x in ingred_ws.get_all_values()[1:] if any(x[:col('K') + 1])]

    def get_final_recipes(self):
        recipes_ws = self.ss.worksheet('Final Recipes')
        headers = recipes_ws.get_all_values()[:1][0]
        return enum(*headers), recipes_ws.get_all_values()[1:]
