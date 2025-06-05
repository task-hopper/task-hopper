class Command(object):
    """
    A base class intended to be inherited when creating commands for the CLI.
    Core commands and commands configured in the .hoprc are instances of this
    base class.

    Attributes
    ----------
    carrot : Carrot
        the `Carrot` this command belongs to. This is 'None' when this is a core
        command or a configured command.
    alias : str
        The alias to be used in the CLI. (required)
    help : str
        The help text displayed when invoking the help command. (default is an
        empty string)

    Methods
    -------


    """
    def __init__(self, alias=None, help=""):
        super().__init__()
        self.carrot = None
        self.alias = alias
        self.help = help
        self.additional_args = []

    def _bootstrap(self, *, subparsers, tasks=None, carrot=None):
        self.carrot = carrot
        self.task_ref = tasks

        self.parser = subparsers.add_parser(
            self.alias, help=self.help)

    def _bind_tasks(self, task_ref):
        self.task_ref = task_ref

    def push_task(self, task, *args, **kwargs):
        self.task_ref[task].stage(*args, **kwargs)

    def setup_command(self):
        pass

    def process_command(self, parsed_args):
        raise NotImplementedError

