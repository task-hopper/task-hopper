from ._hop_command import HopCommand
from helpers.argparse_actions.store_value_and_task_action import StoreValueAndTaskAction


class Env(HopCommand):
    def __init__(self):
        self.alias = 'env'

    def setup_command(self, subparsers):
        env_parser = subparsers.add_parser(
            'env', help="export specified environment's variables")

        group = env_parser.add_mutually_exclusive_group(required=True)

        group.add_argument(
            'environment', nargs='?', action=StoreValueAndTaskAction, task_action='set')

        group.add_argument(
            '-l', '--list', help='list configured environments for current project',
            action='store_const', const='list', dest='task_action')

        group.add_argument(
            '-u', '--unset', help='unsets the configured env vars for current project',
            action='store_const', const='unset', dest='task_action')

        env_parser.add_argument(
            '-v', '--verbose', help='verbosely change environment',
            action='store_const', const=True, dest='verbose')

    def process_command(self, parsed_args):
        self.push_task('ChangeEnv', action='unset', verbose=parsed_args.verbose)
        self.push_task('ChangeEnv', env=parsed_args.environment, action=parsed_args.task_action, verbose=parsed_args.verbose)
