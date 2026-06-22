# 🏏 Cricbuzz LiveStats — Real-Time Cricket Analytics Dashboard

A full-stack cricket analytics web application built with Python and Streamlit, integrating live data from the Cricbuzz API with a SQLite database for SQL-based analytics.

---

## 📌 Project Overview

**Cricbuzz LiveStats** is a comprehensive cricket analytics dashboard that delivers:
- ⚡ Real-time match updates via Cricbuzz API
- 👤 Detailed player statistics and profiles
- 🔍 SQL-driven analytics with 25 queries (Beginner to Advanced)
- 🛠️ Full CRUD operations for data management

---

## 💼 Business Use Cases

| Industry | Use Case |
|---|---|
| 📺 Sports Media | Real-time match updates for commentary teams |
| 🎮 Fantasy Cricket | Player form analysis and recent performance tracking |
| 📈 Cricket Analytics | Advanced statistical modeling and player evaluation |
| 🎓 Education | Teaching SQL and API integration with real-world data |

---

## 🏗️ Project Structure

```
cricbuzz_Project/
│
├── app.py                    ← Streamlit entry point & navigation
├── requirements.txt          ← All dependencies
├── README.md                 ← Project documentation
├── cricket.db                ← SQLite database (auto-created)
│
├── utils/
│   ├── api_helper.py         ← Cricbuzz API integration
│   ├── db_connection.py      ← SQLite connection & query functions
│   ├── data_loader.py        ← Bridge: API data → Database
│   └── sample_data.py        ← Demo data generator for SQL analytics
│
└── pages/
    ├── home.py               ← Home page with project overview
    ├── live_matches.py       ← Live/Recent/Upcoming matches with scorecard
    ├── player_stats.py       ← Player search, profile & career stats
    ├── sql_analytics.py      ← 25 SQL queries (Beginner → Advanced)
    └── crud_operations.py    ← Create, Read, Update, Delete operations
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Core programming language |
| Streamlit | Interactive web dashboard |
| SQLite | Lightweight embedded database |
| Pandas | Data transformation & display |
| Requests | HTTP API calls |
| Cricbuzz API (RapidAPI) | Live cricket data source |

---

## ⚙️ Setup Instructions

### Step 1 — Clone the repository
```bash
git clone https://github.com/Reshma01091992/crickbuzz.git
cd crickbuzz
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Configure API Key
Open `utils/api_helper.py` and replace the API key:
```python
API_KEY = "your_rapidapi_key_here"
```
Get your free API key from: https://rapidapi.com/cricketapilive/api/cricbuzz-cricket

### Step 4 — Initialize the database
```bash
python -m utils.db_connection
```

### Step 5 — Load real data from API
```bash
python -m utils.data_loader
```

### Step 6 — Load sample data for SQL Analytics
```bash
python -m utils.sample_data
```
> ⚠️ **Note:** `sample_data.py` generates realistic but synthetic data for tables like `player_stats`, `batting_performances`, and `bowling_performances`. This is required because detailed match-level performance data is not available on the free Cricbuzz API tier. All other data (matches, teams, venues, players, live scores, player profiles) is fetched in real-time from the Cricbuzz API.

### Step 7 — Run the application
```bash
streamlit run app.py
```

Open your browser at: **http://localhost:8501**

---

## 📊 Database Schema

| Table | Description | Data Source |
|---|---|---|
| `teams` | Cricket teams | Real API data |
| `venues` | Match venues | Real API data |
| `players` | Player details | Real API data |
| `series` | Tournament/series | Sample data |
| `matches` | Match records | Real API data |
| `player_stats` | Career statistics per format | Sample data |
| `batting_performances` | Per-match batting records | Sample data |
| `bowling_performances` | Per-match bowling records | Sample data |

---

## 📱 Pages & Features

### 🏠 Home
- Project overview and description
- Feature highlights and tech stack
- Navigation instructions

