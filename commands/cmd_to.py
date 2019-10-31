from helpers.response_formatter import compose
from .hop_command import HopCommand
from config_handler import ConfigHandler

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
        # load configs to get project path and prompt cd
        configs = ConfigHandler()
        project_configs = configs.project_configs(parsed_args.project)
        self.command_result.append(f'cd {project_configs.get("path")}')

        # export configured environment variables
        project_env = project_configs.get('env', {})
        autoload_type = project_env.get('autoload')
        if autoload_type:
            environments = [e for e in list(project_env.keys()) if e != 'autoload']
            for e in environments:
                if e in ['default', autoload_type]:
                    for var, val in project_env.get(e).items():
                        self.command_result.append(f'export {var}={val}')

        compose('instructions', self.command_result)

# TODO write class method to take in a list of commands as well as an output type, and handle the output
