from ItemClasses import *
from Utils import indent
from AlchemyUtils import build_stats
from DataImporter import SheetCon


class Tea(CraftableItem):
    def __init__(self, name, effects, ingredient, max_stack=5, crafting_time=30, consumable=True, categories=None,
                 prereqs=None, results=None):

        if not prereqs:
            prereqs = [(1, "InventoryItem", ingredient)]

        if not results:
            results = [(1, "ConsumableItem" if consumable else "InventoryItem", name)]

        super(Tea, self).__init__(display_name=name.replace('_', ' '), subtype=name, stats=build_stats(effects),
                                  max_stack=max_stack, crafting_time=crafting_time, consumable=consumable,
                                  categories=categories, prereqs=prereqs, results=results)

        if not self.description.text:
            self.description.text = "A liquid brewed from ground %s." % ingredient.replace('Ground_', '')


def build_from_sheet():
    con = SheetCon()
    con.connect()
    teas = con.get_teas()

    root = ET.Element('Definitions')
    processed_teas = {}
    for row in teas:
        processed_teas[row[0]] = Tea(name=row[0], effects=row[1:3], ingredient=row[3], categories=[row[4]])

    for x in processed_teas.values():
        root.append(x.build_item_def())
        root.append(x.build_crafting_def())

    indent(root)
    ET.ElementTree(root).write('Teas.xml', xml_declaration=True, method="xml")
