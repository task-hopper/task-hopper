from commands._hop_command import HopCommand
from tasks._task import Task
from config_handler import configs
from helpers.utils import apath
from os.path import isdir
import inspect
import pkgutil
import sys
import types

sys.path.append(apath('~/.hop/lib'))

def load_carrots(composer=None):
    bunch = {}

    imported_package = __import__('carrots', fromlist=['devnull'])
    for _1, bunch_name, is_pkg1 in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if is_pkg1:
            bunch_package = __import__(bunch_name, fromlist=['devnull'])
            carrot_members = [m for m in inspect.getmembers(bunch_package, inspect.isclass) if m[1].__module__.split('.')[0] == 'carrots']
            carrot = None
            for (_, c) in carrot_members:
                if 'Carrot' in [i.__name__ for i in c.__bases__]:
                    carrot =  {
                        'name': c.__name__,
                        'cklass': c,
                        'klass': c(),
                        'tasks': {},
                        'commands': {}
                    }
            for _2, carrot_name, is_pkg2 in pkgutil.iter_modules(bunch_package.__path__, bunch_package.__name__ + '.'):
                if not is_pkg2:
                    carrot_module = __import__(carrot_name, fromlist=['devnull'])
                    cls_members = [m for m in inspect.getmembers(carrot_module, inspect.isclass) if m[1].__module__.split('.')[0] == 'carrots'] 
                    for (_, c) in cls_members:
                        base_modules = [i.__name__ for i in c.__bases__]
                        if 'Task' in base_modules:
                            carrot['tasks'][c.__name__] = c(composer=composer)
                        if 'HopCommand' in base_modules:
                            cmd_cls = c()
                            cmd_cls.import_composer(composer=composer)
                            cmd_cls.bind_carrot(carrot=carrot['klass'])
                            carrot['commands'][cmd_cls.alias] = cmd_cls
            bunch[carrot['name']] = carrot

    return bunch


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
                if issubclass(c, HopCommand) & (c is not HopCommand):
                    cmd_cls = c()
                    cmd_cls.import_composer(composer=composer)
                    cmd_cls.bind_tasks(tasks)
                    cmds[cmd_cls.alias] = cmd_cls

    return cmds


# load configured commands
def load_configured_commands(composer=None):
    cmds = {}
    current_project = configs.current_project()
    if current_project:
        config_commands = configs.project_configs(current_project).get('commands', {})
        for a,c in config_commands.items():
            command = HopCommand(alias=a)
            help_msg = (c[:35] + '...') if len(c) > 35 else c
            def new_setup_command(self, subparsers, a=a, help_msg=help_msg):
                custom_parser = subparsers.add_parser(
                    a, help=help_msg)
                custom_parser.set_defaults(cmd='default')

            def new_process_command(self, parsed_args, c=c):
                composer.add('task', c)

            command.setup_command = types.MethodType(new_setup_command, command)
            command.process_command = types.MethodType(new_process_command, command)

            cmds[a] = command

    return cmds

# load hop
def initialize_hop(composer=None):
    carrots = load_carrots(composer=composer)
    tasks = load_tasks(composer=composer)
    commands = load_commands(composer=composer, tasks=tasks)

    # initialize carrots
    for carrot, attrs in carrots.items():
        # patch tasks
        patch_def = attrs['klass'].patch_tasks()
        for task, func in patch_def.items():
            tasks[task].patch(func)
        # bind tasks
        task_ref = {**tasks, **attrs['tasks']}
        for alias, klass in attrs['commands'].items():
            klass.bind_tasks(task_ref)
            commands[alias] = klass

    return {**commands, **load_configured_commands(composer=composer)}

