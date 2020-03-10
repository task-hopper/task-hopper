class Carrot(object):
    def bind_tasks(self, task_ref):
        self.task_ref = task_ref

    def patch_task(self, tasks):
        for task,func in tasks:
            self.task_ref[task].patch(func)