### 📺 Live Matches
- **3 tabs:** Live, Recent, Upcoming matches
- **Match dropdown:** Select any match to view details
- **Scorecard:** Team scores with Innings 1 & 2 (runs/wickets/overs)
- Data fetched in real-time from Cricbuzz API

### 👤 Player Stats
- **Player search:** Type any player name (e.g. "Dhoni", "Kohli")
- **Smart dropdown:** Multiple matches shown when name is common
- **3 tabs per player:**
  - Profile (photo, role, batting/bowling style, DOB, teams)
  - Batting Career Stats (Test/ODI/T20/IPL)
  - Bowling Career Stats (Test/ODI/T20/IPL)

### 📊 SQL Analytics
- **25 queries** across 3 difficulty levels:
  - 🟢 Beginner (Q1-Q8): SELECT, WHERE, GROUP BY, ORDER BY
  - 🟡 Intermediate (Q9-Q16): JOINs, subqueries, aggregations
  - 🔴 Advanced (Q17-Q25): Window functions, CTEs, complex analytics
- **View SQL:** Expandable SQL code viewer
- **Download CSV:** Export any query result
- **Custom Query:** Write and run your own SQL

### ⚙️ CRUD Operations
- **Add Player:** Form with validation
- **View Players:** Full table with CSV export
- **Update Player:** COALESCE/NULLIF for partial updates
- **Delete Player:** Two-step confirmation to prevent accidents

---

## 🧮 SQL Query Highlights

| Level | Query | Concept Used |
|---|---|---|
| Beginner | Q1 - Players from India | WHERE filter |
| Beginner | Q5 - Team Win Count | GROUP BY + COUNT |
| Intermediate | Q2 - Recent Matches | 3-table JOIN |
| Intermediate | Q12 - Home vs Away | Conditional aggregation |
| Advanced | Q21 - Performance Ranking | Weighted scoring formula |
| Advanced | Q23 - Player Form Analysis | CTE + Window functions |
| Advanced | Q25 - Career Trajectory | Quarterly time-series analysis |

---

## 🔌 API Endpoints Used

| Endpoint | Function | Page |
|---|---|---|
| `matches/v1/live` | Live matches | Live Matches |
| `matches/v1/recent` | Recent matches | Live Matches |
| `matches/v1/upcoming` | Upcoming matches | Live Matches |
| `stats/v1/rankings/batsmen` | Batting rankings | Player Stats |
| `stats/v1/rankings/bowlers` | Bowling rankings | Player Stats |
| `stats/v1/player/search` | Player search | Player Stats |
| `stats/v1/player/{id}` | Player profile | Player Stats |
| `stats/v1/player/{id}/batting` | Batting career stats | Player Stats |
| `stats/v1/player/{id}/bowling` | Bowling career stats | Player Stats |

---

## 🎯 Key Design Decisions

1. **Modular architecture** — Each file has one responsibility (Single Responsibility Principle)
2. **Centralized API module** — `api_helper.py` handles all API calls; change key in one place
3. **Parameterized queries** — All SQL uses `?` placeholders to prevent SQL injection
4. **Upsert pattern** — `save_team()` and `save_venue()` prevent duplicate records
5. **Two-step delete** — Confirmation before permanent deletion
6. **Session state** — Streamlit `session_state` preserves search results across reruns
7. **SSL handling** — `verify=False` + `urllib3.disable_warnings()` for corporate networks

---

## 🚀 Future Improvements

- Add Plotly charts for visual analytics
- Extend CRUD to matches and venues tables
- Move API key to environment variables (`.env`) for security
- Upgrade to paid API tier for real batting/bowling scorecard data
- Add user authentication for CRUD operations
- Implement database indexing for faster query performance
- Add auto-refresh for live match scores every 30 seconds

---

## 👩‍💻 Author

**Reshma G**
Solutions Architect & RPA Tech Lead — Kyndryl
GUVI Data Science Capstone Project — 2026

---

## 📄 License

This project is for educational purposes as part of the GUVI Data Science program.