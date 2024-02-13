from cmake_helpers.cli_args import get_cli_args
from cmake_helpers.creator import create

if __name__ == "__main__":
    cli_args = get_cli_args()

    create(cli_args.verbose)
