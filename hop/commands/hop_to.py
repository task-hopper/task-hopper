from ._hop_command import HopCommand
from composer import composer
from config_handler import configs
from helpers.utils import apath
from os.path import exists
from tasks.cd import CD
from tasks.change_env import ChangeEnv

class To(HopCommand):
    def __init__(self):
        self.alias = 'to'

    def setup_command(self, subparsers):
        to_parser = subparsers.add_parser(
            'to', help='changes directory')
        to_parser.add_argument(
            'destination', help='specify project/directory to switch to')

    def process_command(self, parsed_args):
        is_dir = exists(apath(parsed_args.destination))
        if is_dir:
            CD.stage(directory=apath(parsed_args.destination))
        else:
            # prompt cd
            CD.stage(project_name=parsed_args.destination)
            # export configured environment variables if autoload is enabled
            ChangeEnv.stage(project_name=parsed_args.destination, env='autoload')