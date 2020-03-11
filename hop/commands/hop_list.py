from ._hop_command import HopCommand
from tasks.list_projects import ListProjects


class List(HopCommand):
    def __init__(self):
        self.alias = 'list'

    def setup_command(self, subparsers):
        subparsers.add_parser(
            'list', help='lists configured projects')

    def process_command(self, parsed_args):
        self.push_task('ListProjects')
