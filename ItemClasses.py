import xml.etree.ElementTree as ET


class Craftable(object):
    crafting_time = None
    prereqs = None  # List of (amount, type, subtype) tuples
    results = None  # List of (amount, type, subtype) tuples
    categories = None  # List of strings
    hidden_without_prereqs = None

    def __init__(self, prereqs=None, categories=None, crafting_time=3, results=None, hidden_without_prereqs=None, **kwargs):
        super(Craftable, self).__init__()
        self.crafting_time = ET.Element('CraftingTime')
        self.crafting_time.attrib['Seconds'] = str(crafting_time)
        if hidden_without_prereqs == 'TRUE':
            self.hidden_without_prereqs = ET.Element('HiddenWithoutPrereqs')
            self.hidden_without_prereqs.text = 'true'
        if prereqs:
            self.prereqs = ET.Element('Prerequisites')
            for amount, type, subtype in prereqs:
                if not (amount and type and subtype):
                    continue
                item = ET.Element('Item')
                if amount == "SET MANUALLY":
                    amount = 1

                if type.lower() == 'tag':
                    item.attrib['Tag'] = subtype
                else:
                    item.attrib['Type'] = type
                    item.attrib['Subtype'] = subtype
                item.attrib['Amount'] = str(amount)
                self.prereqs.append(item)
        if results:
            self.results = ET.Element('Results')
            for amount, type, subtype in results:
                if not (amount and type and subtype):
                    continue
                item = ET.Element('Item')
                if amount == "SET MANUALLY":
                    amount = 1

                if type.lower() == 'tag':
                    item.attrib['Tag'] = subtype
                else:
                    item.attrib['Type'] = type
                    item.attrib['Subtype'] = subtype
                item.attrib['Amount'] = str(amount)
                self.results.append(item)
        if categories:
            self.categories = []
            for c in categories:
                cat = ET.Element('Category')
                cat.text = c
                self.categories.append(cat)


class Item(object):
    id = None
    max_stack = None
    health = None
    mass = None
    size = None
    model = None
    icon = None
    material = None
    description = None
    display_name = None
    tags = None
    data_type = 'BOTH'

    consumable = False
    stats = None
    use_sound = None
    returned_items = None # List of elements

    def __init__(self, type="InventoryItem", subtype="", max_stack=16, health=200, mass=2, size=(1, 1, 1), model="",
                 icon="", description="", display_name="", tags=None, consumable=False, stats=None, material="None",
                 returned_items=list(), data_type='BOTH', **kwargs):

        self.id = ET.Element('Id')
        self.max_stack = ET.Element('MaxStackAmount')
        self.mass = ET.Element('Mass')
        self.size = ET.Element('Size')
        self.model = ET.Element('Model')
        self.icon = ET.Element('Icon')
        self.material = ET.Element('PhysicalMaterial')
        self.description = ET.Element('Description')
        self.display_name = ET.Element('DisplayName')
        self.tags = []

        self.id.attrib['Type'] = type
        self.id.attrib['Subtype'] = subtype

        if type == 'ConsumableItem':
            self.consumable = True

        self.max_stack.text = str(max_stack)
        if health:
            self.health = ET.Element('Health')
            self.health.text = str(health)
        self.mass = str(mass)

        size_x = ET.Element('X')
        size_z = ET.Element('Y')
        size_y = ET.Element('Z')
        size_x.text, size_z.text, size_y.text = str(size[0]), str(size[1]), str(size[2])
        self.size.extend((size_x, size_y, size_z))

        self.model.text = model
        self.icon.text = icon
        self.material.text = material
        self.description.text = str(description)
        if display_name:
            self.display_name.text = display_name
        else:
            self.display_name.text = subtype.rstrip('1234567890').rstrip('_').replace('_', ' ')

        if tags:
            for t in tags.strip().split(','):
                tag = ET.Element('Tag')
                tag.text = t.strip()
                self.tags.append(tag)

        if self.consumable:
            if stats is not None:
                self.stats = ET.Element('Stats')
                for k, (x, y) in stats.items():
                    stat = ET.Element('Stat')
                    stat.attrib['Name'] = k
                    stat.attrib['Value'] = str(x)
                    stat.attrib['Time'] = str(y)
                    self.stats.append(stat)
            self.use_sound = ET.Element('UseSound')
            self.use_sound.text = "PlayEat"
            if returned_items:
                self.returned_items = []
                for item in returned_items:
                    ret = ET.Element('ReturnedItem')
                    ret.attrib['Type'] = item[1]
                    ret.attrib['Subtype'] = item[0]
                    self.returned_items.append(ret)

        self.data_type = data_type

        super(Item, self).__init__(**kwargs)

    def __repr__(self):
        return "<{}: {}>".format(type(self).__name__, self.id.attrib['Subtype'])

    def build_item_def(self):
        root = ET.Element('Definition')
        if self.consumable:
            root.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] = 'MyObjectBuilder_ConsumableItemDefinition'
        else:
            root.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] = 'MyObjectBuilder_InventoryItemDefinition'

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

        if self.id.attrib['Type'] == 'ConsumableItem':
            if list(self.stats):
                root.append(self.stats)
            root.append(self.use_sound)
            for item in self.returned_items:
                root.append(item)

        return root


class CraftableItem(Item, Craftable):
    def build_crafting_def(self):
        root = ET.Element('Definition')
        root.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] = 'MyObjectBuilder_CraftingRecipeDefinition'

        crafting_id = ET.Element('Id')
        crafting_id.attrib['Type'] = 'MyObjectBuilder_CraftingRecipeDefinition'
        crafting_id.attrib['Subtype'] = self.id.attrib['Subtype']

        root.append(crafting_id)
        root.append(self.display_name)
        root.append(self.icon)
        for cat in self.categories:
            root.append(cat)

        root.append(self.prereqs)
        root.append(self.results)
        root.append(self.crafting_time)
        if self.hidden_without_prereqs is not None:
            root.append(self.hidden_without_prereqs)

        return root
