from collections import defaultdict
import xml.etree.ElementTree as ET

from ...RomUtilityScriptsBase.SheetConnector import SheetCon
from ...RomUtilityScriptsBase.Utils import indent
from .MaterialGroup import MaterialGroup
from .VoxelMaterial import VoxelMaterial


class VoxelMaterialSheetHandler(SheetCon):
    def __init__(self):
        super(VoxelMaterialSheetHandler, self).__init__()
        self.open('Voxel Material Groups')

    def get_material_group_dict(self):
        mat_group_ws = self.ss.worksheet('Material groups')
        vals = mat_group_ws.get_all_values()
        headers, vals = vals[0], vals[1:]
        expected = ['Rules', 'Region', 'voxel layer', 'Depth', 'voxel layer', 'Depth', 'voxel layer', 'Depth', 'voxel layer', 'Depth', 'voxel layer', 'Depth', 'voxel layer', 'Depth', 'Material Group', 'description', 'Completed in WM', 'slope range', 'Height range']
        if headers != expected:
            print('Something changed with the material group headers!', headers)
            return

        mat_groups = {}
        for row in vals:
            if not any(row):
                continue
            matgroup = mat_groups.get(row[0], None)
            if not matgroup:
                matgroup = MaterialGroup(row[0], row[14])
                mat_groups[row[0]] = matgroup

            rule = MaterialGroup.Rule()
            layers = []
            for mat, depth in zip(row[2:14:2], row[3:15:2]):
                if not mat:
                    continue
                layers.append((mat, depth))

            rule.layers = layers
            rule.slope = tuple(row[17].split('-')) if row[17] else ''
            rule.height = tuple(row[18].split('-')) if row[18] else ''

            matgroup.rules.append(rule)

        return mat_groups

    def write_material_groups(self, mat_groups, outfile):
        root = ET.Element('ComplexMaterials')
        for matgroupdata in mat_groups:
            matgroup = ET.Element('MaterialGroup')
            matgroup.attrib['Name'] = matgroupdata.name
            if matgroupdata.value:
                matgroup.attrib['Value'] = matgroupdata.value
            for r in matgroupdata.rules:
                rule = ET.Element('Rule')
                layers = ET.Element('Layers')
                for lmat, ldepth in r.layers:
                    layer = ET.Element('Layer')
                    layer.attrib['Material'] = lmat
                    layer.attrib['Depth'] = ldepth
                    layers.append(layer)
                rule.append(layers)
                if r.slope:
                    slope = ET.Element('Slope')
                    slope.attrib['Min'] = r.slope[0]
                    slope.attrib['Max'] = r.slope[1]
                    rule.append(slope)
                if r.height:
                    height = ET.Element('Height')
                    height.attrib['Min'] = r.height[0]
                    height.attrib['Max'] = r.height[1]
                    rule.append(height)
                matgroup.append(rule)
            root.append(matgroup)

        indent(root)
        ET.ElementTree(root).write(outfile, xml_declaration=True, method="xml", encoding="UTF-8")

    def get_voxel_materials_dict(self):
        voxel_mat_ws = self.ss.worksheet('Voxel materials')
        vals = voxel_mat_ws.get_all_values()
        headers, vals = vals[0], vals[1:]
        expected = ['Voxel Material', 'Description', 'Subtype', 'Filename', 'PhysicalMaterialName', 'Hardness', 'ColorKey', 'Icon', 'Walk Sound', 'Lowest tier mining tool', 'Volume', 'Item Dropped', 'Amount', 'Item Dropped', 'Amount']
        if headers != expected:
            print('Something changed with the voxel material headers!', headers)
            return

        voxel_mats = {}
        for row in vals:
            if not any(row):
                continue
            vm = VoxelMaterial(*row[2:11])
            if row[11]:  # check for `item dropped` value
                vm.mining__items_dropped.append((row[11], str(row[12])))
            if row[13]:
                vm.mining__items_dropped.append((row[13], str(row[14])))
            voxel_mats[row[2]] = vm

        return voxel_mats

    def write_voxel_materials(self, voxel_mats, outfile):
        root = ET.Element('Definitions')
        for voxel in voxel_mats:
            written_voxel = ET.Element('Definition')
            written_voxel.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] = "MyObjectBuilder_Dx11VoxelMaterialDefinition"

            id = ET.Element('Id')
            id.attrib['Type'] = "VoxelMaterialDefinition"
            id.attrib['Subtype'] = voxel.subtype
            written_voxel.append(id)

            if voxel.physical_material:
                physmat = ET.Element('PhysicalMaterialName')
                physmat.text = voxel.physical_material
                written_voxel.append(physmat)

            spec_power = ET.Element('SpecularPower')
            spec_shininess = ET.Element('SpecularShininess')
            spec_power.text = str(1)
            spec_shininess.text = str(0.1)
            written_voxel.append(spec_power)
            written_voxel.append(spec_shininess)

            if voxel.hardness:
                hardness = ET.Element('Hardness')
                hardness.text = voxel.hardness
                written_voxel.append(hardness)
            if voxel.color_key:
                ck = ET.Element('ColorKey')
                ck.attrib['Hex'] = voxel.color_key
                written_voxel.append(ck)
            if voxel.icon:
                icon = ET.Element('Icon')
                icon.text = voxel.icon
                written_voxel.append(icon)
            if voxel.texture_filename:
                cm = ET.Element('ColorMetalXZnY')
                ng = ET.Element('NormalGlossXZnY')
                add = ET.Element('ExtXZnY')
                if voxel.texture_filename.endswith('.dds'):
                    cm.text = ng.text = add.text = voxel.texture_filename
                else:
                    cm.text = 'Textures\Voxels\\' + voxel.texture_filename + '_cm.dds'
                    ng.text = 'Textures\Voxels\\' + voxel.texture_filename + '_ng.dds'
                    add.text = 'Textures\Voxels\\' + voxel.texture_filename + '_add.dds'
                written_voxel.extend([cm, ng, add])

            root.append(written_voxel)

        indent(root)
        ET.ElementTree(root).write(outfile, xml_declaration=True, method="xml", encoding="UTF-8")

    def write_mining_defs(self, voxel_mats, outfile):
        # group mining defs by lowest tier tool
        tiers = defaultdict(list)
        for voxel in voxel_mats:
            tiers[voxel.mining__lowest_tier].append(voxel)

        root = ET.Element('Definitions')
        for tier, voxel_mats in tiers.items():
            mining_def = ET.Element('Definition')
            mining_def.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] = "MyObjectBuilder_VoxelMiningDefinition"

            id = ET.Element('Id')
            id.attrib['Type'] = "VoxelMiningDefinition"
            id.attrib['Subtype'] = tier
            mining_def.append(id)

            for voxel in voxel_mats:
                entry = ET.Element('Entry')
                entry.attrib['VoxelMaterial'] = voxel.subtype
                entry.attrib['Volume'] = voxel.mining__volume
                for mined_item, amount in voxel.mining__items_dropped:
                    item = ET.Element('MinedItem')
                    item.attrib['Type'] = "InventoryItem"
                    item.attrib['Subtype'] = mined_item
                    item.attrib['Amount'] = amount
                    entry.append(item)
                mining_def.append(entry)

            root.append(mining_def)

        indent(root)
        ET.ElementTree(root).write(outfile, xml_declaration=True, method="xml", encoding="UTF-8")
