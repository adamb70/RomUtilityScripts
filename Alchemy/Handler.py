from SheetConnector import SheetCon, col, enum


class AlchemySheetHandler(SheetCon):
    def __init__(self):
        super(AlchemySheetHandler, self).__init__()
        self.open('Potion Ingredients')

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
        return [x[:col('M') + 1] for x in ingred_ws.get_all_values()[1:] if any(x[:col('M') + 1])]

    def get_final_recipes(self):
        recipes_ws = self.ss.worksheet('Final Recipes')
        headers = recipes_ws.get_all_values()[:1][0]
        return enum(*headers), recipes_ws.get_all_values()[1:]
