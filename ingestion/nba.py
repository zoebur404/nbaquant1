from nba_api.stats.static import players as nba_players
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import injuryreport
from datetime import datetime, date
from typing import List
import pandas as pd
from nba_quant.data.schema import Player, Game, InjuryStatus

def fetch_players() -> List[Player]:
    raw = nba_players.get_players()
    return [
        Player(
            player_id=str(p["id"]),
            name=p["full_name"],
            team_id="",
            position=None,
        )
        for p in raw
    ]

def fetch_games_for_date(target_date: date) -> List[Game]:
    logs = leaguegamelog.LeagueGameLog(season="2024-25").get_data_frames()[0]
    logs["GAME_DATE"] = pd.to_datetime(logs["GAME_DATE"]).dt.date
    logs_today = logs[logs["GAME_DATE"] == target_date]

    games = []
    for _, row in logs_today.iterrows():
        games.append(
            Game(
                game_id=row["GAME_ID"],
                date=row["GAME_DATE"],
                home_team_id=row["HOME_TEAM_ID"],
                away_team_id=row["VISITOR_TEAM_ID"],
                start_time=datetime.utcnow(),
            )
        )
    return games

def fetch_injuries() -> List[InjuryStatus]:
    try:
        df = injuryreport.InjuryReport().get_data_frames()[0]
    except Exception:
        return []

    injuries = []
    for _, row in df.iterrows():
        injuries.append(
            InjuryStatus(
                player_id=str(row["PERSON_ID"]),
                team_id=str(row["TEAM_ID"]),
                status=row["INJURY_STATUS"].lower(),
                reason=row.get("INJURY_DESC", None),
                timestamp=datetime.utcnow(),
            )
        )
    return injuries
