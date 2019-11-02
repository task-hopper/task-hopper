import carrot_bunch

class SayIt(carrot_bunch.Carrot):
    def __init__(self):
        super().__init__()
        self.description = 'SayIt function'

    def perform_operation(self, argument):
        return argument
