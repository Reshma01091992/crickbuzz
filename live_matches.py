import streamlit as st
from utils.api_helper import get_live_matches, get_recent_matches, get_upcoming_matches


def extract_matches(data):
    """Extract flat list of matches from nested API response."""
    matches = []
    for type_match in data.get("typeMatches", []):
        for series in type_match.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper", {})
            if wrapper:
                for match in wrapper.get("matches", []):
                    matches.append(match)
    return matches


def get_match_label(mi):
    """Create a display label for match dropdown."""
    team1  = mi.get("team1", {}).get("teamName", "TBA")
    team2  = mi.get("team2", {}).get("teamName", "TBA")
    fmt    = mi.get("matchFormat", "")
    desc   = mi.get("matchDesc", "")
    return f"{team1} vs {team2} | {desc} | {fmt}"


def display_scorecard(mi, ms):
    """Display detailed match scorecard."""
    team1   = mi.get("team1", {}).get("teamName", "TBA")
    team2   = mi.get("team2", {}).get("teamName", "TBA")
    status  = mi.get("status", "")
    venue   = mi.get("venueInfo", {}).get("ground", "Unknown")
    city    = mi.get("venueInfo", {}).get("city", "")
    fmt     = mi.get("matchFormat", "")
    desc    = mi.get("matchDesc", "")

    # ── Match Header ──────────────────────────────────────
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        border-radius: 12px;
        padding: 20px;
        color: white;
        margin-bottom: 16px;
    ">
        <h2 style="margin:0;">🏏 {team1} vs {team2}</h2>
        <p style="margin:8px 0 0 0; opacity:0.85;">
            📍 {venue}, {city} &nbsp;|&nbsp; {desc} &nbsp;|&nbsp; {fmt}
        </p>
        <p style="margin:8px 0 0 0; color:#2ecc71; font-weight:bold;">
            {status}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Scorecard ─────────────────────────────────────────
    if ms:
        st.subheader("📊 Scorecard")
        col1, col2 = st.columns(2)

        # Team 1 Score
        with col1:
            team1_score = ms.get("team1Score", {})
            if team1_score:
                st.markdown(f"### 🏏 {team1}")
                # Innings 1
                inn1 = team1_score.get("inngs1", {})
                if inn1:
                    runs  = inn1.get("runs", "-")
                    wkts  = inn1.get("wickets", "-")
                    overs = inn1.get("overs", "-")
                    st.metric(
                        label="Innings 1",
                        value=f"{runs}/{wkts}",
                        delta=f"{overs} overs"
                    )
                # Innings 2
                inn2 = team1_score.get("inngs2", {})
                if inn2:
                    runs  = inn2.get("runs", "-")
                    wkts  = inn2.get("wickets", "-")
                    overs = inn2.get("overs", "-")
                    st.metric(
                        label="Innings 2",
                        value=f"{runs}/{wkts}",
                        delta=f"{overs} overs"
                    )
            else:
                st.info(f"{team1} yet to bat")

        # Team 2 Score
        with col2:
            team2_score = ms.get("team2Score", {})
            if team2_score:
                st.markdown(f"### 🏏 {team2}")
                # Innings 1
                inn1 = team2_score.get("inngs1", {})
                if inn1:
                    runs  = inn1.get("runs", "-")
                    wkts  = inn1.get("wickets", "-")
                    overs = inn1.get("overs", "-")
                    st.metric(
                        label="Innings 1",
                        value=f"{runs}/{wkts}",
                        delta=f"{overs} overs"
                    )
                # Innings 2
                inn2 = team2_score.get("inngs2", {})
                if inn2:
                    runs  = inn2.get("runs", "-")
                    wkts  = inn2.get("wickets", "-")
                    overs = inn2.get("overs", "-")
                    st.metric(
                        label="Innings 2",
                        value=f"{runs}/{wkts}",
                        delta=f"{overs} overs"
                    )
            else:
                st.info(f"{team2} yet to bat")
    else:
        st.info("⏳ Score not available yet.")


def show_matches_tab(fetch_fn, tab_title, limit=20):
    """Generic function to show matches in a tab."""
    st.subheader(tab_title)
    with st.spinner("Fetching matches..."):
        data = fetch_fn()

    if not data:
        st.warning("Could not fetch matches.")
        return

    matches = extract_matches(data)
    if not matches:
        st.info("No matches found.")
        return

    matches = matches[:limit]

    # ── Dropdown ──────────────────────────────────────────
    match_labels = [
        get_match_label(m.get("matchInfo", {}))
        for m in matches
    ]

    selected_label = st.selectbox(
        "Select a Match:",
        match_labels,
        key=f"select_{tab_title}"
    )

    # ── Show selected match scorecard ─────────────────────
    selected_index = match_labels.index(selected_label)
    selected_match = matches[selected_index]
    mi = selected_match.get("matchInfo", {})
    ms = selected_match.get("matchScore", {})

    st.markdown("---")
    display_scorecard(mi, ms)

    # ── All matches summary ────────────────────────────────
    st.markdown("---")
    with st.expander("📋 View All Matches"):
        for match in matches:
            mi_  = match.get("matchInfo", {})
            ms_  = match.get("matchScore", {})
            team1 = mi_.get("team1", {}).get("teamName", "TBA")
            team2 = mi_.get("team2", {}).get("teamName", "TBA")
            status = mi_.get("status", "")
            venue  = mi_.get("venueInfo", {}).get("ground", "")

            # Score summary
            t1s = ms_.get("team1Score", {}).get("inngs1", {})
            t2s = ms_.get("team2Score", {}).get("inngs1", {})
            t1_score = f"{t1s.get('runs','-')}/{t1s.get('wickets','-')} ({t1s.get('overs','-')} ov)" if t1s else "Yet to bat"
            t2_score = f"{t2s.get('runs','-')}/{t2s.get('wickets','-')} ({t2s.get('overs','-')} ov)" if t2s else "Yet to bat"

            st.markdown(f"""
            **🏏 {team1} vs {team2}**  
            📍 {venue} | {t1_score} vs {t2_score}  
            🟢 {status}
            """)
            st.markdown("---")


def show():
    st.title("📺 Live & Recent Matches")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🔴 Live", "✅ Recent", "📅 Upcoming"])

    with tab1:
        show_matches_tab(get_live_matches, "🔴 Live Matches")

    with tab2:
        show_matches_tab(get_recent_matches, "✅ Recent Matches")

    with tab3:
        show_matches_tab(get_upcoming_matches, "📅 Upcoming Matches")