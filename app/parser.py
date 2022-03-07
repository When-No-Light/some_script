import argparse


class Parser:
    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(
            description="Script to get information about NBA \
                players and matches"
        )

        subparsers = parser.add_subparsers(
            dest="command",
            title="subcommands",
            description="valid subcommands",
            help="additional help",
        )
        subparsers.add_parser("grouped-teams")

        s2 = subparsers.add_parser("players-stats")
        s2.add_argument(
            "-n",
            "--name",
            help="Players specific name.",
            type=valid_player_name,
            required=True,
        )

        s3 = subparsers.add_parser("teams-stats")
        s3.add_argument(
            "-s",
            "--season",
            help="Season of a specific year.",
            type=valid_season,
            required=True,
        )
        s3.add_argument(
            "-o",
            "--output",
            help="Output can be saved in csv, json or sqlite \
                format.",
            type=valid_output_param,
            default="stdout",
        )

        return parser


def valid_player_name(name: str) -> str:
    """Custom argparse type for name values given from the command line"""
    msg = "Given name ({}) not valid! Expected only letters!".format(name)
    try:
        if all(char.isalpha() for char in name):
            return name
        else:
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        raise argparse.ArgumentTypeError(msg)


def valid_season(season: str) -> str:
    msg = "Given year is not valid! Please enter the year in YYYY format, \
between 1979 and 2021!"
    try:
        if season and season.isdigit() and int(season) in range(1979, 2021):
            return season
        else:
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        raise argparse.ArgumentTypeError(msg)


def valid_output_param(output: str) -> str:
    msg = "Invalid data! -o/--output takes arguments like 'stdout', \
'csv', 'sqlite' or 'json'!"
    try:
        if output in ["stdout", "csv", "sqlite", "json"]:
            return output
        else:
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        raise argparse.ArgumentTypeError(msg)
