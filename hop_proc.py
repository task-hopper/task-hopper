from composer import composer
from helpers.command_tools import check_command, command_hooks, load_commands
import argparse
import sys

@command_hooks
def run_command(command, parsed_args):
    command.process_command(parsed_args)

def main():
    # print directive before showing help message
    if sys.argv[-1] in ['-h', '--help']: print('__hop_message__')
    if not check_command(sys.argv[1]):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

        cmds = load_commands()
        for alias, cls in cmds.items():
            cls.setup_command(subparsers)

        parsed_args = parser.parse_args(sys.argv[1:])
        run_command(cmds[parsed_args.subparser_name], parsed_args)
    composer.compose()

if __name__ == '__main__':
    main()

# carrot implementation
#  carrot_bunch = CarrotBunch('carrots')
#  carrot_bunch.apply_all_carrots_on_value(5)
