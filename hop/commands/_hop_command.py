class HopCommand(object):
    def __init__(self, alias=None):
        super().__init__()
        self.alias = alias
        self.composer = None

    def import_composer(self, composer):
        self.composer = composer

    def bind_tasks(self, task_ref):
        self.task_ref = task_ref

    def bind_carrot(self, carrot):
        self.carrot = carrot

    def push_task(self, task, *args, **kwargs):
        self.task_ref[task].stage(*args, **kwargs)

    def setup_command(self, subparsers):
        raise NotImplementedError

    def process_command(self, parsed_args):
        raise NotImplementedError
