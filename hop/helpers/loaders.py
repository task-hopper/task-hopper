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
def load_core_commands(*, composer, tasks, subparsers):
    cmds = {}
    imported_package = __import__('commands', fromlist=['devnull'])
    for _, command_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not is_pkg:
            command_module = __import__(command_name, fromlist=['devnull'])
            cls_members = inspect.getmembers(command_module, inspect.isclass)
            for (_, c) in cls_members:
                if issubclass(c, Command) & (c is not Command):
                    cmd_cls = c()
                    cmd_cls._bootstrap(
                        composer=composer,
                        tasks=tasks,
                        subparsers=subparsers
                    )
                    cmds[cmd_cls.alias] = cmd_cls

    return cmds


# load configured commands
def load_configured_commands(*, composer, subparsers):
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
        help_msg = (c[:35] + '...') if len(c) > 35 else c
        command = Command(alias=a, hhelp=help_msg)

        def new_process_command(self, _, c=c):
            cmd_args = ' '.join(self.additional_args)
            composer.add('task', f'{c} {cmd_args}')

        command.process_command = types.MethodType(new_process_command, command)

        command._bootstrap(composer=composer, subparsers=subparsers)
        cmds[a] = command

    return cmds

# load hop
def initialize_hop(composer=None, subparsers=None):
    tasks = load_tasks(composer=composer)
    core_commands = load_core_commands(composer=composer, tasks=tasks, subparsers=subparsers)
    configured_commands = load_configured_commands(composer=composer, subparsers=subparsers)

    commands = {**core_commands, **configured_commands}

    for _, cls in commands.items():
        cls.setup_command()

    return commands
