import streamlit as st
import pandas as pd
from utils.db_connection import execute_query

# ─── ALL 25 QUERIES ───────────────────────────────────────
QUERIES = {
    "1. Players from India": """
        SELECT full_name, playing_role, batting_style, bowling_style
        FROM players
        WHERE country = 'India'
    """,
    "2. Recent Matches": """
        SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2,
               v.venue_name, v.city, m.match_date, m.status
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        ORDER BY m.match_date DESC
        LIMIT 20
    """,
    "3. Top 10 Run Scorers in ODI": """
        SELECT p.full_name, ps.runs_scored, ps.batting_avg, ps.centuries
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.match_format = 'ODI'
        ORDER BY ps.runs_scored DESC
        LIMIT 10
    """,
    "4. Venues with Capacity over 25000": """
        SELECT venue_name, city, country, capacity
        FROM venues
        WHERE capacity > 25000
        ORDER BY capacity DESC
        LIMIT 10
    """,
    "5. Team Win Count": """
        SELECT t.team_name, COUNT(*) AS total_wins
        FROM matches m
        JOIN teams t ON m.winning_team_id = t.team_id
        GROUP BY t.team_name
        ORDER BY total_wins DESC
    """,
    "6. Players by Role": """
        SELECT playing_role, COUNT(*) AS player_count
        FROM players
        WHERE playing_role IS NOT NULL
        GROUP BY playing_role
        ORDER BY player_count DESC
    """,
    "7. Highest Score by Format": """
        SELECT match_format, MAX(highest_score) AS highest_score
        FROM player_stats
        WHERE match_format IN ('TEST', 'ODI', 'T20')
        GROUP BY match_format
    """,
    "8. Series Started in 2024": """
        SELECT series_name, host_country, match_type,
               start_date, total_matches
        FROM series
        WHERE start_date LIKE '2024%'
        ORDER BY start_date
    """,
    "9. All-rounders 1000 runs and 50 wickets": """
        SELECT p.full_name, ps.runs_scored, ps.wickets_taken, ps.match_format
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.runs_scored > 1000 AND ps.wickets_taken > 50
        ORDER BY ps.runs_scored DESC
    """,
    "10. Last 20 Completed Matches": """
        SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2,
               tw.team_name AS winner, m.victory_margin,
               m.victory_type, v.venue_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams tw ON m.winning_team_id = tw.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        WHERE m.status = 'completed'
        ORDER BY m.match_date DESC
        LIMIT 20
    """,
    "11. Player Performance Across Formats": """
        SELECT p.full_name,
               SUM(CASE WHEN ps.match_format='TEST' THEN ps.runs_scored ELSE 0 END) AS test_runs,
               SUM(CASE WHEN ps.match_format='ODI'  THEN ps.runs_scored ELSE 0 END) AS odi_runs,
               SUM(CASE WHEN ps.match_format='T20'  THEN ps.runs_scored ELSE 0 END) AS t20_runs,
               ROUND(AVG(ps.batting_avg), 2) AS overall_avg
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.player_id
        HAVING COUNT(DISTINCT ps.match_format) >= 2
        ORDER BY overall_avg DESC
    """,
    "12. Home vs Away Performance": """
        SELECT t.team_name,
               SUM(CASE WHEN v.country = t.country THEN 1 ELSE 0 END) AS home_wins,
               SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) AS away_wins
        FROM matches m
        JOIN teams t ON m.winning_team_id = t.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        GROUP BY t.team_name
        ORDER BY home_wins DESC
    """,
    "13. Century Partnerships": """
        SELECT p1.full_name AS batsman1, p2.full_name AS batsman2,
               bp1.runs_scored + bp2.runs_scored AS partnership_runs,
               bp1.innings_number
        FROM batting_performances bp1
        JOIN batting_performances bp2
          ON bp1.match_id = bp2.match_id
         AND bp1.innings_number = bp2.innings_number
         AND bp2.batting_position = bp1.batting_position + 1
        JOIN players p1 ON bp1.player_id = p1.player_id
        JOIN players p2 ON bp2.player_id = p2.player_id
        WHERE bp1.runs_scored + bp2.runs_scored >= 100
        ORDER BY partnership_runs DESC
        LIMIT 20
    """,
    "14. Bowling at Venues 3 plus matches": """
        SELECT p.full_name, v.venue_name,
               COUNT(DISTINCT bp.match_id) AS matches_played,
               ROUND(AVG(bp.economy_rate), 2) AS avg_economy,
               SUM(bp.wickets_taken) AS total_wickets
        FROM bowling_performances bp
        JOIN players p ON bp.player_id = p.player_id
        JOIN matches m ON bp.match_id = m.match_id
        JOIN venues v ON m.venue_id = v.venue_id
        WHERE bp.overs_bowled >= 4
        GROUP BY p.player_id, v.venue_id
        HAVING matches_played >= 3
        ORDER BY total_wickets DESC
    """,
    "15. Performance in Close Matches": """
        SELECT p.full_name,
               COUNT(DISTINCT bp.match_id) AS close_matches,
               ROUND(AVG(bp.runs_scored), 2) AS avg_runs
        FROM batting_performances bp
        JOIN players p ON bp.player_id = p.player_id
        JOIN matches m ON bp.match_id = m.match_id
        WHERE (m.victory_type = 'runs' AND CAST(m.victory_margin AS INTEGER) < 50)
           OR (m.victory_type = 'wickets' AND CAST(m.victory_margin AS INTEGER) < 5)
        GROUP BY p.player_id
        ORDER BY avg_runs DESC
        LIMIT 20
    """,
    "16. Yearly Batting Trends 2020 plus": """
        SELECT p.full_name,
               SUBSTR(m.match_date, 1, 4) AS year,
               ROUND(AVG(bp.runs_scored), 2) AS avg_runs,
               ROUND(AVG(bp.strike_rate), 2) AS avg_strike_rate,
               COUNT(DISTINCT bp.match_id) AS matches_played
        FROM batting_performances bp
        JOIN players p ON bp.player_id = p.player_id
        JOIN matches m ON bp.match_id = m.match_id
        WHERE SUBSTR(m.match_date, 1, 4) >= '2020'
        GROUP BY p.player_id, year
        HAVING matches_played >= 5
        ORDER BY year DESC, avg_runs DESC
    """,
    "17. Toss Advantage Analysis": """
        SELECT m.toss_decision,
               COUNT(*) AS total_matches,
               SUM(CASE WHEN m.toss_winner_id = m.winning_team_id THEN 1 ELSE 0 END) AS toss_winner_wins,
               ROUND(
                   100.0 * SUM(CASE WHEN m.toss_winner_id = m.winning_team_id THEN 1 ELSE 0 END)
                   / COUNT(*), 2
               ) AS win_percentage
        FROM matches m
        WHERE m.toss_decision IS NOT NULL AND m.winning_team_id IS NOT NULL
        GROUP BY m.toss_decision
    """,
    "18. Most Economical Bowlers": """
        SELECT p.full_name,
               COUNT(DISTINCT bp.match_id) AS matches,
               ROUND(AVG(bp.economy_rate), 2) AS avg_economy,
               SUM(bp.wickets_taken) AS total_wickets
        FROM bowling_performances bp
        JOIN players p ON bp.player_id = p.player_id
        JOIN matches m ON bp.match_id = m.match_id
        WHERE m.match_format IN ('ODI', 'T20')
        GROUP BY p.player_id
        HAVING matches >= 10 AND AVG(bp.overs_bowled) >= 2
        ORDER BY avg_economy ASC
        LIMIT 20
    """,
    "19. Most Consistent Batsmen": """
        SELECT p.full_name,
               COUNT(bp.perf_id) AS innings,
               ROUND(AVG(bp.runs_scored), 2) AS avg_runs,
               ROUND(
                   SQRT(AVG(bp.runs_scored * bp.runs_scored)
                   - AVG(bp.runs_scored) * AVG(bp.runs_scored)), 2
               ) AS std_deviation
        FROM batting_performances bp
        JOIN players p ON bp.player_id = p.player_id
        JOIN matches m ON bp.match_id = m.match_id
        WHERE bp.balls_faced >= 10 AND SUBSTR(m.match_date, 1, 4) >= '2022'
        GROUP BY p.player_id
        HAVING innings >= 10
        ORDER BY std_deviation ASC
        LIMIT 20
    """,
    "20. Format-wise Match Count and Average": """
        SELECT p.full_name,
               SUM(CASE WHEN m.match_format='TEST' THEN 1 ELSE 0 END) AS test_matches,
               SUM(CASE WHEN m.match_format='ODI'  THEN 1 ELSE 0 END) AS odi_matches,
               SUM(CASE WHEN m.match_format='T20'  THEN 1 ELSE 0 END) AS t20_matches,
               ROUND(AVG(bp.runs_scored), 2) AS overall_avg
        FROM batting_performances bp
        JOIN players p ON bp.player_id = p.player_id
        JOIN matches m ON bp.match_id = m.match_id
        GROUP BY p.player_id
        HAVING COUNT(DISTINCT bp.match_id) >= 20
        ORDER BY overall_avg DESC
    """,
    "21. Player Performance Ranking": """
        SELECT p.full_name, ps.match_format,
               ROUND(
                   (ps.runs_scored * 0.01)
                 + (ps.batting_avg * 0.5)
                 + (ps.strike_rate * 0.3)
                 + (ps.wickets_taken * 2)
                 + ((50 - COALESCE(ps.bowling_avg, 50)) * 0.5)
                 + ((6  - COALESCE(ps.economy_rate, 6)) * 2), 2
               ) AS performance_score
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        ORDER BY performance_score DESC
        LIMIT 30
    """,
    "22. Head to Head Analysis": """
        SELECT t1.team_name AS team1, t2.team_name AS team2,
               COUNT(*) AS total_matches,
               SUM(CASE WHEN m.winning_team_id = m.team1_id THEN 1 ELSE 0 END) AS team1_wins,
               SUM(CASE WHEN m.winning_team_id = m.team2_id THEN 1 ELSE 0 END) AS team2_wins
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        WHERE m.match_date >= DATE('now', '-3 years')
        GROUP BY t1.team_id, t2.team_id
        HAVING total_matches >= 5
        ORDER BY total_matches DESC
    """,
    "23. Player Form Analysis": """
        WITH recent AS (
            SELECT bp.player_id, bp.runs_scored, bp.strike_rate,
                   ROW_NUMBER() OVER (
                       PARTITION BY bp.player_id ORDER BY m.match_date DESC
                   ) AS rn
            FROM batting_performances bp
            JOIN matches m ON bp.match_id = m.match_id
        )
        SELECT p.full_name,
               ROUND(AVG(CASE WHEN rn <= 5  THEN runs_scored END), 2) AS last_5_avg,
               ROUND(AVG(CASE WHEN rn <= 10 THEN runs_scored END), 2) AS last_10_avg,
               ROUND(AVG(CASE WHEN rn <= 10 THEN strike_rate END), 2) AS recent_sr,
               SUM(CASE WHEN rn <= 10 AND runs_scored >= 50 THEN 1 ELSE 0 END) AS fifties_in_10,
               CASE
                   WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 50 THEN 'Excellent Form'
                   WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 30 THEN 'Good Form'
                   WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 15 THEN 'Average Form'
                   ELSE 'Poor Form'
               END AS form_category
        FROM recent
        JOIN players p ON recent.player_id = p.player_id
        GROUP BY recent.player_id
        HAVING last_10_avg IS NOT NULL
        ORDER BY last_5_avg DESC
        LIMIT 30
    """,
    "24. Best Batting Partnerships": """
        SELECT p1.full_name AS batsman1, p2.full_name AS batsman2,
               COUNT(*) AS partnerships,
               ROUND(AVG(bp1.runs_scored + bp2.runs_scored), 2) AS avg_partnership,
               MAX(bp1.runs_scored + bp2.runs_scored) AS best_partnership,
               SUM(CASE WHEN bp1.runs_scored + bp2.runs_scored > 50 THEN 1 ELSE 0 END) AS fifty_plus
        FROM batting_performances bp1
        JOIN batting_performances bp2
          ON bp1.match_id = bp2.match_id
         AND bp1.innings_number = bp2.innings_number
         AND bp2.batting_position = bp1.batting_position + 1
        JOIN players p1 ON bp1.player_id = p1.player_id
        JOIN players p2 ON bp2.player_id = p2.player_id
        GROUP BY bp1.player_id, bp2.player_id
        HAVING partnerships >= 5
        ORDER BY avg_partnership DESC
        LIMIT 20
    """,
    "25. Career Trajectory Analysis": """
        WITH quarterly AS (
            SELECT bp.player_id,
                   SUBSTR(m.match_date, 1, 4) || '-Q'
                   || ((CAST(SUBSTR(m.match_date, 6, 2) AS INTEGER) - 1) / 3 + 1) AS quarter,
                   AVG(bp.runs_scored) AS avg_runs,
                   AVG(bp.strike_rate) AS avg_sr,
                   COUNT(*) AS innings
            FROM batting_performances bp
            JOIN matches m ON bp.match_id = m.match_id
            GROUP BY bp.player_id, quarter
            HAVING innings >= 3
        )
        SELECT p.full_name,
               COUNT(DISTINCT q.quarter) AS quarters_played,
               ROUND(AVG(q.avg_runs), 2) AS career_avg
        FROM quarterly q
        JOIN players p ON q.player_id = p.player_id
        GROUP BY q.player_id
        HAVING quarters_played >= 6
        ORDER BY career_avg DESC
    """
}


