import xml.etree.ElementTree as ET
from Base.ItemClasses import Item, CraftableItem
from Base.Utils import indent
from Alchemy.Handler import AlchemySheetHandler


class Ingredient(Item):
    decayed_item = None

    def __init__(self, name, max_stack=16, icon="", dried_suffix=None, consumable=False, tags="", model=""):
        super(Ingredient, self).__init__(display_name=name.replace('_', ' '), subtype=name, type='DurableItem',
                                         max_stack=max_stack, consumable=consumable, icon=icon, tags=tags, model=model)
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
    def __init__(self, name, ingredient, max_stack=16, consumable=False, icon="", tags="", model=""):
        super(DriedIngredient, self).__init__(display_name=name.replace('_', ' '), subtype=name, max_stack=max_stack,
                                              consumable=consumable, icon=icon, tags=tags, model=model)

        if not self.description.text:
            self.description.text = "Dried %s." % ingredient.replace('Dried_', '').replace('_', ' ')


class GroundIngredient(CraftableItem):
    def __init__(self, name, ingredient, ingredient_type, max_stack=16, crafting_time=3, consumable=False,
                 categories=None, prereqs=None, results=None, hidden_without_prereqs=None):

        if not prereqs:
            prereqs = [(1, ingredient_type, ingredient)]

        if not categories:
            categories = ["Mortar_And_Pestle"]

        if not results:
            results = [(1, "ConsumableItem" if consumable else "InventoryItem", name)]

        super(GroundIngredient, self).__init__(display_name=name.replace('_', ' '), subtype=name,
                                               max_stack=max_stack, crafting_time=crafting_time, consumable=consumable,
                                               categories=categories, prereqs=prereqs, results=results, hidden_without_prereqs=hidden_without_prereqs)

        if not self.description.text:
            self.description.text = "A powder made by grinding %s." % ingredient.replace('Ground_', '')


def build_ingredients_from_sheet(generate_ground=True):
    """ Builds from ingredients sheet. Auto generates ground and dried varieties """
    con = AlchemySheetHandler()
    ingreds = con.get_ingreds()

    ing_root = ET.Element('Definitions')
    ground_root = ET.Element('Definitions')
    dried_root = ET.Element('Definitions')
    processed_ingreds = {}
    ground_ingreds = {}
    dried_ingreds = {}
    for row in ingreds:
        processed_ingreds[row[0]] = Ingredient(name=row[0], dried_suffix=row[10], icon=row[11], tags=row[12], model="Models\Consumables\Herbs.mwm")
        ground_name = "Ground_" + row[0]
        ground_ingreds[ground_name] = GroundIngredient(name=ground_name, ingredient=row[0],
                                                       ingredient_type=processed_ingreds[row[0]].id.attrib['Type'])

        dried_name = "Dried_" + row[0]
        if row[10]:
            dried_name += '_' + row[10]
        dried_ingreds[dried_name] = DriedIngredient(name=dried_name, ingredient=row[0], icon=row[11], tags="Dried_Ingredient", model="Models\Consumables\Herbs.mwm")

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
    ET.ElementTree(ing_root).write('Output/Ingredients.sbc', xml_declaration=True, method="xml", encoding="UTF-8")
    ET.ElementTree(dried_root).write('Output/DriedIngredients.sbc', xml_declaration=True, method="xml", encoding="UTF-8")
    if generate_ground:
        ET.ElementTree(ground_root).write('Output/GroundIngredients.sbc', xml_declaration=True, method="xml", encoding="UTF-8")
