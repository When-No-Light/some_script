import pandas as pd
import requests
from sqlalchemy import create_engine

engine = create_engine("sqlite:///output.sqlite", echo=False)


class NbeApi:
    URL = "https://www.balldontlie.io/api/v1/"

    def get_data(self, url: str) -> pd.DataFrame:
        page_number = 0
        page_size = 100
        list = []
        try:
            while page_size > 99:
                url = url + f"per_page=100&page={page_number}"
                response = requests.get(url)

                if not response.json()["data"] and page_number == 0:
                    return pd.DataFrame()
                elif not response.json()["data"]:
                    pd.DataFrame.from_dict(dict)
                else:
                    page_size = len(response.json()["data"])
                    list += response.json()["data"]

                page_number += 1

            return pd.DataFrame.from_dict(list)
        except Exception as e:
            print(
                f"Error {e} occurred while trying to connect to the \
                    NBA API by url {url}"
            )

    def grouped_teams(self) -> None:
        url_teams = self.URL + "teams?"
        df = self.get_data(url_teams)
        try:
            for i in df["division"].unique():
                print(i)
                f = df.loc[df["division"] == i]
                for index, row in f.iterrows():
                    print("\t", row["full_name"], f'({row["abbreviation"]})')
        except Exception as e:
            print(
                f"An error {e} occurred while trying to process the data \
                    received from the API"
            )

    def players_stats(self, name: str) -> None:

        url_players = self.URL + "players?search=" + name + "&"
        df = self.get_data(url_players)

        if not df.empty:
            # df = df.loc[(df['first_name'] == name) | (df['last_name'] == name)]
            height_feet_column = df["height_feet"]
            height_feet_column.dropna()
            if height_feet_column.any():
                max_height_player = df.loc[height_feet_column.idxmax()]

                height_text = "{first_name} {last_name} {height_m} meters".format(
                    first_name=max_height_player.first_name,
                    last_name=max_height_player.last_name,
                    height_m=round(max_height_player.height_feet * 0.3048, 2),
                )
            else:
                height_text = "Not found"

            weight_pounds_column = df["weight_pounds"]

            weight_pounds_column.dropna()
            if weight_pounds_column.any():
                max_weight_player = df.loc[weight_pounds_column.idxmax()]

                weight_text = "{first_name} {last_name} {weight} kilograms".format(
                    first_name=max_weight_player.first_name,
                    last_name=max_weight_player.last_name,
                    weight=int(max_weight_player.weight_pounds * 0.453592),
                )
            else:
                weight_text = "Not found"

        else:
            height_text = weight_text = "Not found"
        print("The tallest player: ", height_text)
        print("The heaviest player: ", weight_text)

    def teams_stats(self, season: int, output: str) -> None:

        url_all_games = self.URL + f"games?seasons[]={season}&"

        df_all_games = self.get_data(url_all_games)

        columns = [
            "Team name",
            "Won games as home team",
            "Won games as visitor team",
            "Lost games as home team",
            "Lost games as visitor team",
        ]

        teams_stats = pd.DataFrame(columns=columns)

        url_teams = self.URL + "teams?"
        all_teams = self.get_data(url_teams)

        try:
            df_all_games.reset_index()
            all_teams.reset_index()
            for index, team in all_teams.iterrows():
                won_games_as_home_team = 0
                won_games_as_visitor_team = 0
                lost_games_as_home_team = 0
                lost_games_as_visitor_team = 0

                for index, row in df_all_games.iterrows():
                    if row["home_team"]["id"] == team.id:
                        if row["home_team_score"] > row["visitor_team_score"]:
                            won_games_as_home_team += 1
                        else:
                            lost_games_as_home_team += 1
                    elif row["visitor_team"]["id"] == team.id:
                        if row["home_team_score"] > row["visitor_team_score"]:
                            lost_games_as_visitor_team += 1
                        else:
                            won_games_as_visitor_team += 1

                new_dict = {
                    "Team name": f"{team['full_name']} ({team['abbreviation']})",
                    "Won games as home team": won_games_as_home_team,
                    "Won games as visitor team": won_games_as_visitor_team,
                    "Lost games as home team": lost_games_as_home_team,
                    "Lost games as visitor team": lost_games_as_visitor_team,
                }

                df_dictionary = pd.DataFrame([new_dict])
                teams_stats = pd.concat([teams_stats, df_dictionary], ignore_index=True)

            if output == "stdout":
                for index, row in teams_stats.iterrows():
                    print(row["Team name"])
                    for col in teams_stats.columns[1:]:
                        print(f"\t{col.lower()}: {row[col]}")
                return
            elif output == "csv":
                teams_stats.to_csv("/output.csv", index=False)
                return
            teams_stats = teams_stats.rename(
                columns={
                    "Team name": "team_name",
                    "Won games as home team": "won_games_as_home_team",
                    "Won games as visitor team": "won_games_as_visitor_team",
                    "Lost games as home team": "lost_games_as_home_team",
                    "Lost games as visitor team": "lost_games_as_visitor_team",
                }
            )
            if output == "sqlite":
                teams_stats.to_sql("teams_stats", con=engine, index=False)
            elif output == "json":
                teams_stats.to_json("output.json", orient="records")
            else:
                raise ValueError(
                    "Invalid data was received for -o/--otput \
                    parameter"
                )
        except Exception as e:
            print(
                f"An error {e} occurred while trying to process the data received \
                    from the API"
            )
