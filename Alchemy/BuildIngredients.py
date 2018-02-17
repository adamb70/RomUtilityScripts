from ItemClasses import *
from Utils import indent
from DataImporter import SheetCon


class Ingredient(Item):
    decayed_item = None

    def __init__(self, name, max_stack=16, dried_suffix=None, consumable=False):
        super(Ingredient, self).__init__(display_name=name.replace('_', ' '), subtype=name, type='DurableItem',
                                         max_stack=max_stack, consumable=consumable)
        self.max_durability = ET.Element('MaxDurability')
        self.max_durability.text = str(6)

        self.decayed_item = ET.Element('BrokenItem')
        self.decayed_item.attrib['Type'] = 'MyObjectBuilder_InventoryItem'
        if dried_suffix:
            dried_suffix = '_'+dried_suffix
        self.decayed_item.attrib['Subtype'] = "Dried_" + name + dried_suffix

    def build_item_def(self):
        """ Must use DurableItem for now to be able to decay into dried item """
        root = ET.Element('Definition')
        root.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] = 'MyObjectBuilder_DurableItemDefinition'

        root.append(self.id)

        if self.tags:
            for t in self.tags:
                root.append(t)

        public = ET.Element('Public')
        public.text = "true"
        root.append(public)
        root.append(self.display_name)
        root.append(self.description)
        root.append(self.icon)
        root.append(self.material)
        root.append(self.size)
        root.append(self.model)
        root.append(self.max_stack)
        root.append(self.max_durability)
        root.append(self.decayed_item)

        if self.consumable:
            if self.stats is not None:
                root.append(self.stats)
            root.append(self.use_sound)

        return root


class DriedIngredient(Item):
    def __init__(self, name, ingredient, max_stack=4, consumable=False):
        super(DriedIngredient, self).__init__(display_name=name.replace('_', ' '), subtype=name, max_stack=max_stack,
                                              consumable=consumable)

        if not self.description.text:
            self.description.text = "Dried %s." % ingredient.replace('Dried_', '').replace('_', ' ')


class GroundIngredient(CraftableItem):
    def __init__(self, name, ingredient, ingredient_type, max_stack=20, crafting_time=3, consumable=False,
                 categories=None, prereqs=None, results=None):

        if not prereqs:
            prereqs = [(1, ingredient_type, ingredient)]

        if not categories:
            categories = ["Mortar_And_Pestle"]

        if not results:
            results = [(1, "ConsumableItem" if consumable else "InventoryItem", name)]

        super(GroundIngredient, self).__init__(display_name=name.replace('_', ' '), subtype=name,
                                               max_stack=max_stack, crafting_time=crafting_time, consumable=consumable,
                                               categories=categories, prereqs=prereqs, results=results)

        if not self.description.text:
            self.description.text = "A powder made by grinding %s." % ingredient.replace('Ground_', '')


def build_ingredients_from_sheet(generate_ground=True):
    """ Builds from ingredients sheet. Auto generates ground and dried varieties """
    con = SheetCon()
    con.connect()
    ingreds = con.get_ingreds()

    ing_root = ET.Element('Definitions')
    ground_root = ET.Element('Definitions')
    dried_root = ET.Element('Definitions')
    processed_ingreds = {}
    ground_ingreds = {}
    dried_ingreds = {}
    for row in ingreds:
        processed_ingreds[row[0]] = Ingredient(name=row[0], dried_suffix=row[10])
        ground_name = "Ground_" + row[0]
        ground_ingreds[ground_name] = GroundIngredient(name=ground_name, ingredient=row[0],
                                                       ingredient_type=processed_ingreds[row[0]].id.attrib['Type'])

        dried_name = "Dried_" + row[0]
        if row[10]:
            dried_name += '_' + row[10]
        dried_ingreds[dried_name] = DriedIngredient(name=dried_name, ingredient=row[0])

    for x in processed_ingreds.values():
        ing_root.append(x.build_item_def())

    for x in ground_ingreds.values():
        ground_root.append(x.build_item_def())
        ground_root.append(x.build_crafting_def())

    for x in dried_ingreds.values():
        dried_root.append(x.build_item_def())

    indent(ing_root)
    indent(ground_root)
    indent(dried_root)
    ET.ElementTree(ing_root).write('Output/Ingredients.xml', xml_declaration=True, method="xml")
    ET.ElementTree(dried_root).write('Output/DriedIngredients.xml', xml_declaration=True, method="xml")
    if generate_ground:
        ET.ElementTree(ground_root).write('Otput/GroundIngredients.xml', xml_declaration=True, method="xml")
