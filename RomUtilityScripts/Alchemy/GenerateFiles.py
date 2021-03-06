import os
from copy import deepcopy
from collections import defaultdict

from ..RomUtilityScriptsBase.ItemClasses import CraftableItem
from ..RomUtilityScriptsBase.Classes import SbcWriter
from .AlchemyUtils import build_stats
from .Handler import AlchemySheetHandler
from . import BuildIngredients


def generate_alchemy_files():
    con = AlchemySheetHandler()
    headers, recipe_list = con.get_final_recipes()
    os.makedirs('./Output/Alchemy', exist_ok=True)

    # Ingredients and dried ingredients are not in final sheet, use ingredients sheet to generate
    BuildIngredients.build_ingredients_from_sheet(generate_ground=False)

    files = defaultdict(list)
    for recipe in recipe_list:
        filename = recipe[headers['Filename']]
        if filename != '':
            files[filename].append(recipe)

    completed_items = set()
    completed_crafting = defaultdict(int)
    for filename in files:
        root = SbcWriter.build_root()
        processed_items = []

        for recipe in files[filename]:
            build_type = recipe[headers['Build Data Type']]
            if build_type.upper() == 'NONE':
                continue

            res = [(recipe[headers['Result 1 Amount']], recipe[headers['Result 1 Type']], recipe[headers['Result 1']]),
                   (recipe[headers['Result 2 Amount']], recipe[headers['Result 2 Type']], recipe[headers['Result 2']])]

            pre = [(recipe[headers['Ingredient 1 Amount']], recipe[headers['Ingredient 1 Type']], recipe[headers['Ingredient 1']]),
                   (recipe[headers['Ingredient 2 Amount']], recipe[headers['Ingredient 2 Type']], recipe[headers['Ingredient 2']]),
                   (recipe[headers['Ingredient 3 Amount']], recipe[headers['Ingredient 3 Type']], recipe[headers['Ingredient 3']]),
                   (recipe[headers['Ingredient 4 Amount']], recipe[headers['Ingredient 4 Type']], recipe[headers['Ingredient 4']])]

            stat_effs = [(recipe[headers['Stat Effect 1']], recipe[headers['Stat Effect 1 Amount']], recipe[headers['Stat Effect 1 Time']]),
                   (recipe[headers['Stat Effect 2']], recipe[headers['Stat Effect 2 Amount']], recipe[headers['Stat Effect 2 Time']]),
                   (recipe[headers['Stat Effect 3']], recipe[headers['Stat Effect 3 Amount']], recipe[headers['Stat Effect 3 Time']]),
                   (recipe[headers['Stat Effect 4']], recipe[headers['Stat Effect 4 Amount']], recipe[headers['Stat Effect 4 Time']])]

            effs = [(recipe[headers['Effect 1']], recipe[headers['Effect 1 Type']]),
                    (recipe[headers['Effect 2']], recipe[headers['Effect 2 Type']]),
                    (recipe[headers['Effect 3']], recipe[headers['Effect 3 Type']]),
                    (recipe[headers['Effect 4']], recipe[headers['Effect 4 Type']])]


            returned_items = []
            if recipe[headers['Returned Item, Type 1']]:
                returned_items.append(tuple(x.strip() for x in recipe[headers['Returned Item, Type 1']].strip().split(',')))
            if recipe[headers['Returned Item, Type 2']]:
                returned_items.append(tuple(x.strip() for x in recipe[headers['Returned Item, Type 2']].strip().split(',')))

            categories = recipe[headers['Categories']].strip().split(',')

            description = recipe[headers['Description']].strip()
            if not description:
                if filename == 'GroundIngredients.sbc':
                    description = "A powder made by grinding %s." % recipe[headers['Ingredient 1']].replace('Ground_', '').replace('_', ' ')
                elif filename == 'Teas.sbc':
                    description = "Tea brewed by boiling %s." % recipe[headers['Ingredient 1']].replace('_', ' ')
                elif filename == 'Extracts.sbc':
                    description = "Reduced extract of %s." % recipe[headers['Result 1']].replace('_Extract', '')
                elif filename == 'Essences.sbc':
                    description = "Refined essence of %s." % recipe[headers['Result 1']].replace('_Essence', '')

            processed_items.append(CraftableItem(display_name=recipe[headers['Display Name']], model=recipe[headers['Model']],
                                                 type=recipe[headers['Result 1 Type']], returned_items=returned_items,
                                                 subtype=recipe[headers['Result 1']], icon=recipe[headers['Icon 1']],
                                                 icon2=recipe[headers['Icon 2']], icon3=recipe[headers['Icon 3']],
                                                 stats=build_stats(stat_effs), prereqs=pre, tags=recipe[headers['Tags']],
                                                 results=res, categories=categories, hidden_without_prereqs=recipe[headers['HiddenWithoutPrereqs']],
                                                 crafting_time=recipe[headers['Craft Time']], data_type=build_type,
                                                 max_stack=recipe[headers['Stack Size']], effects=effs, description=description
                                                 ))

        for x in processed_items:
            if not x.data_type.upper() == 'CRAFTING':
                if not (x.id.attrib['Type'], x.id.attrib['Subtype']) in completed_items:
                    root.append(x.build_item_def())
                    completed_items.add((x.id.attrib['Type'], x.id.attrib['Subtype']))

            # Required to force lxml to allow two of the same element in both items and crafting recipes
            x = deepcopy(x)

            if not x.data_type.upper() == 'ITEM':
                old_subtype = x.id.attrib['Subtype']
                if completed_crafting[(x.id.attrib['Type'], old_subtype)] > 0:
                    x.id.attrib['Subtype'] = old_subtype + '_' + str(completed_crafting[(x.id.attrib['Type'], x.id.attrib['Subtype'])] + 1)

                root.append(x.build_crafting_def())
                completed_crafting[(x.id.attrib['Type'], old_subtype)] += 1

        SbcWriter.write_sbc(root, 'Output/Alchemy/' + filename)
