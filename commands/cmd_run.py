from helpers.command_tools import compose
from ._hop_command import HopCommand
from config_handler import configs

class HopcmdRun(HopCommand):
    def __init__(self):
        self.alias = 'run'

    def setup_command(self, subparsers):
        to_parser = subparsers.add_parser(
            'run', help='runs commands')
        to_parser.add_argument(
            'command_alias', help='the configured command alias')

    def process_command(self, parsed_args):
        current_project = configs.current_project()

        if current_project:
            project_configs = configs.project_configs(current_project)

            command = (
                project_configs
                .get('commands', {})
                .get(parsed_args.command_alias, None))

            if command is None:
                compose('error', f"'{parsed_args.command_alias}' is not a configured command")
            else:
                compose('instructions', command)
        else:
            compose('error', 'Unable to run command. Not in a project.')

