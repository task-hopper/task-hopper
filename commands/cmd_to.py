from .hop_command import HopCommand
from config_handler import ConfigHandler

class CmdTo(HopCommand):
    def __init__(self):
        self.alias = 'to'

    def setup_command(self, subparsers):
        to_parser = subparsers.add_parser(
            'to', help='changes directory')
        to_parser.add_argument(
            'project', help='specify project to switch to')

    def process_command(self, parsed_args):
        configs = ConfigHandler()
        project_configs = configs.project_configs(parsed_args.project)
        print(f'cd {project_configs.get("path")}')



