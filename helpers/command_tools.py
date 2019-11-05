from commands._hop_command import HopCommand
from composer import composer
from config_handler import configs
import inspect
import pkgutil

# decorator for implementing before / after commands
def command_hooks(func, enabled=True):
    def wrapper(*args, **kwargs):
         
        composer.add('message', 'Running before...')
        func(*args, **kwargs)
        composer.add('message', 'Running after...')

    return wrapper


def load_commands():
    cmds = {}
    imported_package = __import__('commands', fromlist=['blah'])
    for _, command_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not is_pkg:
            command_module = __import__(command_name, fromlist=['blah'])
            cls_members = inspect.getmembers(command_module, inspect.isclass)
            for (_, c) in cls_members:
                if issubclass(c, HopCommand) & (c is not HopCommand):
                    cmd_cls = c()
                    cmds[cmd_cls.alias] = cmd_cls
    return cmds


# TODO rename this method
def check_command(command_arg):
    current_project = configs.current_project()
    configured_command = None

    if current_project:
        configured_command = configs.project_configs(current_project).get('commands', {}).get(command_arg)

    if not configured_command:
        configured_command = configs.configs.get('commands', {}).get(command_arg)

    if configured_command: 
        if isinstance(configured_command, dict):
            command = configured_command.get('command')
            composer.add('task', command)
        else:
            composer.add('task', configured_command)

        return True
