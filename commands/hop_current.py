from ._hop_command import HopCommand
from composer import composer
from config_handler import configs
from tasks.get_project_detail import GetProjectDetail

class Project(HopCommand):
    def __init__(self):
        self.alias = 'current'

    def setup_command(self, subparsers):
        current_parser = subparsers.add_parser(
            'current', help='get current project name')
        current_parser.set_defaults(current_type='alias')
        group = current_parser.add_mutually_exclusive_group()
        group.add_argument(
            '-n', '--name', help='show full project name', 
            action='store_const', const='name', dest='current_type')
        group.add_argument(
            '-p', '--path', help='show project path', 
            action='store_const', const='path', dest='current_type')

    def process_command(self, parsed_args):
        GetProjectDetail.stage(detail_type=parsed_args.current_type)

