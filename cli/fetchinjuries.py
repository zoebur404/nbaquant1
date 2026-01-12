from nba_api.stats.endpoints import injuryreport
from datetime import datetime

def fetch_injuries():
    try:
        df = injuryreport.InjuryReport().get_data_frames()[0]
    except Exception:
        print("Error fetching injury report")
        return

    df["timestamp"] = datetime.utcnow()
    print(df)

if __name__ == "__main__":
    fetch_injuries()
