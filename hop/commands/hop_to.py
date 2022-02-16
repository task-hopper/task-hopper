from ._hop_command import HopCommand
from config_handler import configs
from helpers.utils import apath
from os.path import exists

class To(HopCommand):
    def __init__(self):
        self.alias = 'to'

    def setup_command(self, subparsers):
        to_parser = subparsers.add_parser(
            'to', help='changes directory')

        to_parser.add_argument(
            'destination', help='specify project')

        to_parser.add_argument(
            '-v', '--verbose', help='verbosely change directory',
            action='store_const', const=True, dest='verbose')

    def process_command(self, parsed_args):
        # Unset the current project env vars before going to destination project
        if configs.current_project():
            self.push_task('ChangeEnv', action='unset')

        # prompt cd
        self.push_task('CD', project_name=parsed_args.destination)

        # export configured environment variables if autoload is enabled
        self.push_task('ChangeEnv', project_name=parsed_args.destination, env='autoload')

        # run user-defined shell commands upon switching to a project if configured
        self.push_task('AutoRun', project_name=parsed_args.destination, verbose=parsed_args.verbose)
