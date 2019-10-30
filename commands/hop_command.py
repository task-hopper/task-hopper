class HopCommand(object):
    def __init__(self):
        super().__init__()
        self.alias = None

    def setup_command(self, subparsers):
        raise NotImplementedError

    def process_command(self, parsed_args):
        raise NotImplementedError
