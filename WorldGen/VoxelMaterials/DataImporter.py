from collections import defaultdict
import xml.etree.ElementTree as ET

import Utils
from SheetConnector import SheetCon
from WorldGen.VoxelMaterials.MaterialGroup import MaterialGroup


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

    def write_material_groups(self, mat_groups):
        root = ET.Element('ComplexMaterials')
        for matgroupdata in mat_groups:
            matgroup = ET.Element('MaterialGroup')
            matgroup.attrib['Name'] = matgroupdata.name
            if matgroupdata.value:
                matgroup.attrib['Value'] = matgroupdata.value
            for r in matgroupdata.rules:
                rule = ET.Element('Rule')
                for lmat, ldepth in r.layers:
                    layer = ET.Element('Layer')
                    layer.attrib['Material'] = lmat
                    layer.attrib['Depth'] = ldepth
                    rule.append(layer)
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

        Utils.indent(root)
        ET.ElementTree(root).write('Output/MaterialGroups.sbc', xml_declaration=True, method="xml", encoding="UTF-8")


ss = VoxelMaterialSheetHandler()

print(ss.write_material_groups(ss.get_material_group_dict().values()))