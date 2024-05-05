#!/usr/bin/env python3

import argparse
import sys
from io import StringIO

from core import Loader, composer


class HopParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print_help(self):
        msg_io = StringIO()
        super().print_help(msg_io)
        composer.add('info', msg_io.getvalue())
        composer.compose()


def main():
    # Setup up parser
    parser = HopParser()
    subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

    # Initialize commands
    loader = Loader(subparsers=subparsers)
    commands = loader.commands

    # print help if hop has no arguments
    if len(sys.argv) == 1:
        parser.print_help()

    # Parse args and run command
    parsed_args = parser.parse_known_args()
    command = commands[parsed_args[0].subparser_name]
    command.additional_args = parsed_args[1]
    command.process_command(parsed_args[0])

    # compose result
    composer.compose()

if __name__ == '__main__':
    main()
