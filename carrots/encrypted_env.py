import carrot_bunch
from tasks.env import Env

class EncryptedEnv(carrot_bunch.Carrot):
    def __init__(self):
        super().__init__()
        self.description = 'SayIt function'

    def perform_operation(self, argument):
        return argument
