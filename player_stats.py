import streamlit as st
import pandas as pd
from utils.api_helper import (
    search_player, get_player_info,
    get_player_batting_career, get_player_bowling_career
)


def parse_career_table(data):
    """Convert headers + values into a clean DataFrame."""
    if not data or "headers" not in data:
        return None
    headers = data.get("headers", [])
    rows = []
    for item in data.get("values", []):
        rows.append(item.get("values", []))
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=headers)
    df = df.rename(columns={"ROWHEADER": "Stat"})
    return df


def show_player_profile(info):
    """Display the Profile tab content."""
    col1, col2 = st.columns([1, 3])
    with col1:
        image_url = info.get("image", "")
        if image_url:
            st.image(image_url, width=150)
    with col2:
        st.subheader(info.get("name", "Unknown"))
        full_name = info.get("fullName", "")
        if full_name:
            st.caption(full_name)

    st.markdown("---")
    st.subheader("🎯 Personal Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🏏 Cricket Details**")
        st.write(f"**Role:** {info.get('role', 'N/A')}")
        st.write(f"**Batting:** {info.get('bat', 'N/A')}")
        st.write(f"**Bowling:** {info.get('bowl', 'N/A') or 'N/A'}")
        st.write(f"**International Team:** {info.get('intlTeam', 'N/A')}")

    with col2:
        st.markdown("**📍 Personal Details**")
        st.write(f"**Date of Birth:** {info.get('DoB', 'N/A')}")
        st.write(f"**Birth Place:** {info.get('birthPlace', 'N/A')}")

    with col3:
        st.markdown("**🏆 Teams Played For**")
        teams = info.get("teams", "")
        if teams:
            for team in teams.split(","):
                st.write(f"- {team.strip()}")

    st.markdown("---")
    web_url = info.get("appIndex", {}).get("webURL", "")
    if web_url:
        st.markdown(f"🔗 **Full Profile:** [{web_url}]({web_url})")


def show_career_stats(data, title):
    """Display Batting or Bowling stats tab."""
    st.subheader(title)
    df = parse_career_table(data)
    if df is None or df.empty:
        st.info(f"No {title.lower()} data available for this player.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)


def display_selected_player(player_id, found_name):
    """Fetch and display full profile/batting/bowling for one player."""
    st.markdown("---")

    with st.spinner("Fetching player details..."):
        info    = get_player_info(player_id)
        batting = get_player_batting_career(player_id)
        bowling = get_player_bowling_career(player_id)

    st.subheader(f"📊 {found_name} - Player Profile")
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🏏 Batting Stats", "🎳 Bowling Stats"])

    with tab1:
        if info:
            show_player_profile(info)
        else:
            st.warning("Could not fetch profile information.")

    with tab2:
        show_career_stats(batting, "🏏 Batting Career Stats")

    with tab3:
        show_career_stats(bowling, "🎳 Bowling Career Stats")


def show():
    st.title("👤 Cricket Player Statistics")
    st.markdown("---")

    # ── SEARCH SECTION ─────────────────────────────────
    st.subheader("🔍 Search for a Player")
    col1, col2 = st.columns([4, 1])
    with col1:
        player_name = st.text_input("Enter player name:", placeholder="e.g. Dhoni, Sachin, Singh")
    with col2:
        st.write("")
        st.write("")
        search_clicked = st.button("🔍 Search")

    # Run search and store results in session_state so dropdown selection
    # doesn't trigger a fresh search on every rerun
    if search_clicked:
        if not player_name.strip():
            st.warning("⚠️ Please enter a player name!")
            st.session_state.pop("search_results", None)
        else:
            with st.spinner("Searching..."):
                result = search_player(player_name)
            players = result.get("player", []) if result else []
            if not players:
                st.error(f"❌ No player found with name '{player_name}'")
                st.session_state.pop("search_results", None)
            else:
                st.session_state["search_results"] = players

    # ── SHOW DROPDOWN IF WE HAVE RESULTS ───────────────
    if "search_results" in st.session_state:
        players = st.session_state["search_results"]

        st.success(f"✅ Found {len(players)} matching player(s)")

        # Build readable labels: "Name - Team"
        options = [
            f"{p.get('name', 'Unknown')} - {p.get('teamName', 'N/A')}"
            for p in players
        ]

        selected_option = st.selectbox(
            "Select the correct player:",
            options
        )

        # Find the matching player dict for the selected label
        selected_index = options.index(selected_option)
        selected_player = players[selected_index]

        player_id = selected_player.get("id")
        found_name = selected_player.get("name")

        display_selected_player(player_id, found_name)