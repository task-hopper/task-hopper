from th import Command


class ToCommand(Command):
    def __init__(self):
        self.alias = 'to'
        self.help = 'cd to project directory'

    def setup_command(self):
        self.parser.add_argument(
            'destination', help='specify project')

    def process_command(self, parsed_args):
        # Unset the current project env vars before going to destination project
        #  configs = self.configs
        #  if configs.current_project():
            #  self.push_task('ChangeEnv', action='unset')
        # prompt cd
        self.push_task('CD', project_name=parsed_args.destination)
        # export configured environment variables if autoload is enabled
        self.push_task('ChangeEnv', project_name=parsed_args.destination, env='autoload')
