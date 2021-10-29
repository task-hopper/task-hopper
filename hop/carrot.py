from config_handler import configs
from helpers.utils import apath, camel_to_snake

class Carrot(object):
    def __init__(self):
        carrot_name = type(self).__name__
        self.data_dir = apath(f'~/.hop/lib/carrots/{camel_to_snake(carrot_name)}/data')
        self.configs = configs.carrot_configs(carrot_name)

    def bind_tasks(self, task_ref):
        self.task_ref = task_ref

    def patch_task(self, tasks):
        for task,func in tasks:
            self.task_ref[task].patch(func)

    # default task patcher
    def patch_tasks(self):
        return {}
