class HopCommand(object):
    def __init__(self, alias=None):
        super().__init__()
        self.alias = alias

    def setup_command(self, subparsers):
        raise NotImplementedError

    def process_command(self, parsed_args):
        raise NotImplementedError
