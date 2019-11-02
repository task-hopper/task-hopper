from helpers.command_tools import compose
from ._hop_command import HopCommand
from config_handler import configs
from builders.cd import CD
from builders.env import Env

class CmdTo(HopCommand):
    def __init__(self):
        self.alias = 'to'
        self.command_result = []

    def setup_command(self, subparsers):
        to_parser = subparsers.add_parser(
            'to', help='changes directory')
        to_parser.add_argument(
            'project', help='specify project to switch to')

    def process_command(self, parsed_args):
        # prompt cd
        # TODO decide whether to limit builder responses to list only
        self.command_result.append(CD.build(project_name=parsed_args.project))
        # export configured environment variables if autoload is enabled
        self.command_result.extend(Env.build(project_name=parsed_args.project))
        compose('instructions', self.command_result)

