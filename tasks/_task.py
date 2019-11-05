class Task():
    @classmethod
    def stage(cls):
        pass

    @classmethod
    def patch(cls, func):
        cls.build = func
