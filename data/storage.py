from pathlib import Path
from typing import List
import pandas as pd
from .schema import Player, Game, InjuryStatus, Market

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "storage"
DATA_DIR.mkdir(exist_ok=True)

def _to_df(models, model_cls):
    return pd.DataFrame([m.model_dump() for m in models], columns=model_cls.model_fields.keys())

def save_players(players: List[Player]):
    df = _to_df(players, Player)
    df.to_parquet(DATA_DIR / "players.parquet", index=False)

def save_games(games: List[Game]):
    df = _to_df(games, Game)
    df.to_parquet(DATA_DIR / "games.parquet", index=False)

def save_injuries(injuries: List[InjuryStatus]):
    df = _to_df(injuries, InjuryStatus)
    df.to_parquet(DATA_DIR / "injuries.parquet", index=False)

def save_markets(markets: List[Market]):
    df = _to_df(markets, Market)
    df.to_parquet(DATA_DIR / "markets.parquet", index=False)

def load_players():
    return pd.read_parquet(DATA_DIR / "players.parquet")

def load_games():
    return pd.read_parquet(DATA_DIR / "games.parquet")

def load_injuries():
    return pd.read_parquet(DATA_DIR / "injuries.parquet")

def load_markets():
    return pd.read_parquet(DATA_DIR / "markets.parquet")
