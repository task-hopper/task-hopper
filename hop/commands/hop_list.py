from ._hop_command import HopCommand
from tasks.list_projects import ListProjects


class List(HopCommand):
    def __init__(self):
        self.alias = 'list'

    def setup_command(self, subparsers):
        list_parser = subparsers.add_parser(
            'list', help='lists configured projects')

        list_parser.add_argument(
            '--no-color', help='do not use colors in output',
            action='store_const', const=True, dest='no_color')

    def process_command(self, parsed_args):
        self.push_task('ListProjects', no_color=parsed_args.no_color)
