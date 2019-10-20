from ..RomUtilityScriptsBase.Classes import SheetCon, col, enum

expected_headers_alchemy = ["Display Name", "Build Data Type",
                            "Result 1", "Result 1 Amount", "Result 1 Type",
                            "Result 2", "Result 2 Amount", "Result 2 Type",
                            "Ingredient 1", "Ingredient 1 Amount", "Ingredient 1 Type",
                            "Ingredient 2", "Ingredient 2 Amount", "Ingredient 2 Type",
                            "Ingredient 3", "Ingredient 3 Amount", "Ingredient 3 Type",
                            "Ingredient 4", "Ingredient 4 Amount", "Ingredient 4 Type",
                            "Stat Effect 1", "Stat Effect 1 Amount", "Stat Effect 1 Time",
                            "Stat Effect 2", "Stat Effect 2 Amount", "Stat Effect 2 Time",
                            "Stat Effect 3", "Stat Effect 3 Amount", "Stat Effect 3 Time",
                            "Stat Effect 4", "Stat Effect 4 Amount", "Stat Effect 4 Time",
                            "Effect 1", "Effect 1 Type", "Effect 2", "Effect 2 Type",
                            "Effect 3", "Effect 3 Type", "Effect 4", "Effect 4 Type",
                            "Categories", "Craft Time", "Stack Size", "Filename", 
                            "Icon 1", "Icon 2", "Icon 3", "Model", "Tags", "HiddenWithoutPrereqs",
                            "Returned Item, Type 1", "Returned Item, Type 2"]


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
        if headers != expected_headers_alchemy:
            print(f'\nSomething changed with the alchemy group headers! Got \n{headers} \n expected \n{expected_headers_alchemy}')
            return
        return enum(*headers), recipes_ws.get_all_values()[1:]
