from commands import Command


class Foo(Command):
    def __init__(self):
        self.alias = 'foo'

    def setup_command(self, subparsers):
        foo_parser = subparsers.add_parser(
            'foo', help='says the thing')

    def process_command(self, parsed_args):
        self.push_task('HelloWorld')
