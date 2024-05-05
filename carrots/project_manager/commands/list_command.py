from th import Command


class ListCommand(Command):
    def __init__(self):
        self.alias = 'list'
        self.help = 'list configured projects'

    def setup_command(self):
        self.parser.add_argument(
            '--no-color', help='do not use colors in output',
            action='store_const', const=True, dest='no_color')

    def process_command(self, parsed_args):
        self.push_task('ListProjects', no_color=parsed_args.no_color)
