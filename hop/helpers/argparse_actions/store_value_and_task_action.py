import argparse

class StoreValueAndTaskAction(argparse.Action):
    def __init__(self, option_strings, dest, task_action=None, **kwargs):
        self.task_action = task_action
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            setattr(namespace, 'task_action', self.task_action)
            setattr(namespace, self.dest, values)

