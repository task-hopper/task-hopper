from ._hop_command import HopCommand

class Env(HopCommand):
    def __init__(self):
        self.alias = 'env'

    def setup_command(self, subparsers):
        env_parser = subparsers.add_parser(
            'env', help="export specified environment's variables")

        env_parser.add_argument(
            'environment', nargs='?', help='the environment to set variables for')

        env_parser.add_argument(
            '-l', '--list', help='list configured environments for current project',
            action='store_const', const=True, dest='list_envs')

        env_parser.add_argument(
            '-v', '--verbose', help='verbosely change environment',
            action='store_const', const=True, dest='verbose')

    def process_command(self, parsed_args):
        self.push_task('ChangeEnv', env=parsed_args.environment, list_envs=parsed_args.list_envs, verbose=parsed_args.verbose)
