from datetime import date
from nba_quant.ingestion.nba import fetch_players, fetch_games_for_date, fetch_injuries
from nba_quant.ingestion.odds import fetch_markets_for_today
from nba_quant.data.storage import save_players, save_games, save_injuries, save_markets

if __name__ == "__main__":
    today = date.today()

    print("Fetching players…")
    players = fetch_players()

    print("Fetching games…")
    games = fetch_games_for_date(today)

    print("Fetching injuries…")
    injuries = fetch_injuries()

    print("Fetching markets…")
    markets = fetch_markets_for_today()

    print("Saving data…")
    save_players(players)
    save_games(games)
    save_injuries(injuries)
    save_markets(markets)

    print("Ingestion complete.")
