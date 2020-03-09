#!/usr/bin/env python3

from composer import composer
from helpers.command_tools import load_config_commands, load_commands, load_carrot_commands
from helpers.utils import apath
import argparse
import sys

sys.path.append(apath('~/repos/personal/task-hopper'))

#  @command_hooks
def run_hop_command(command, parsed_args):
    command.process_command(parsed_args)

def main():
    # print directive before showing help message
    if sys.argv[-1] in ['-h', '--help']: print('__hop_message__')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

    cmds = {**load_commands(), **load_config_commands(), **load_carrot_commands()}
    for alias, cls in cmds.items():
        cls.setup_command(subparsers)

    parsed_args = parser.parse_args(sys.argv[1:])
    run_hop_command(cmds[parsed_args.subparser_name], parsed_args)

    # compose result
    composer.compose()

if __name__ == '__main__':
    main()

