class Builder():
    @classmethod
    def build(cls):
        pass

    @classmethod
    def patch(cls, func):
        cls.build = func
