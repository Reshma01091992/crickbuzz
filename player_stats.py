import streamlit as st
import pandas as pd
from utils.api_helper import get_batting_stats, get_bowling_stats

def show():
    st.title("🏆 Player Statistics")
    st.markdown("---")

    # ── Format Selector ───────────────────────────────────
    fmt = st.selectbox("Select Format:", ["test", "odi", "t20"])

    # ── Two Tabs ──────────────────────────────────────────
    tab1, tab2 = st.tabs(["🏏 Top Batsmen", "🎳 Top Bowlers"])

    # ── Batting Stats ─────────────────────────────────────
    with tab1:
        st.subheader(f"🏏 Top Batsmen — {fmt.upper()}")
        with st.spinner("Fetching batting rankings..."):
            data = get_batting_stats(fmt)

        if not data:
            st.warning("Could not fetch batting stats.")
        else:
            rankings = data.get("rank", [])
            if not rankings:
                st.info("No batting rankings available.")
            else:
                # Build rows for dataframe
                rows = []
                for i, p in enumerate(rankings[:20], 1):
                    rows.append({
                        "Rank"    : i,
                        "Player"  : p.get("name", "Unknown"),
                        "Country" : p.get("country", ""),
                        "Rating"  : p.get("rating", "-"),
                    })
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # ── Bar Chart ─────────────────────────────
                st.subheader(f"📊 Top 5 Batsmen by Rating")
                top5 = df.head(5)
                st.bar_chart(
                    top5.set_index("Player")["Rating"].astype(float)
                )

    # ── Bowling Stats ─────────────────────────────────────
    with tab2:
        st.subheader(f"🎳 Top Bowlers — {fmt.upper()}")
        with st.spinner("Fetching bowling rankings..."):
            data = get_bowling_stats(fmt)

        if not data:
            st.warning("Could not fetch bowling stats.")
        else:
            rankings = data.get("rank", [])
            if not rankings:
                st.info("No bowling rankings available.")
            else:
                rows = []
                for i, p in enumerate(rankings[:20], 1):
                    rows.append({
                        "Rank"    : i,
                        "Player"  : p.get("name", "Unknown"),
                        "Country" : p.get("country", ""),
                        "Rating"  : p.get("rating", "-"),
                    })
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # ── Bar Chart ─────────────────────────────
                st.subheader(f"📊 Top 5 Bowlers by Rating")
                top5 = df.head(5)
                st.bar_chart(
                    top5.set_index("Player")["Rating"].astype(float)
                )