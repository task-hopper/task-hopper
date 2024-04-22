#!/usr/bin/env python3

from composer import composer
from helpers.loaders import initialize_hop
import argparse
import sys

def run_command(command, parsed_args, additional_args):
    command.additional_args = additional_args
    command.process_command(parsed_args)

def main():
    # Setup up parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

    # Initialize commands
    commands = initialize_hop(composer=composer, subparsers=subparsers)

    # Handle -h or --help 
    if len(sys.argv) == 1 or sys.argv[-1] in ['-h', '--help']:
        print('__hop_message__')
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse args and run command
    parsed_args = parser.parse_known_args()
    run_command(commands[parsed_args[0].subparser_name], parsed_args[0], parsed_args[1])

    # compose result
    composer.compose()

if __name__ == '__main__':
    main()
