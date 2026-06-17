from utils.db_connection import execute_update, execute_query

def insert_sample_data():
    print("Inserting sample data...")

    # ─── UPDATE VENUES WITH CAPACITY ──────────────────────
    print("Updating venues...")
    venues = execute_query("SELECT venue_id, venue_name FROM venues LIMIT 20")
    capacities = [95000, 68000, 66000, 50000, 45000, 40000, 35000, 
                  30000, 28000, 25000, 22000, 20000, 18000, 15000,
                  12000, 10000, 8000, 6000, 5000, 4000]
    for i, venue in enumerate(venues):
        execute_update(
            "UPDATE venues SET capacity = ?, country = 'India' WHERE venue_id = ?",
            (capacities[i % len(capacities)], venue["venue_id"])
        )
    print("✅ Venues updated!")

    # ─── INSERT SERIES ────────────────────────────────────
    print("Inserting series...")
    series_data = [
        ("India tour of England 2024", "England", "ODI", "2024-01-15", "2024-01-30", 5),
        ("Australia tour of India 2024", "India", "TEST", "2024-02-10", "2024-03-15", 4),
        ("ICC T20 World Cup 2024", "West Indies", "T20", "2024-06-01", "2024-06-29", 55),
        ("Asia Cup 2024", "Sri Lanka", "ODI", "2024-08-01", "2024-08-17", 13),
        ("India tour of Australia 2024", "Australia", "TEST", "2024-11-22", "2025-01-07", 5),
        ("England tour of India 2024", "India", "TEST", "2024-01-25", "2024-03-05", 5),
        ("South Africa tour of India 2024", "India", "T20", "2024-09-25", "2024-10-05", 4),
        ("New Zealand tour of India 2024", "India", "TEST", "2024-10-16", "2024-11-05", 3),
    ]
    for s in series_data:
        try:
            execute_update("""
                INSERT INTO series (series_name, host_country, match_type, 
                                   start_date, end_date, total_matches)
                VALUES (?, ?, ?, ?, ?, ?)
            """, s)
        except:
            pass
    print("✅ Series inserted!")

    # ─── INSERT PLAYER STATS ──────────────────────────────
    print("Inserting player stats...")
    player_stats = [
        # (player_id, format, matches, runs, avg, sr, 100s, 50s, hs, wkts, bowl_avg, econ, catches, stumpings)
        (4,  "TEST", 80,  7500, 55.1, 58.2, 26, 35, 239, 5,  88.0, 2.8, 45, 0),
        (4,  "ODI",  140, 4500, 38.5, 82.3, 9,  30, 164, 8,  65.0, 5.2, 55, 0),
        (5,  "TEST", 90,  7200, 52.3, 54.1, 24, 32, 251, 3,  95.0, 2.5, 50, 0),
        (5,  "ODI",  160, 6500, 47.8, 80.5, 13, 40, 148, 5,  72.0, 4.8, 60, 0),
        (5,  "T20",  80,  2100, 31.2, 125.3, 2, 15, 95,  2,  55.0, 7.2, 25, 0),
        (6,  "TEST", 20,  1800, 52.8, 62.3, 5,  10, 182, 15, 32.5, 3.1, 12, 0),
        (6,  "ODI",  45,  1500, 40.2, 88.5, 3,  8,  115, 25, 28.3, 4.5, 18, 0),
        (7,  "TEST", 50,  3500, 42.1, 55.3, 10, 18, 180, 2,  85.0, 2.9, 30, 0),
        (7,  "ODI",  120, 4200, 38.8, 84.2, 8,  28, 143, 3,  75.0, 5.1, 45, 0),
        (7,  "T20",  60,  1500, 28.3, 128.5, 1, 10, 86,  1,  62.0, 7.8, 20, 0),
        (8,  "TEST", 15,  1500, 57.2, 68.5, 4,  7,  214, 0,  0.0,  0.0, 8,  0),
        (8,  "ODI",  25,  900,  42.3, 92.5, 2,  5,  124, 0,  0.0,  0.0, 10, 0),
        (8,  "T20",  35,  1100, 38.5, 152.3, 2, 8,  98,  0,  0.0,  0.0, 12, 0),
        (9,  "TEST", 18,  1600, 51.2, 58.3, 4,  8,  240, 8,  42.5, 3.2, 10, 0),
        (9,  "ODI",  40,  1400, 38.8, 85.2, 3,  7,  108, 12, 35.2, 4.8, 15, 0),
        (9,  "T20",  50,  1300, 32.5, 135.2, 1, 8,  88,  8,  28.5, 7.5, 18, 0),
        (10, "TEST", 20,  1800, 52.5, 65.3, 5,  8,  192, 0,  0.0,  0.0, 12, 0),
        (10, "ODI",  50,  2200, 52.8, 98.5, 6,  12, 145, 0,  0.0,  0.0, 20, 0),
        (10, "T20",  65,  2100, 45.2, 158.3, 4, 14, 126, 0,  0.0,  0.0, 22, 0),
    ]
    for ps in player_stats:
        try:
            execute_update("""
                INSERT INTO player_stats 
                    (player_id, match_format, matches_played, runs_scored,
                     batting_avg, strike_rate, centuries, half_centuries,
                     highest_score, wickets_taken, bowling_avg, economy_rate,
                     catches, stumpings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ps)
        except Exception as e:
            print(f"Skipping player stat: {e}")
    print("✅ Player stats inserted!")

    # ─── INSERT BATTING PERFORMANCES ──────────────────────
    print("Inserting batting performances...")
    import random
    random.seed(42)

    match_ids  = [3, 4, 5, 6, 7, 8, 9, 10]
    player_ids = [4, 5, 6, 7, 8, 9, 10]

    for match_id in match_ids:
        for innings in [1, 2]:
            for pos, player_id in enumerate(player_ids, 1):
                runs      = random.randint(0, 120)
                balls     = max(runs, random.randint(10, 150))
                sr        = round((runs / balls) * 100, 2) if balls > 0 else 0
                fours     = random.randint(0, runs // 8) if runs > 0 else 0
                sixes     = random.randint(0, runs // 20) if runs > 0 else 0
                dismissal = random.choice(["bowled", "caught", "lbw", "run out", "not out"])
                try:
                    execute_update("""
                        INSERT INTO batting_performances
                            (match_id, player_id, innings_number, runs_scored,
                             balls_faced, strike_rate, fours, sixes,
                             batting_position, dismissal_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (match_id, player_id, innings, runs,
                          balls, sr, fours, sixes, pos, dismissal))
                except Exception as e:
                    pass
    print("✅ Batting performances inserted!")

    # ─── INSERT BOWLING PERFORMANCES ──────────────────────
    print("Inserting bowling performances...")
    bowler_ids = [6, 9]  # players who bowl

    for match_id in match_ids:
        for innings in [1, 2]:
            for player_id in bowler_ids:
                overs     = round(random.uniform(4, 10), 1)
                runs      = random.randint(20, 80)
                wickets   = random.randint(0, 5)
                economy   = round(runs / overs, 2) if overs > 0 else 0
                maidens   = random.randint(0, 2)
                try:
                    execute_update("""
                        INSERT INTO bowling_performances
                            (match_id, player_id, innings_number, overs_bowled,
                             runs_conceded, wickets_taken, economy_rate, maidens)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (match_id, player_id, innings, overs,
                          runs, wickets, economy, maidens))
                except Exception as e:
                    pass
    print("✅ Bowling performances inserted!")

    # ─── UPDATE MATCHES WITH WINNING TEAM & TOSS ──────────
    print("Updating matches...")
    matches = execute_query("SELECT match_id, team1_id, team2_id FROM matches LIMIT 30")
    import random
    for match in matches:
        winner    = random.choice([match["team1_id"], match["team2_id"]])
        toss      = random.choice([match["team1_id"], match["team2_id"]])
        decision  = random.choice(["bat", "bowl"])
        v_type    = random.choice(["runs", "wickets"])
        v_margin  = str(random.randint(1, 100)) if v_type == "runs" else str(random.randint(1, 10))
        execute_update("""
            UPDATE matches
            SET winning_team_id = ?,
                toss_winner_id  = ?,
                toss_decision   = ?,
                victory_type    = ?,
                victory_margin  = ?,
                status          = 'completed'
            WHERE match_id = ?
        """, (winner, toss, decision, v_type, v_margin, match["match_id"]))
    print("✅ Matches updated!")

    print("\n🎉 All sample data inserted successfully!")
    print("Now run your SQL queries — most should return results!")


if __name__ == "__main__":
    insert_sample_data()