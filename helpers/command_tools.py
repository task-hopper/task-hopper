from commands._hop_command import HopCommand
from composer import composer
from config_handler import configs
import inspect
import pkgutil


# decorator for implementing before / after commands
#  def command_hooks(func, enabled=True):
    #  def wrapper(*args, **kwargs):
        #  composer.add('message', 'Running before...')
        #  func(*args, **kwargs)
        #  composer.add('message', 'Running after...')

    #  return wrapper


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
def get_config_command(command_arg):
    current_project = configs.current_project()
    config_command = None

    # use project-specific command if configured
    if current_project:
        config_command = configs.project_configs(current_project).get('commands', {}).get(command_arg)

    # use global command if configured
    if not config_command:
        config_command = configs.configs.get('commands', {}).get(command_arg)

    return config_command 
