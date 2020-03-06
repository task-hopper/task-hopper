from commands._hop_command import HopCommand
from composer import composer
from config_handler import configs
import inspect
import pkgutil
import types


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

def load_config_commands():
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

