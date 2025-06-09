# 🚓 Traffic Stops Dashboard

A Streamlit-powered dashboard for analyzing traffic stop data collected at police check posts.  
It connects to a PostgreSQL database, fetches real-time logs, and provides crime insights and arrest prediction.

---

## 📌 What This Project Does

- 🔍 Search traffic stop logs by vehicle number
- 📋 View incident summaries (age, gender, violation, search, arrest, etc.)
- 📊 Visualize traffic stop patterns (violations, stop durations, drug-related incidents)
- 🧠 Predict likely arrest outcomes for new vehicle stop entries
- 🛡️ Centralized log monitoring for check post analysis

---

## 🖼️ Example Features

### Vehicle Log Search
Search by vehicle number and instantly view matching incident logs.

### Incident Report
Summarizes the key details from a selected traffic stop:
- Driver age & gender
- Violation committed
- Whether a search or arrest happened
- Drug involvement and stop duration

### Key Insights (Plotly Charts)
- 🚦 Top Violations
- 🚔 Arrest Rate Distribution
- 🌍 Drug-related stops by country
- ⏱️ Traffic stop duration analysis

### New Log & Arrest Prediction
Enter new stop info and get a **basic prediction**:
> _Will the driver likely be arrested?_

---

## 🛠️ Technologies Used

| Tool         | Purpose                                |
|--------------|----------------------------------------|
| Streamlit    | Web dashboard frontend                 |
| PostgreSQL   | Backend database                       |
| SQLAlchemy   | Database connection                    |
| Plotly       | Interactive charts                     |
| Pandas       | Data manipulation                      |
| Python       | Core logic and processing              |

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [PostgreSQL](https://www.postgresql.org/)

---

