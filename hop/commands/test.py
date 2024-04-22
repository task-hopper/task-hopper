from commands import Command


class Foo(Command):
    def __init__(self):
        self.alias = 'foo'
        self.help = 'It says the thing'

    def process_command(self, parsed_args):
        self.push_task('HelloWorld')
