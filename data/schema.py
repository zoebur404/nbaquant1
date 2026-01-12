from pydantic import BaseModel
from typing import Optional, Literal, Dict
from datetime import datetime, date

class Player(BaseModel):
    player_id: str
    name: str
    team_id: str
    position: Optional[str] = None

class Game(BaseModel):
    game_id: str
    date: date
    home_team_id: str
    away_team_id: str
    start_time: datetime

class InjuryStatus(BaseModel):
    player_id: str
    team_id: str
    status: Literal["out", "doubtful", "questionable", "probable", "active"]
    reason: Optional[str] = None
    timestamp: datetime

class Market(BaseModel):
    market_id: str
    book: str
    timestamp: datetime
    game_id: str
    player_id: str
    stat_type: str
    line: float
    over_odds: float
    under_odds: float

class PlayerState(BaseModel):
    player: Player
    game: Game
    opponent_team_id: str
    injury_status: InjuryStatus
    minutes_proj: Optional[float] = None
    usage_proj: Optional[float] = None
    rebound_chances: Optional[float] = None
    potential_assists: Optional[float] = None
    pace_projection: Optional[float] = None
    dvp_modifiers: Dict[str, float] = {}
