import inspect
import pkgutil
import sys
import types
from hop import Carrot, Command, Task
from config_handler import configs
from helpers.utils import apath, mergedicts


CARROT_PATH = apath('~/.hop/carrots')

sys.path.append(CARROT_PATH)



def _issubclass(cls_member, parent_cls):
    return (
        issubclass(cls_member[1], parent_cls)
        and
        cls_member[1] is not parent_cls
    )


def load_carrots(composer=None, subparsers=None):
    bunch = {}

    # Iterate through each carrot plugin in the "carrots" folder
    for _1, carrot_name, is_pkg1 in pkgutil.iter_modules([CARROT_PATH]):
        if is_pkg1:
            carrot_package = __import__(carrot_name, fromlist=['devnull'])
            carrot_members = [
                m
                for m
                in inspect.getmembers(carrot_package, inspect.isclass)
                if _issubclass(m, Carrot)
            ]
            # Make sure there is only 1 Carrot subclass defined for the carrot plugin
            if len(carrot_members) > 1:
                composer.add('error', f"Carrot Error: {carrot_name} module has multiple members of Carrot class when one is required.")
            if not len(carrot_members):
                composer.add('error', f"Carrot Error: {carrot_name} module missing Carrot class member.")

            # Start carrot metadata dict
            carrot = None
            for (_, c) in carrot_members:
                carrot = {
                    'name': c.__name__,
                    'klass': c(),
                    'tasks': {},
                    'commands': {}
                }
            # Iterate through carrot submodules
            for _2, carrot_submodule_name, is_pkg2 in pkgutil.iter_modules(carrot_package.__path__, carrot_package.__name__ + '.'):
                # Allow tasks and commands submodules only
                allowed_submodules = [ f"{carrot_name}.{asm}" for asm in ['tasks', 'commands'] ]
                if is_pkg2 and carrot_submodule_name in allowed_submodules:
                    carrot_submodule = __import__(carrot_submodule_name, fromlist=['devnull']) 
                    carrot_submodule_members = [
                        m
                        for m
                        in inspect.getmembers(carrot_submodule, inspect.isclass)
                        if _issubclass(m, Command) or _issubclass(m, Task)
                    ]

                    for (_, c) in carrot_submodule_members:
                        base_modules = [i.__name__ for i in c.__bases__]
                        if 'Task' in base_modules:
                            task = c()
                            task._bootstrap(composer=composer, carrot=carrot_name)
                            carrot['tasks'][c.__name__] = task
                        if 'Command' in base_modules:
                            command = c()
                            command._bootstrap(
                                carrot=carrot_name,
                                composer=composer,
                                subparsers=subparsers
                            )
                            carrot['commands'][command.alias] = command
            bunch[carrot_name] = carrot

    return bunch


def load_tasks(composer=None):
    tasks = {}
    imported_package = __import__('tasks', fromlist=['devnull'])
    for _, task_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not is_pkg:
            task_module = __import__(task_name, fromlist=['devnull'])
            cls_members = inspect.getmembers(task_module, inspect.isclass)
            for cls in cls_members:
                if _issubclass(cls, Task):
                    (_, c) = cls
                    task = c()
                    task._bootstrap(composer=composer)
                    tasks[c.__name__] = task

    return tasks


# load core Task Hopper commands
def load_core_commands(*, composer, tasks, subparsers):
    cmds = {}
    imported_package = __import__('commands', fromlist=['devnull'])
    for _, command_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not is_pkg:
            command_module = __import__(command_name, fromlist=['devnull'])
            cls_members = inspect.getmembers(command_module, inspect.isclass)
            for cls in cls_members:
                if _issubclass(cls, Command):
                    (_, c) = cls
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
        command = Command(alias=a, help=help_msg)

        def new_process_command(self, _, c=c):
            cmd_args = ' '.join(self.additional_args)
            composer.add('task', f'{c} {cmd_args}')

        command.process_command = types.MethodType(new_process_command, command)

        command._bootstrap(composer=composer, subparsers=subparsers)
        cmds[a] = command

    return cmds


# load Task Hopper
def initialize_task_hopper(composer=None, subparsers=None):
    tasks = load_tasks(composer=composer)
    core_commands = load_core_commands(composer=composer, tasks=tasks, subparsers=subparsers)
    configured_commands = load_configured_commands(composer=composer, subparsers=subparsers)
    carrot_bunch = load_carrots(composer=composer, subparsers=subparsers)

    commands = {**core_commands, **configured_commands}

    for _, meta in carrot_bunch.items():
        # bind tasks
        # TODO: handle task name collisions
        task_ref = {**tasks, **meta['tasks']}

        # bind tasks to commands
        for alias, cls in meta['commands'].items():
            cls._bind_tasks(task_ref)
            # TODO: handle command alias collisions
            commands[alias] = cls

    for _, cls in commands.items():
        cls.setup_command()

    return commands
