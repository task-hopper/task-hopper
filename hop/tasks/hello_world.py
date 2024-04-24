from hop import Task, THCallback


class HelloWorld(Task):
    def stage(self):
        self.composer.add('info', 'Hello, World!')

