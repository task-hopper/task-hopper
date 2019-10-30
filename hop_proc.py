from carrot_bunch import CarrotBunch
from commands.hop_command import HopCommand
from config_handler import ConfigHandler
import argparse
import inspect
import pkgutil
import sys

# TODO roll into central load_module helper
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


def main():
    #  carrot_bunch = CarrotBunch('carrots')
    #  carrot_bunch.apply_all_carrots_on_value(5)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

    cmds = load_commands()
    for alias, cls in cmds.items():
        cls.setup_command(subparsers)

    parsed_args = parser.parse_args(sys.argv[1:])
    cmds[parsed_args.subparser_name].process_command(parsed_args)


if __name__ == '__main__':
    main()
