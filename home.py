import streamlit as st

def show():
    st.title("🏏 Welcome to Cricbuzz LiveStats!")
    st.markdown("""
        This application provides real-time cricket statistics and insights using the Cricbuzz API. 
        Navigate through the sidebar to explore live matches, player stats, SQL analytics, and CRUD operations.
        
        **Features:**
        - 📺 Live Matches: View ongoing cricket matches with live scores and details.
        - 🏆 Player Stats: Access detailed statistics for your favorite players.
        - 📊 SQL Analytics: Analyze match data with custom SQL queries.
        - ⚙️ CRUD Operations: Manage player and match data with Create, Read, Update, Delete functionalities.
        
        Powered by the Cricbuzz API, this app is your go-to source for all things cricket! 🏏
    """)
    st.subheader("Getting Started")
    st.markdown("""
        Use the sidebar to navigate through different sections of the app. 
        Each section provides unique insights and functionalities related to cricket statistics.
        
        **Note:** Data is fetched in real-time from the Cricbuzz API, so you can stay updated with the latest cricket action!
    """)
    
    st.markdown("---")
    st.subheader("🛠️ Tech Stack")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🐍 Python 3.14")
    with col2:
        st.info("🎨 Streamlit")
    with col3:
        st.info("🗄️ SQLite")
    with col4:
        st.info("🌐 Cricbuzz API")