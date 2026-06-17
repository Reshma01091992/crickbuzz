import streamlit as st
import pandas as pd
from utils.db_connection import execute_query, execute_update

def show():
    st.title("⚙️ CRUD Operations")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Add Player",
        "📋 View Players",
        "✏️ Update Player",
        "🗑️ Delete Player"
    ])

    # ─── ADD PLAYER ───────────────────────────────────────
    with tab1:
        st.subheader("➕ Add New Player")
        name          = st.text_input("Player Name")
        country       = st.text_input("Country")
        playing_role  = st.selectbox("Playing Role",
            ["Batsman", "Bowler", "All-rounder", "Wicketkeeper"])
        batting_style = st.selectbox("Batting Style",
            ["Right-hand bat", "Left-hand bat", "Unknown"])
        bowling_style = st.selectbox("Bowling Style",
            ["Right-arm fast", "Left-arm fast", "Right-arm spin", "Left-arm spin", "Unknown"])
        dob = st.date_input("Date of Birth")

        if st.button("➕ Add Player"):
            if not name or not country:
                st.error("❌ Name and Country are required!")
            else:
                try:
                    execute_update("""
                        INSERT INTO players 
                            (full_name, country, playing_role, 
                             batting_style, bowling_style, date_of_birth)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (name, country, playing_role,
                          batting_style, bowling_style, dob.isoformat()))
                    st.success(f"✅ Player '{name}' added successfully!")
                except Exception as e:
                    st.error(f"❌ Error adding player: {e}")

    # ─── VIEW PLAYERS ─────────────────────────────────────
    with tab2:
        st.subheader("📋 View All Players")
        try:
            players = execute_query("""
                SELECT player_id, full_name, country,
                       playing_role, batting_style,
                       bowling_style, date_of_birth
                FROM players
                ORDER BY full_name
            """)
            if not players:
                st.info("No players found in the database.")
            else:
                df = pd.DataFrame(players, columns=[
                    "ID", "Name", "Country",
                    "Role", "Batting", "Bowling", "DOB"
                ])
                st.success(f"✅ {len(df)} players found!")
                st.dataframe(df, use_container_width=True, hide_index=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    "players.csv",
                    "text/csv"
                )
        except Exception as e:
            st.error(f"❌ Error fetching players: {e}")

    # ─── UPDATE PLAYER ────────────────────────────────────
    with tab3:
        st.subheader("✏️ Update Player Information")
        player_id   = st.number_input("Player ID to Update", min_value=1, step=1)
        new_name    = st.text_input("New Name")
        new_country = st.text_input("New Country")

        if st.button("✏️ Update Player"):
            player = execute_query(
                "SELECT * FROM players WHERE player_id = ?",
                (int(player_id),)
            )
            if not player:
                st.error(f"❌ No player found with ID {player_id}!")
            elif not new_name and not new_country:
                st.error("❌ Provide at least one field to update!")
            else:
                try:
                    execute_update("""
                        UPDATE players
                        SET full_name = COALESCE(NULLIF(?, ''), full_name),
                            country   = COALESCE(NULLIF(?, ''), country)
                        WHERE player_id = ?
                    """, (new_name, new_country, int(player_id)))
                    st.success(f"✅ Player ID {player_id} updated successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # ─── DELETE PLAYER ────────────────────────────────────
    with tab4:
        st.subheader("🗑️ Delete Player")
        st.warning("⚠️ This action cannot be undone!")

        del_player_id = st.number_input(
            "Player ID to Delete", min_value=1, step=1)

        if st.button("🔍 Find Player"):
            player = execute_query(
                "SELECT * FROM players WHERE player_id = ?",
                (int(del_player_id),)
            )
            if not player:
                st.error(f"❌ No player found with ID {del_player_id}!")
            else:
                st.session_state["delete_player"] = dict(player[0])

        if "delete_player" in st.session_state:
            p = st.session_state["delete_player"]
            st.error(f"⚠️ You are about to delete: **{p.get('full_name')}** ({p.get('country')})")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Confirm Delete"):
                    try:
                        execute_update(
                            "DELETE FROM players WHERE player_id = ?",
                            (int(del_player_id),)
                        )
                        st.success("✅ Player deleted successfully!")
                        del st.session_state["delete_player"]
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            with col2:
                if st.button("❌ Cancel"):
                    del st.session_state["delete_player"]
                    st.info("Delete cancelled!")