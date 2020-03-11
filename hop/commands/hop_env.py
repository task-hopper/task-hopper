from ._hop_command import HopCommand

class Env(HopCommand):
    def __init__(self):
        self.alias = 'env'

    def setup_command(self, subparsers):
        env_parser = subparsers.add_parser(
            'env', help="export specified environment's variables")
        env_parser.add_argument('environment', help='the environment to get variables for')

    def process_command(self, parsed_args):
        self.push_task('ChangeEnv', env=parsed_args.environment)
