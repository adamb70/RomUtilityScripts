from WorldGen.VoxelMaterials.DataImporter import VoxelMaterialSheetHandler


def generate_material_groups(outfile='Output/MaterialGroups.sbc', handler=None):
    ss = VoxelMaterialSheetHandler() if not handler else handler
    ss.write_material_groups(ss.get_material_group_dict().values(), outfile)
    return outfile


def generate_voxel_materials(outfile='Output/VoxelMaterials.sbc', handler=None):
    ss = VoxelMaterialSheetHandler() if not handler else handler
    ss.write_voxel_materials(ss.get_voxel_materials_dict().values(), outfile)
    return outfile


def generate_mining_definitions(outfile='Output/MiningDefinitions.sbc', handler=None):
    ss = VoxelMaterialSheetHandler() if not handler else handler
    ss.write_mining_defs(ss.get_voxel_materials_dict().values(), outfile)
    return outfile


def generate_voxel_files():
    ss = VoxelMaterialSheetHandler()
    out1 = generate_material_groups(handler=ss)
    out2 = generate_voxel_materials(handler=ss)
    out3 = generate_mining_definitions(handler=ss)
    return out1, out2, out3
