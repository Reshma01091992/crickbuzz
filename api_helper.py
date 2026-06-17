import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_HOST = "cricbuzz-cricket.p.rapidapi.com"
API_KEY  = "c0b1a4e556mshe95aa6a1451e5bfp19354fjsn414e6ef191ea"
BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

def api_get(endpoint):
    try:
       url = BASE_URL + "/" + endpoint
       response = requests.get(url, headers=HEADERS, verify=False)
       return response.json()
    except requests.RequestException as e:
        print(f"Error fetching API data from {endpoint}: {e}")
        return {"error": str(e)}
# ── MATCHES ──────────────────────────────────────────
def get_live_matches():
    return api_get("matches/v1/live")

def get_recent_matches():
    return api_get("matches/v1/recent")

def get_upcoming_matches():
    return api_get("matches/v1/upcoming")

def get_scorecard(match_id):
    return api_get(f"mcenter/v1/{match_id}/hscard")

# ── PLAYERS ──────────────────────────────────────────
def get_batting_stats(format="odi"):
    return api_get(f"stats/v1/rankings/batsmen?formatType={format}")

def get_bowling_stats(format="odi"):
    return api_get(f"stats/v1/rankings/bowlers?formatType={format}")

def search_player(name):
    return api_get(f"stats/v1/player/search?plrN={name}")

# ── SERIES ───────────────────────────────────────────
def get_series(category="international"):
    return api_get(f"series/v1/{category}")

if __name__ == "__main__":
    print("Testing API...")
    data = get_live_matches()
    print(data)
