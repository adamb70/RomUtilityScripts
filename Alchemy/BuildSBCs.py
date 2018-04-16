from collections import defaultdict

from ItemClasses import *
from Utils import indent
from AlchemyUtils import build_stats
from DataImporter import SheetCon
import BuildIngredients

con = SheetCon()
con.connect()
headers, recipe_list = con.get_final_recipes()


""" Expected Headers:
Result 1
Result 1 Amount
Result 1 Type
Result 2
Result 2 Amount
Result 2 Type
Ingredient 1
Ingredient 1 Amount
Ingredient 1 Type
Ingredient 2
Ingredient 2 Amount
Ingredient 2 Type
Ingredient 3
Ingredient 3 Amount
Ingredient 3 Type
Ingredient 4
Ingredient 4 Amount
Ingredient 4 Type
Effect 1
Effect 1 Amount
Effect 1 Time
Effect 2
Effect 2 Amount
Effect 2 Time
Effect 3
Effect 3 Amount
Effect 3 Time
Effect 4
Effect 4 Amount
Effect 4 Time
Categories
Craft Time
Stack Size
Filename
Icon
Tags"""


# Ingredients and dried ingredients are not in final sheet, use ingredients sheet to generate
BuildIngredients.build_ingredients_from_sheet(generate_ground=False)

files = defaultdict(list)
for recipe in recipe_list:
    files[recipe[headers['Filename']]].append(recipe)


completed_items = set()
completed_crafting = defaultdict(int)
for filename in files:
    root = ET.Element('Definitions')
    processed_items = []

    for recipe in files[filename]:
        res = [(recipe[headers['Result 1 Amount']], recipe[headers['Result 1 Type']], recipe[headers['Result 1']]),
               (recipe[headers['Result 2 Amount']], recipe[headers['Result 2 Type']], recipe[headers['Result 2']])]

        pre = [(recipe[headers['Ingredient 1 Amount']], recipe[headers['Ingredient 1 Type']], recipe[headers['Ingredient 1']]),
               (recipe[headers['Ingredient 2 Amount']], recipe[headers['Ingredient 2 Type']], recipe[headers['Ingredient 2']]),
               (recipe[headers['Ingredient 3 Amount']], recipe[headers['Ingredient 3 Type']], recipe[headers['Ingredient 3']]),
               (recipe[headers['Ingredient 4 Amount']], recipe[headers['Ingredient 4 Type']], recipe[headers['Ingredient 4']])]

        eff = [(recipe[headers['Effect 1']], recipe[headers['Effect 1 Amount']], recipe[headers['Effect 1 Time']]),
               (recipe[headers['Effect 2']], recipe[headers['Effect 2 Amount']], recipe[headers['Effect 2 Time']]),
               (recipe[headers['Effect 3']], recipe[headers['Effect 3 Amount']], recipe[headers['Effect 3 Time']]),
               (recipe[headers['Effect 4']], recipe[headers['Effect 4 Amount']], recipe[headers['Effect 4 Time']])]

        categories = recipe[headers['Categories']].strip().split(',')

        processed_items.append(CraftableItem(display_name=recipe[headers['Display Name']],
                                             type=recipe[headers['Result 1 Type']],
                                             subtype=recipe[headers['Result 1']], icon=recipe[headers['Icon']],
                                             stats=build_stats(eff), prereqs=pre, tags=recipe[headers['Tags']],
                                             results=res, categories=categories,
                                             crafting_time=recipe[headers['Craft Time']]))

    for x in processed_items:
        if not (x.id.attrib['Type'], x.id.attrib['Subtype']) in completed_items:
            root.append(x.build_item_def())
            completed_items.add((x.id.attrib['Type'], x.id.attrib['Subtype']))

        old_subtype = x.id.attrib['Subtype']
        if completed_crafting[(x.id.attrib['Type'], old_subtype)] > 0:
            x.id.attrib['Subtype'] = old_subtype + '_' + str(completed_crafting[(x.id.attrib['Type'], x.id.attrib['Subtype'])] + 1)

        root.append(x.build_crafting_def())
        completed_crafting[(x.id.attrib['Type'], old_subtype)] += 1

    indent(root)
    ET.ElementTree(root).write('Output/'+filename, xml_declaration=True, method="xml", encoding="UTF-8")
