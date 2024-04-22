#!/usr/bin/env python3

from composer import composer
from helpers.loaders import initialize_hop
import argparse
from io import StringIO


class HopParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.composer = composer

    def print_help(self):
        msg_io = StringIO()
        super().print_help(msg_io)
        composer.add('message', msg_io.getvalue())
        composer.compose()


def run_command(command, parsed_args, additional_args):
    command.additional_args = additional_args
    command.process_command(parsed_args)


def main():
    # Setup up parser
    #  parser = argparse.ArgumentParser()
    parser = HopParser()
    subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

    # Initialize commands
    commands = initialize_hop(composer=composer, subparsers=subparsers)

    # Parse args and run command
    parsed_args = parser.parse_known_args()
    run_command(commands[parsed_args[0].subparser_name], parsed_args[0], parsed_args[1])

    # compose result
    composer.compose()

if __name__ == '__main__':
    main()
