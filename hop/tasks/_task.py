class Task():
    def __init__(self, composer=None):
        super().__init__()
        self.composer = composer

    def stage(self):
        pass

    @classmethod
    def patch(self, func):
        self.stage = func
