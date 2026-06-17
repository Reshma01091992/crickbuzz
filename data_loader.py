# 1. Imports at top
from utils.api_helper import get_recent_matches, get_batting_stats, get_bowling_stats
from utils.db_connection import get_connection, execute_update
import urllib3
urllib3.disable_warnings()

# 2. save_team() function
def save_team(team_name, country=""):
    conn = get_connection()
    cursor = conn.cursor()
    
    # First CHECK if team exists
    cursor.execute(
        "SELECT team_id FROM teams WHERE team_name = ?", 
        (team_name,)
    )
    row = cursor.fetchone()
    
    if row:
        # Team EXISTS → just return its ID
        conn.close()
        return row["team_id"]
    else:
        # Team DOESN'T EXIST → insert it
        cursor.execute(
            "INSERT INTO teams (team_name, country) VALUES (?, ?)",
            (team_name, country)
        )
        conn.commit()
        team_id = cursor.lastrowid
        conn.close()
        return team_id

# 3. save_venue() function
def save_venue(venue_name, city="", country="", capacity=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    # First CHECK if venue exists
    cursor.execute(
        "SELECT venue_id FROM venues WHERE venue_name = ?", 
        (venue_name,)
    )
    row = cursor.fetchone()
    
    if row:
        # Venue EXISTS → just return its ID
        conn.close()
        return row["venue_id"]
    else:
        # Venue DOESN'T EXIST → insert it
        cursor.execute(
            "INSERT INTO venues (venue_name, city, country, capacity) VALUES (?, ?, ?, ?)",
            (venue_name, city, country, capacity)
        )
        conn.commit()
        venue_id = cursor.lastrowid
        conn.close()
        return venue_id
    
# 4. load_matches() function
def load_matches():
    print("Loading matches...")
    data = get_recent_matches()  # which api function?
    if not data:
        print("❌ No match data received.")
        return

    count = 0
    for type_match in data.get("typeMatches", []):
        for series in type_match.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper", {})
            if not wrapper:
                continue
            for match in wrapper.get("matches", []):
                mi = match.get("matchInfo", {})
                if not mi:
                    continue

                # Get team names from matchInfo
                team1_name = mi.get("team1", {}).get("teamName", "Unknown")
                team2_name = mi.get("team2", {}).get("teamName", "Unknown")
                
                # Save teams and get their IDs
                team1_id = save_team(team1_name) # save team1
                team2_id = save_team(team2_name) # save team2

                # Get venue info
                venue_info = mi.get("venueInfo", {})
                venue_name = venue_info.get("ground", "Unknown")
                city       = venue_info.get("city", "")
                country    = venue_info.get("country", "")
                
                # Save venue and get its ID
                venue_id = save_venue(venue_name, city, country) # save venue

                # Get match details
                api_match_id = str(mi.get("matchId", ""))
                match_desc   = mi.get("matchDesc", "")
                match_format = mi.get("matchFormat", "")
                match_date   = mi.get("startDate", "")
                status       = mi.get("status", "")

                # Skip if match already exists
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT match_id FROM matches WHERE api_match_id = ?",
                    (api_match_id,)
                )
                if cursor.fetchone():
                    conn.close()
                    continue
                conn.close()

                # Insert match into database
                execute_update("""
                    INSERT INTO matches
                        (match_desc, match_format, team1_id, team2_id,
                         venue_id, match_date, status, api_match_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (match_desc, match_format, team1_id, team2_id,
                      venue_id, match_date, status, api_match_id))
                count += 1

    print(f"✅ {count} matches loaded into database!")
# 5. load_players() function
def load_players():
    print("Loading players...")
    count = 0
    
    for fmt in ["test", "odi", "t20"]:
        # ── BATTING ───────────────────────────
        bat_data = get_batting_stats(fmt)
        if bat_data:
            rankings = bat_data.get("rank", [])
            for player in rankings:
                api_id  = str(player.get("id", ""))
                name    = player.get("name", "Unknown")
                country = player.get("country", "")
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT player_id FROM players WHERE api_player_id = ?",
                    (api_id,)
                )
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO players (full_name, country, api_player_id)
                        VALUES (?, ?, ?)
                    """, (name, country, api_id))
                    conn.commit()
                    count += 1
                conn.close()

        # ── BOWLING ───────────────────────────
        bowl_data = get_bowling_stats(fmt)
        if bowl_data:
            rankings = bowl_data.get("rank", [])
            for player in rankings:
                api_id  = str(player.get("id", ""))
                name    = player.get("name", "Unknown")
                country = player.get("country", "")
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT player_id FROM players WHERE api_player_id = ?",
                    (api_id,)
                )
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO players (full_name, country, api_player_id)
                        VALUES (?, ?, ?)
                    """, (name, country, api_id))
                    conn.commit()
                    count += 1
                conn.close()

    print(f"✅ {count} players loaded!")  # ← AFTER the loop!
# 6. Test block
if __name__ == "__main__":
    try:
        load_matches()
        load_players()
        print("Data loading complete!") 
    except Exception as e:
        print(f"Error loading data: {e}")   