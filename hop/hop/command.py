class Command(object):
    def __init__(self, alias=None, help=""):
        super().__init__()
        self.carrot = None
        self.composer = None
        self.alias = alias
        self.help = help
        self.additional_args = []

    def _bootstrap(self, *, composer, subparsers, tasks=None, carrot=None):
        self.carrot = carrot
        self.composer = composer
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

