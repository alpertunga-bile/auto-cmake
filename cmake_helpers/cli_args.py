from argparse import ArgumentParser
from collections import namedtuple

CLIArgs = namedtuple("CLIArgs", ["verbose"])


def get_cli_args() -> CLIArgs:
    parser = ArgumentParser(
        prog="auto_cmake", description="Automation for creating the CMakeLists.txt file"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Log informations about the progress",
        default=False,
        required=False,
    )
    args = parser.parse_args()

    cli_args = CLIArgs(args.verbose)

    return cli_args
