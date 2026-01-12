from datetime import date
import pandas as pd
from nba_quant.data.storage import load_players, load_games, load_injuries, load_markets

def get_tonights_board(target_date: date) -> pd.DataFrame:
    players = load_players()
    games = load_games()
    injuries = load_injuries()
    markets = load_markets()

    games_today = games[games["date"] == target_date]

    df = markets.merge(
        games_today[["game_id", "home_team_id", "away_team_id", "date"]],
        on="game_id",
        how="inner",
    ).merge(
        players[["player_id", "name", "team_id", "position"]],
        on="player_id",
        how="left",
    )

    injuries_sorted = injuries.sort_values("timestamp").drop_duplicates(
        subset=["player_id"], keep="last"
    )
    df = df.merge(
        injuries_sorted[["player_id", "status"]],
        on="player_id",
        how="left",
    ).rename(columns={"status": "injury_status"})

    return df

if __name__ == "__main__":
    board = get_tonights_board(date.today())
    print(board.head())
    print(f"{len(board)} markets on today’s board")
