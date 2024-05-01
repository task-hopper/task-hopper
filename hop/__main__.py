#!/usr/bin/env python3

import argparse
import sys
from io import StringIO

from composer import Composer
from loader import Loader


class HopParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print_help(self):
        msg_io = StringIO()
        super().print_help(msg_io)
        composer = Composer()
        composer.add('info', msg_io.getvalue())
        composer.compose()


def run_command(command, parsed_args, additional_args):
    command.additional_args = additional_args
    command.process_command(parsed_args)


def main():
    # Setup up parser
    parser = HopParser()
    subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

    # Initialize commands
    loader = Loader(subparsers=subparsers)
    commands = loader.commands
    #  commands = initialize_task_hopper(composer=composer, subparsers=subparsers)

    # print help if hop has no arguments
    if len(sys.argv) == 1:
        parser.print_help()

    # Parse args and run command
    parsed_args = parser.parse_known_args()
    breakpoint()
    run_command(commands[parsed_args[0].subparser_name], parsed_args[0], parsed_args[1])

    # compose result
    loader.composer.compose()

if __name__ == '__main__':
    main()
