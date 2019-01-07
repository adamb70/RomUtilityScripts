from WorldGen.VoxelMaterials.DataImporter import VoxelMaterialSheetHandler


def generate_material_groups():
    ss = VoxelMaterialSheetHandler()
    ss.write_material_groups(ss.get_material_group_dict().values())


def generate_voxel_materials():
    ss = VoxelMaterialSheetHandler()
    ss.write_voxel_materials(ss.get_voxel_materials_dict().values())

def generate_mining_definitions():
    ss = VoxelMaterialSheetHandler()
    ss.write_mining_defs(ss.get_voxel_materials_dict().values())

generate_material_groups()
generate_voxel_materials()
generate_mining_definitions()
