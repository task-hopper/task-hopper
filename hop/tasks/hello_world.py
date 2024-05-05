from core import (
    Task,
    composer,
)


class HelloWorld(Task):
    def stage(self):
        composer.add('info', 'Hello, World!')

