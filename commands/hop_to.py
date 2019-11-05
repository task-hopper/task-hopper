from tasks.cd import CD
from tasks.env import Env
from composer import composer
from config_handler import configs
from ._hop_command import HopCommand

class To(HopCommand):
    def __init__(self):
        self.alias = 'to'

    def setup_command(self, subparsers):
        to_parser = subparsers.add_parser(
            'to', help='changes directory')
        to_parser.add_argument(
            'project', help='specify project to switch to')

    def process_command(self, parsed_args):
        # prompt cd
        CD.stage(project_name=parsed_args.project)

        # export configured environment variables if autoload is enabled
        Env.stage(project_name=parsed_args.project)
