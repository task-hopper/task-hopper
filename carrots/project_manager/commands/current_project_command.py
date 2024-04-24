from hop import Command


class CurrentProjectCommand(Command):
    def __init__(self):
        self.alias = 'current'
        self.help = 'show current project details'

    def setup_command(self):
        self.parser.set_defaults(current_type='alias')
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(
            '-n', '--name', help='show full project name', 
            action='store_const', const='name', dest='current_type')
        group.add_argument(
            '-p', '--path', help='show project path', 
            action='store_const', const='path', dest='current_type')

    def process_command(self, parsed_args):
        self.push_task('GetProjectDetail', detail_type=parsed_args.current_type)

