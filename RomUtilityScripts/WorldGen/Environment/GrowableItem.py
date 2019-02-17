
class GrowableItem(object):
    def __init__(self, type="", subtype=""):
        self.type = type
        self.subtype = subtype
        self.dead_state = None
        self.max_slope = None
        self.growthsteps = []

    class GrowthStep(object):
        def __init__(self):
            self.name = None
            self.probability = None
            self.next_step = None
            self.next_step_time = None
            self.step_interval = "Hours"
            self.model_collection = None
            self.actions = []

    class Actions(object):
        def __init__(self):
            self.name = None
            self.next_step = None
            self.type = None
            self.subtype = None
            self.min = None
            self.max = None

