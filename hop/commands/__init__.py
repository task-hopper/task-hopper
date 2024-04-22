class Command(object):
    def __init__(self, alias=None, hhelp=None):
        super().__init__()
        self.composer = None
        self.alias = alias
        self.help = hhelp
        self.additional_args = []

    def _bootstrap(self, *, composer, subparsers, tasks=None):
        self.composer = composer
        self.task_ref = tasks

        help_msg = self.help if self.help else ""
        self.parser = subparsers.add_parser(
            self.alias, help=help_msg)

    def push_task(self, task, *args, **kwargs):
        self.task_ref[task].stage(*args, **kwargs)

    def setup_command(self):
        pass

    def process_command(self, parsed_args):
        raise NotImplementedError
