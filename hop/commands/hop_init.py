from ._hop_command import HopCommand


class Init(HopCommand):
    def __init__(self):
        self.alias = 'init'

    def setup_command(self, subparsers):
        current_parser = subparsers.add_parser(
            'init', help='add project to ~/.hoprc')

        current_parser.add_argument(
            '-d', '--directory', help='root directory of project')

        current_parser.add_argument(
            '-n', '--name', help='name of project')

        current_parser.add_argument(
            '-a', '--alias', help='(short) alias for project')

        current_parser.add_argument(
            '-c', '--create-hop-file', help='create default .hop file for project',
            action='store_const', const=True, dest='create_hop_file')

    def process_command(self, parsed_args):
        self.push_task('InitConfig',
                       directory=parsed_args.directory,
                       name=parsed_args.name,
                       alias=parsed_args.alias,
                       create_hop_file=parsed_args.create_hop_file)
