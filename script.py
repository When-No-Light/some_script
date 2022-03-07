import argparse
from app.parser import Parser
from app.nbe import NbeApi


nbe_api = NbeApi()
parser = Parser.get_args()
args = parser.parse_args()


def get_function(args: argparse.Namespace) -> None:
    if args.command == "grouped-teams":
        args = parser.parse_args()
        nbe_api.grouped_teams()

    elif args.command == "players-stats":
        args = parser.parse_args()
        nbe_api.players_stats(args.name)

    elif args.command == "teams-stats":
        args = parser.parse_args()
        nbe_api.teams_stats(args.season, args.output)


if __name__ == "__main__":
    get_function(args)

    # python script.py players-stats --name Michael
