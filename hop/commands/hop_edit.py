from ._hop_command import HopCommand


class Edit(HopCommand):
    def __init__(self):
        self.alias = 'edit'

    def setup_command(self, subparsers):
        current_parser = subparsers.add_parser(
            'edit', help='edit project configuration')

        current_parser.add_argument('project', nargs='?', help='the project whose configuration you want to edit')

        current_parser.add_argument(
            '-g', '--global', help='edit global configuration',
            action='store_const', const=True, dest='edit_global')

    def process_command(self, parsed_args):
        self.push_task('EditConfig', project_name=parsed_args.project, edit_global=parsed_args.edit_global)