def show():
    st.title("📊 SQL Analytics — 25 Queries")
    st.markdown("---")

    # ─── QUERY SELECTOR ───────────────────────────────────
    selected = st.selectbox(
        "Select a Query to Run:",
        list(QUERIES.keys())
    )

    # ─── SHOW SQL ─────────────────────────────────────────
    with st.expander("👁 View SQL Query"):
        st.code(QUERIES[selected], language="sql")

    # ─── RUN QUERY ────────────────────────────────────────
    if st.button("▶ Run Query"):
        try:
            results = execute_query(QUERIES[selected])
            if results:
                df = pd.DataFrame([dict(r) for r in results])
                st.success(f"✅ {len(df)} rows returned!")
                st.dataframe(df, use_container_width=True, hide_index=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    f"{selected}.csv",
                    "text/csv"
                )
            else:
                st.info("ℹ️ Query returned no results. Database may need more data.")
        except Exception as e:
            st.error(f"❌ SQL Error: {e}")

    st.markdown("---")

    # ─── CUSTOM QUERY ─────────────────────────────────────
    st.subheader("🔧 Write Your Own SQL Query")
    custom_sql = st.text_area(
        "Enter SQL Query:",
        height=150,
        placeholder="SELECT * FROM players LIMIT 10"
    )
    if st.button("▶ Run Custom Query"):
        if custom_sql.strip():
            try:
                results = execute_query(custom_sql)
                if results:
                    df = pd.DataFrame([dict(r) for r in results])
                    st.success(f"✅ {len(df)} rows returned!")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("Query returned no results.")
            except Exception as e:
                st.error(f"❌ SQL Error: {e}")
        else:
            st.warning("⚠️ Please enter a query first!")