from .hop_command import HopCommand

class HopcmdRun(HopCommand):
    def __init__(self):
        self.alias = 'run'

    def setup_command(self, subparsers):
        to_parser = subparsers.add_parser(
            'run', help='runs commands')
        to_parser.add_argument(
            'script_name', help='whatever')

    def process_command(self, parsed_args):
        pass
        # TODO read in user commands, or from specified file.
        # read config file
        # find project
        # find run section
        # excecute run section
