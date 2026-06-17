import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.sidebar.title("🏏 Cricbuzz LiveStats")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "📺 Live Matches", "🏆 Player Stats",
     "📊 SQL Analytics", "⚙️ CRUD Operations"]
)

st.sidebar.markdown("---")
st.sidebar.info("Powered by Cricbuzz API")

if page == "🏠 Home":
    from pages.home import show
    show()
elif page == "📺 Live Matches":
    from pages.live_matches import show
    show()
elif page == "🏆 Player Stats":
    from pages.player_stats import show
    show()
elif page == "📊 SQL Analytics":
    from pages.sql_analytics import show
    show()
elif page == "⚙️ CRUD Operations":
    from pages.crud_operations import show
    show()