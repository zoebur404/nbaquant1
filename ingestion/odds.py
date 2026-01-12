import requests
from datetime import datetime
from typing import List
import uuid
from nba_quant.data.schema import Market
from nba_quant.config import ODDS_API_KEY, BOOKS

BASE_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba"

MARKET_MAP = {
    "player_points": "points",
    "player_rebounds": "rebounds",
    "player_assists": "assists",
    "player_threes": "threes",
    "player_points_rebounds_assists": "pra",
}

def fetch_markets_for_today() -> List[Market]:
    events = requests.get(
        f"{BASE_URL}/events",
        params={"apiKey": ODDS_API_KEY, "regions": "us"},
        timeout=10,
    ).json()

    markets = []

    for event in events:
        event_id = event["id"]

        odds_resp = requests.get(
            f"{BASE_URL}/events/{event_id}/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": "us",
                "markets": ",".join(MARKET_MAP.keys()),
            },
            timeout=10,
        )

        if odds_resp.status_code != 200:
            continue

        odds_data = odds_resp.json()

        for book in odds_data.get("bookmakers", []):
            if book["key"] not in BOOKS:
                continue

            for market in book.get("markets", []):
                stat_type = MARKET_MAP.get(market["key"])
                if not stat_type:
                    continue

                for outcome in market.get("outcomes", []):
                    if outcome.get("point") is None:
                        continue

                    markets.append(
                        Market(
                            market_id=str(uuid.uuid4()),
                            book=book["key"],
                            timestamp=datetime.utcnow(),
                            game_id=event_id,
                            player_id=outcome["description"],
                            stat_type=stat_type,
                            line=float(outcome["point"]),
                            over_odds=float(outcome.get("price", 0)),
                            under_odds=float(outcome.get("price", 0)),
                        )
                    )

    return markets
