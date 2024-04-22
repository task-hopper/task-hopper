from tasks import Task


class HelloWorld(Task):
    def stage(self):
        self.composer.add('message', 'Hello, World!')
