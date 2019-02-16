from collections import defaultdict
import xml.etree.ElementTree as ET

from RomUtilityScriptsBase.SheetConnector import SheetCon
from RomUtilityScriptsBase.Utils import indent
from WorldGen.Environment.ItemGroup import ItemGroup
from WorldGen.Environment.GrowableItem import GrowableItem


class ProceduralItemGroupSheetHandler(SheetCon):
    def __init__(self):
        super(ProceduralItemGroupSheetHandler, self).__init__()
        self.open('Procedural Environments')

    def get_item_group_dict(self):
        item_group_ws = self.ss.worksheet('ItemGroups')
        vals = item_group_ws.get_all_values()
        headers, vals = vals[0], vals[1:]
        expected = ['Name', 'Density', 'LodStart', 'LodEnd']
        if headers != expected:
            print('Something changed with the environment item group definition headers!', headers)
            return

        item_groups = []
        for row in vals:
            group = ItemGroup(name=row[0], density=row[1], lod_start=row[2], lod_end=row[3])
            group.mappings = self.get_item_group_mappings(group)
            item_groups.append(group)

        return item_groups

    def get_item_group_mappings(self, group):
        group_ws = self.ss.worksheet(group.name)
        vals = group_ws.get_all_values()
        headers, vals = vals[0], vals[1:]
        expected = ['Biomes', 'Materials', 'Slope Min', 'Slope Max', 'Height Min', 'Height Max', 'Type', 'Subtype',
                    'Density', 'MaxRoll', 'Latitude min', 'Latitude Max', 'Longitude Min', 'Longitude Max']
        if headers != expected:
            print('Something changed with the environment item group headers!', headers)

        mappings = {}
        for row in vals:
            mapping = ItemGroup.Mapping()
            mapping.biomes = tuple(s.strip() for s in row[0].split(','))
            mapping.materials = tuple(s.strip() for s in row[1].split(','))
            mapping.slope = (row[2], row[3])
            mapping.height = (row[4], row[5])
            mapping.latitude = (row[10], row[11])
            mapping.longitude = (row[12], row[13])

            map_key = mapping.unique_id
            if mappings.get(map_key, None) is not None:
                mapping = mappings[map_key]

            mapping.mapping_items.append([row[6], row[7], row[8], row[9]])
            mappings[map_key] = mapping

        return list(mappings.values())

    def write_item_groups(self, item_groups, outfile):
        root = ET.Element('PutTheseInProceduralWorldDef')
        for itemgroupdata in item_groups:
            itemgroup = ET.Element('ItemGroup')
            itemgroup.attrib['Name'] = itemgroupdata.name
            itemgroup.attrib['Density'] = itemgroupdata.density
            itemgroup.attrib['LodStart'] = itemgroupdata.lod[0]
            itemgroup.attrib['LodEnd'] = itemgroupdata.lod[1]

            for mappingdata in itemgroupdata.mappings:
                mapping = ET.Element('Mapping')

                for biome in mappingdata.biomes:
                    b = ET.Element('Biome')
                    b.text = biome
                    mapping.append(b)

                for material in mappingdata.materials:
                    m = ET.Element('Material')
                    m.text = material
                    mapping.append(m)

                if all(mappingdata.height):
                    height = ET.Element('Height')
                    height.attrib['Min'] = mappingdata.height[0]
                    height.attrib['Max'] = mappingdata.height[1]
                    mapping.append(height)
                if all(mappingdata.slope):
                    slope = ET.Element('Slope')
                    slope.attrib['Min'] = mappingdata.slope[0]
                    slope.attrib['Max'] = mappingdata.slope[1]
                    mapping.append(slope)
                if all(mappingdata.latitude):
                    latitude = ET.Element('Latitude')
                    latitude.attrib['Min'] = mappingdata.latitude[0]
                    latitude.attrib['Max'] = mappingdata.latitude[1]
                    mapping.append(latitude)
                if all(mappingdata.longitude):
                    longitude = ET.Element('Longitude')
                    longitude.attrib['Min'] = mappingdata.longitude[0]
                    longitude.attrib['Max'] = mappingdata.longitude[1]
                    mapping.append(longitude)

                for item in mappingdata.mapping_items:
                    i = ET.Element('Item')
                    i.attrib['Type'] = item[0]
                    i.attrib['Subtype'] = item[1]
                    i.attrib['Density'] = item[2]
                    i.attrib['MaxRoll'] = item[3]
                    mapping.append(i)

                itemgroup.append(mapping)
            root.append(itemgroup)

        indent(root)
        ET.ElementTree(root).write(outfile, xml_declaration=True, method="xml", encoding="UTF-8")


