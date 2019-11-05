from composer import composer
from helpers.command_tools import get_config_command, load_commands
import argparse
import sys

#  @command_hooks
def run_hop_command(command, parsed_args):
    command.process_command(parsed_args)

#  @command_hooks
def run_configured_command(command):
    composer.add('task', command)

def main():
    # print directive before showing help message
    if sys.argv[-1] in ['-h', '--help']: print('__hop_message__')

    config_command = get_config_command(sys.argv[1])
    if config_command:
        run_configured_command(command=config_command)
    else:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='subparser_name', metavar='')

        cmds = load_commands()
        for alias, cls in cmds.items():
            cls.setup_command(subparsers)

        parsed_args = parser.parse_args(sys.argv[1:])
        run_hop_command(cmds[parsed_args.subparser_name], parsed_args)
    composer.compose()

if __name__ == '__main__':
    main()

# carrot implementation
#  carrot_bunch = CarrotBunch('carrots')
#  carrot_bunch.apply_all_carrots_on_value(5)
