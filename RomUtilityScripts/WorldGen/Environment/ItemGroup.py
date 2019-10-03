
class ItemGroup(object):
    def __init__(self, name="", density=None, lod_start=None, lod_end=None):
        self.name = name
        self.density = density
        self.lod = (lod_start, lod_end)
        self.mappings = []

    class Mapping(object):
        def __init__(self):
            self.biomes = ()  # Tuple, for immutability
            self.materials = ()  # Tuple, for immutability
            self.slope = None  # Tuple (min, max)
            self.height = None  # Tuple (min, max)
            self.latitude = None  # Tuple (min, max)
            self.longitude = None  # Tuple (min, max)
            self.mapping_items = []

        @property
        def unique_id(self):
            return (self.biomes, self.materials, self.slope,
                    self.height, self.latitude, self.longitude)


class SS_Item(object):
    biomes = ()
    materials = ()
    slope = None
    height = None
    latitude = None
    longitude = None
    item_type = None
    item_subtype = None
    item_density = 0
    item_maxroll = 0

    def __repr__(self):
        return f"<{self.item_subtype}, {self.item_density}>"

    @property
    def unique_id(self):
        return (self.item_type, self.item_subtype, self.item_density, self.item_maxroll)
