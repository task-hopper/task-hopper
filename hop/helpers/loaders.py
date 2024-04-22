from commands import Command
from tasks import Task
from config_handler import configs
from helpers.utils import mergedicts
import inspect
import pkgutil
import types


def load_tasks(composer=None):
    tasks = {}
    imported_package = __import__('tasks', fromlist=['devnull'])
    for _, task_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not is_pkg:
            task_module = __import__(task_name, fromlist=['devnull'])
            cls_members = inspect.getmembers(task_module, inspect.isclass)
            for (_, c) in cls_members:
                if issubclass(c, Task) & (c is not Task):
                    tasks[c.__name__] = c(composer=composer)

    return tasks


# load core hop commands
def load_commands(composer=None, tasks=None):
    cmds = {}
    imported_package = __import__('commands', fromlist=['devnull'])
    for _, command_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not is_pkg:
            command_module = __import__(command_name, fromlist=['devnull'])
            cls_members = inspect.getmembers(command_module, inspect.isclass)
            for (_, c) in cls_members:
                if issubclass(c, Command) & (c is not Command):
                    cmd_cls = c()
                    cmd_cls.import_composer(composer=composer)
                    cmd_cls.bind_tasks(tasks)
                    cmds[cmd_cls.alias] = cmd_cls

    return cmds


# load configured commands
def load_configured_commands(composer=None):
    cmds = {}

    # get configuration
    global_commands = configs.configs.get('commands', {})
    current_project = configs.current_project()
    project_commands = {}
    if current_project:
        project_commands = configs.project_configs(current_project).get('commands', {})
    config_commands = mergedicts(global_commands, project_commands)

    # build commands
    for a, c in config_commands.items():
        command = Command(alias=a)
        help_msg = (c[:35] + '...') if len(c) > 35 else c

        def new_setup_command(_, subparsers, a=a, help_msg=help_msg):
            custom_parser = subparsers.add_parser(
                a, help=help_msg)
            #  custom_parser.add_argument('cmd_args', nargs=REMAINDER)
            custom_parser.set_defaults(cmd='default')

        def new_process_command(self, _, c=c):
            cmd_args = ' '.join(self.additional_args)
            composer.add('task', f'{c} {cmd_args}')

        command.setup_command = types.MethodType(new_setup_command, command)
        command.process_command = types.MethodType(new_process_command, command)

        cmds[a] = command

    return cmds

# load hop
def initialize_hop(composer=None):
    tasks = load_tasks(composer=composer)
    commands = load_commands(composer=composer, tasks=tasks)

    return {**commands, **load_configured_commands(composer=composer)}
