class Task():
    def __init__(self, composer=None):
        super().__init__()
        self.composer = composer

    def stage(self):
        pass

    @classmethod
    def patch(self, func):
        self._stage = self.stage
        self.stage = func
