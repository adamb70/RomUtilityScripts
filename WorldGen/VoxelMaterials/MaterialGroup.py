
class MaterialGroup(object):
    def __init__(self, name="", value=None):
        self.name = name
        self.value = value
        self.rules = []

    class Rule(object):
        def __init__(self):
            self.layers = []
            self.slope = None  # Tuple (min, max)
            self.height = None  # Tuple (min, max)


