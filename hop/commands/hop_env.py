from ._hop_command import HopCommand
from tasks.change_env import ChangeEnv

class Env(HopCommand):
    def __init__(self):
        self.alias = 'env'

    def setup_command(self, subparsers):
        env_parser = subparsers.add_parser(
            'env', help="export specified environment's variables")
         
        env_parser.add_argument('environment', help='the environment to get variables for')

    def process_command(self, parsed_args):
        ChangeEnv.stage(env=parsed_args.environment)
