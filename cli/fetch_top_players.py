import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

CATEGORIES = {
    "points": "PTS",
    "rebounds": "REB",
    "assists": "AST",
    "threes": "FG3M",
    "steals": "STL",
    "blocks": "BLK"
}

def fetch_top_players(season="2024-25"):
    df = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season
    ).get_data_frames()[0]

    results = {}

    for name, col in CATEGORIES.items():
        top10 = df.sort_values(col, ascending=False).head(10)
        results[name] = top10[["PLAYER_ID", "PLAYER_NAME", col]]

    return results

if __name__ == "__main__":
    data = fetch_top_players()
    for cat, df in data.items():
        print(f"\nTop 10 {cat.upper()}:")
        print(df)
