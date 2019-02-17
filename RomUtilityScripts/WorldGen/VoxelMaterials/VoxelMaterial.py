
class VoxelMaterial(object):
    def __init__(self, subtype="", filename=None, physical_material="Grass", hardness=100, color_key=None, icon=None, walk_sound=None, mining__lowest_tier=None, mining__volume=64, texture_filename=None):
        self.subtype = subtype
        self.physical_material = physical_material
        self.hardness = str(hardness)
        self.color_key = color_key
        self.icon = icon
        self.walk_sound = walk_sound

        self.mining__lowest_tier = mining__lowest_tier
        self.mining__volume = mining__volume
        self.mining__items_dropped = []  # list of tuples (item, amount)
        self.texture_filename = filename
