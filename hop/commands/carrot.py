from hop import Command
from helpers.carrot_utils import read_registry


class CarrotCommand(Command):
    def __init__(self):
        self.alias = 'carrot'
        self.help = 'perform carrot action'

    def setup_command(self):
        carrot_subparsers = self.parser.add_subparsers(dest="subcommand")

        #############
        # available #
        #############
        available_parser = carrot_subparsers.add_parser(
            "available", help="list available carrots"
        )

        available_parser.add_argument("carrot_name", nargs="?", help="name of carrot")

        ###########
        # install #
        ###########
        install_parser = carrot_subparsers.add_parser(
            "install", help="install a carrot plugin"
        )

        install_parser.add_argument("carrot_name", help="name of the carrot")
        install_parser.add_argument("-v", "--version", help="version tag/branch")
        install_parser.add_argument("-r", "--repo", help="repo clone string or local path")

        ########
        # show #
        ########
        show_parser = carrot_subparsers.add_parser(
            "show", help="show carrot version"
        )

        show_parser.add_argument("carrot_name", help="name of the carrot")

        ##########
        # remove #
        ##########
        remove_parser = carrot_subparsers.add_parser(
            "remove", help="uninstall a carrot"
        )

        remove_parser.add_argument("carrot_name", help="name of the carrot")

        #######

        # Require carrot name argument for the parsers
        #  for subcmd in [install_parser, show_parser, remove_parser]:
            #  subcmd.required = True


    def process_command(self, parsed_args):
        if parsed_args.subcommand == 'available':
            registry_data = read_registry()
            carrots = "\n".join(list(registry_data.keys()))
            output = f"\nAvailable Carrots\n-----------------\n\n{carrots}"
            self.composer.add('info', output)
        elif parsed_args.subcommand == 'install':
            self.push_task(
                'InstallCarrot',
                carrot_name=parsed_args.carrot_name,
                version=parsed_args.version,
                repo=parsed_args.repo
            )
        else:
            self.composer.add('info', f"{parsed_args.subcommand} not ready yet")