class GrowableItemGroupSheetHandler(SheetCon):
    def __init__(self):
        super(GrowableItemGroupSheetHandler, self).__init__()
        self.open('Growable/Farmable/Tree Env Items')

    def get_growable_items(self, worksheet='GrowableEnvironmentItems', is_farmable=False):
        growable_ws = self.ss.worksheet(worksheet)
        vals = growable_ws.get_all_values()
        headers, vals = vals[1], vals[2:]
        expected = ['Farmable Item', 'DeadState', 'MaxSlope', 'Step Name', 'StartingProbability',
                    'ModelCollectionSubtypeId', 'NextStep', 'TimeToNextStep', '', 'Name', 'Next Step',
                    'Item Type', 'Item Subtype', 'Min', 'Max', '', 'Name', 'Next Step', 'Item Type',
                    'Item Subtype', 'Min', 'Max']

        if headers != expected and headers != expected[:1] + expected[3:]:
            print('Something changed with the environment item group definition headers!', headers)
            return

        growth_steps = defaultdict(list)
        farmable_data = {}
        for row in vals:
            if is_farmable:
                # farming spreadsheet adds more columns, remove these so indicies can stay
                farmable_data[row[0]] = (row.pop(1), row.pop(1))  # deadstate, maxslope

            step = GrowableItem.GrowthStep()
            step.name = row[1]
            step.probability = row[2]
            step.model_collection = row[3]
            step.next_step = row[4]

            step_data = row[5].strip().split(' ')
            if len(step_data) == 2:
                step_time, step_interval = step_data
                step.next_step_time = step_time
                step.step_interval = step_interval
            else:
                step.next_step_time = row[5]

            actions = []
            if row[7]:
                a = GrowableItem.Actions()
                a.name = row[7]
                a.next_step = row[8]
                a.type = row[9]
                a.subtype = row[10]
                a.min = row[11]
                a.max = row[12]
                actions.append(a)
            if row[14]:
                b = GrowableItem.Actions()
                b.name = row[14]
                b.next_step = row[15]
                b.type = row[16]
                b.subtype = row[17]
                b.min = row[18]
                b.max = row[19]
                actions.append(b)

            step.actions = actions
            growth_steps[row[0]].append(step)

        growable_items = []
        for growable_subtype, steps in growth_steps.items():
            growable = GrowableItem(type="MyObjectBuilder_GrowableEnvironmentItemDefinition", subtype=growable_subtype)
            growable.growthsteps = steps

            if is_farmable:
                growable.dead_state, growable.max_slope = farmable_data[growable_subtype]
            growable_items.append(growable)

        return growable_items

    def write_growable_items(self, growable_items, outfile):
        root = ET.Element('Definitions')
        for data in growable_items:
            growable = ET.Element('Definition')
            growable.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] = 'VR.EI.GrowableEnvironmentItem'
            id = ET.Element('Id')
            id.attrib['Type'] = data.type
            id.attrib['Subtype'] = data.subtype
            growable.append(id)

            if data.dead_state:
                ds = ET.Element('DeadState')
                ds.text = data.dead_state
                growable.append(ds)

            growth_steps = ET.Element('GrowthSteps')
            if data.growthsteps:
                for step in data.growthsteps:
                    growth_step = ET.Element('GrowthStep')
                    growth_step.attrib['Name'] = step.name
                    if step.probability:
                        growth_step.attrib['StartingProbability'] = step.probability

                    if step.model_collection:
                        models = ET.Element('ModelCollectionSubtypeId')
                        models.text = step.model_collection
                        growth_step.append(models)

                    if step.next_step:
                        next = ET.Element('NextStep')
                        next.text = step.next_step
                        growth_step.append(next)

                    if step.next_step_time:
                        time_to = ET.Element('TimeToNextStep')
                        time_to.attrib[step.step_interval.title()] = step.next_step_time
                        growth_step.append(time_to)

                    if step.actions:
                        actions = ET.Element('Actions')
                        for step_action in step.actions:
                            action = ET.Element('Action')
                            action.attrib['Name'] = step_action.name
                            if step_action.next_step:
                                action.attrib['NextStep'] = step_action.next_step

                            id = ET.Element('Id')
                            id.attrib['Type'] = step_action.type
                            id.attrib['Subtype'] = step_action.subtype
                            action.append(id)

                            if step_action.min:
                                action_min = ET.Element('Min')
                                action_min.text = step_action.min
                                action.append(action_min)

                            if step_action.max:
                                action_max = ET.Element('Max')
                                action_max.text = step_action.max
                                action.append(action_max)

                            actions.append(action)
                        growth_step.append(actions)
                    growth_steps.append(growth_step)

            growable.append(growth_steps)

            if data.max_slope:
                ms = ET.Element('MaxSlope')
                ms.text = data.max_slope
                growable.append(ms)

            root.append(growable)

            indent(root)
            ET.ElementTree(root).write(outfile, xml_declaration=True, method="xml", encoding="UTF-8")
