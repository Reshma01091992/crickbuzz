import sqlite3

DB_PATH = "cricket.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create teams table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name  TEXT NOT NULL UNIQUE,
            country    TEXT,
            team_type  TEXT
        )
    """)
    #Create Venue table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venues (
            venue_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            venue_name TEXT NOT NULL UNIQUE,
            city       TEXT,
            country    TEXT,
            capacity   INTEGER
        )
    """)
    # Create players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            country     TEXT,
            playing_role        TEXT,
            batting_style       TEXT,
            bowling_style       TEXT,
            date_of_birth        TEXT,
            api_player_id        TEXT UNIQUE
            
        )
    """)
    # Create series table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS series (
            series_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name TEXT NOT NULL,
            host_country    TEXT,
            match_type       TEXT,
            start_date       TEXT,
            end_date         TEXT, 
            total_matches     INTEGER
        )
    """)
    # Create matches table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            match_desc TEXT,
            match_format   TEXT,
            team1_id    INTEGER,
            team2_id    INTEGER,
            venue_id    INTEGER,
            series_id   INTEGER,
            match_date   TEXT,
            victory_margin   TEXT,
            status      TEXT,
            winning_team_id INTEGER,
            victory_type TEXT,
            toss_winner_id INTEGER,
            toss_decision TEXT,
            api_match_id TEXT UNIQUE,
            FOREIGN KEY (series_id) REFERENCES series(series_id),
            FOREIGN KEY (team1_id) REFERENCES teams(team_id),
            FOREIGN KEY (team2_id) REFERENCES teams(team_id),
            FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
            FOREIGN KEY (winning_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id)
        )
    """)
    # Create player_stats table--#sql lite uses REAL for floating point numbers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_stats (
        stat_id         INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id       INTEGER,
        match_format    TEXT,
        matches_played  INTEGER DEFAULT 0,
        runs_scored     INTEGER DEFAULT 0,
        batting_avg     REAL DEFAULT 0.0,  
        strike_rate     REAL DEFAULT 0.0,
        centuries       INTEGER DEFAULT 0,
        half_centuries  INTEGER DEFAULT 0,
        highest_score   INTEGER DEFAULT 0,
        wickets_taken   INTEGER DEFAULT 0,
        bowling_avg     REAL DEFAULT 0.0,
        economy_rate    REAL DEFAULT 0.0,
        catches         INTEGER DEFAULT 0,
        stumpings       INTEGER DEFAULT 0,
        FOREIGN KEY (player_id) REFERENCES players(player_id)
    )
""")
    # Create table batting performances
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS batting_performances (
        perf_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id         INTEGER,
        player_id        INTEGER,
        innings_number   INTEGER,
        runs_scored      INTEGER DEFAULT 0,
        balls_faced      INTEGER DEFAULT 0,
        strike_rate      REAL DEFAULT 0.0,
        fours            INTEGER DEFAULT 0,
        sixes            INTEGER DEFAULT 0,
        batting_position INTEGER,
        dismissal_type   TEXT,
        FOREIGN KEY (match_id)  REFERENCES matches(match_id),
        FOREIGN KEY (player_id) REFERENCES players(player_id)
    )
""")
    # Create table bowling performances
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bowling_performances (
        perf_id         INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id        INTEGER,
        player_id       INTEGER,
        innings_number  INTEGER,
        overs_bowled    REAL DEFAULT 0.0,
        runs_conceded   INTEGER DEFAULT 0,
        wickets_taken   INTEGER DEFAULT 0,
        economy_rate    REAL DEFAULT 0.0,
        maidens         INTEGER DEFAULT 0,
        FOREIGN KEY (match_id)  REFERENCES matches(match_id),
        FOREIGN KEY (player_id) REFERENCES players(player_id)
    )
""")
    conn.commit()
    conn.close()
    print("✅ Database initialized!")
    
def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def execute_update(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id
if __name__ == "__main__":
    try:
        init_db()
        print("Database setup complete!")
    except Exception as e:
        print(f"Error initializing database: {e}")
#run this file to see cricket.db created in the project folder with all the tables.