
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
