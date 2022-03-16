#!/usr/bin/env python3

from composer import composer
from helpers.loaders import initialize_hop
from helpers.utils import apath
import argparse
import sys

sys.path.append(apath('~/repos/personal/task-hopper'))

def run_hop_command(command, parsed_args, additional_args):
    command.additional_args = additional_args
    command.process_command(parsed_args)

def main():
    commands = initialize_hop(composer=composer)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

    for alias, cls in sorted(commands.items()):
        cls.setup_command(subparsers)

        if len(sys.argv) > 1 and alias.startswith(sys.argv[1]):
            sys.argv[1] = alias

    if len(sys.argv) == 1 or sys.argv[-1] in ['-h', '--help']:
        # print directive before showing help message
        print('__hop_message__')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    parsed_args = parser.parse_known_args()

    run_hop_command(commands[parsed_args[0].subparser_name], parsed_args[0], parsed_args[1])

    # compose result
    composer.compose()

if __name__ == '__main__':
    main()

