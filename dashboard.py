import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine


DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "test"
DB_USER = "postgres"
DB_PASS = "admin123"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
df = pd.read_sql("SELECT * FROM traffic_stops_cleaned;", con=engine)
st.set_page_config(page_title="Traffic Stops Dashboard", layout="wide")
st.title("🚓 Traffic Stops Dashboard")

st.write("📁 Case Logs Overview")
st.dataframe(df.head(10))

with st.expander("🔎 Search Vehicle Logs"):
    search_plate = st.text_input("Enter Vehicle Number")
if search_plate:    
    filtered = df[df['vehicle_number'].str.contains(search_plate, case=False, na=False)]
    st.dataframe(filtered)
    st.write("🔍 Match Found!" if not filtered.empty else "❌ No match found.")
else:
     filtered = pd.DataFrame()  
     st.info("Please enter a vehicle number to search.")

st.subheader("📋 Incident Report")

if not filtered.empty:
    example = filtered.iloc[0]
    stop_time = example['stop_time'].strftime('%I:%M %p')
    narrative = f"""
    🚗 A {example['driver_age']}-year-old {example['driver_gender']} driver was stopped for **{example['violation']}** at {stop_time}.
    {'A search was conducted.' if example['search_conducted'] else 'No search was conducted.'}
    {'The driver was arrested.' if example['is_arrested'] else 'The driver was not arrested.'}
    The stop lasted {example['stop_duration']} and was {'drug-related' if example['drugs_related_stop'] else 'not drug-related'}.
    """
    st.markdown(narrative)
else:
    st.markdown("No incident report to display.")

st.subheader("📊 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🚦 Top 5 Violations")
    top_violations = df['violation'].value_counts().nlargest(5).reset_index()
    top_violations.columns = ['violation', 'count']
    fig1 =px.bar(top_violations, x='violation', y='count', color='violation', title="Top Violation")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
       arrest_rate = df['is_arrested'].rename("Arrest_Status").replace({True: 'Yes', False: 'No'}).value_counts(normalize=True) * 100
       st.write("🚔 Arrest Rate:")
       st.dataframe(arrest_rate.rename("Percentage (%)"))  
 


st.subheader("🛡️ Centralized Monitoring & Crime Analysis")

col1, col2 = st.columns(2)

with col1:
     #st.write("🌍 Drug-related Stops by Country")
     drug_related = df[df['drugs_related_stop']== True]
     country_drugs = drug_related['country_name'].value_counts().reset_index()
     st.plotly_chart(
          px.pie(country_drugs, 
                 names= 'country_name', 
                 values ='count', 
                 title='🌍 Drug-related Stops by Country'), 
                 use_container_width=True)
    
     
with col2:
     duration_df = df['stop_duration'].value_counts().reset_index()
     duration_df.columns = ['Duration Range', 'Stop Count']

     st.plotly_chart(
        px.bar(duration_df, 
           x='Duration Range', 
           y='Stop Count', 
           title='⏱️ Traffic Stop Duration Analysis',
           color='Stop Count', 
           color_continuous_scale='Blues'),
           use_container_width=True
)
     

st.title("🔍 Traffic Stop Analytics Dashboard (Live SQL Queries)")

query_option = st.selectbox("Select a Query to Explore", 
    ["1. Top 10 vehicle numbers in drug-related stops",
     "2. Most frequently searched vehicles",
     "3. Gender distribution by country",
     "4. Race and gender combination with highest search rate",
     "5. Average stop duration per violation",
     "6. Common violations among drivers under 25",
     "7. Country with highest drug-related stops",
     "8. Country with most searches conducted"])

if query_option == "1. Top 10 vehicle numbers in drug-related stops":
    st.subheader("🚗 Top 10 Vehicle Numbers in Drug-Related Stops")
    query = """
        SELECT vehicle_number, COUNT(*) as count
        FROM traffic_stops_cleaned
        WHERE drugs_related_stop = TRUE
        GROUP BY vehicle_number
        ORDER BY count DESC
        LIMIT 10;
    """
    st.dataframe(pd.read_sql(query, con=engine))

elif query_option == "2. Most frequently searched vehicles":
    st.subheader("🚗 Most Frequently Searched Vehicles")
    query = """
        SELECT vehicle_number, COUNT(*) as count
        FROM traffic_stops_cleaned
        WHERE search_conducted = TRUE
        GROUP BY vehicle_number
        ORDER BY count DESC
        LIMIT 10;
    """
    st.dataframe(pd.read_sql(query, con=engine))

elif query_option == "3. Gender distribution by country":
    st.subheader("🧍 Gender Distribution by Country")
    query = """
        SELECT country_name, driver_gender, COUNT(*) as count
        FROM traffic_stops_cleaned
        GROUP BY country_name, driver_gender;
    """
    df_plot = pd.read_sql(query, con=engine)
    fig = px.bar(df_plot, x='country_name', y='count', color='driver_gender', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif query_option == "4. Race and gender combination with highest search rate":
    st.subheader("🧍 Highest Search Rate by Race and Gender")
    query = """
        SELECT driver_race, driver_gender, COUNT(*) as count
        FROM traffic_stops_cleaned
        WHERE search_conducted = TRUE
        GROUP BY driver_race, driver_gender
        ORDER BY count DESC
        LIMIT 10;
    """
    st.dataframe(pd.read_sql(query, con=engine))

elif query_option == "5. Average stop duration per violation":
    st.subheader("🕒 Average Stop Duration by Violation")
    query = """
        SELECT violation, mode() WITHIN GROUP (ORDER BY stop_duration) AS most_common_duration
        FROM traffic_stops_cleaned
        GROUP BY violation;
    """
    st.dataframe(pd.read_sql(query, con=engine))

elif query_option == "6. Common violations among drivers under 25":
    st.subheader("⚖️ Common Violations - Drivers under 25")
    query = """
        SELECT violation, COUNT(*) as count
        FROM traffic_stops_cleaned
        WHERE driver_age < 25
        GROUP BY violation
        ORDER BY count DESC
        LIMIT 10;
    """
    pd.read_sql(query, con=engine)

elif query_option == "7. Country with highest drug-related stops":
    st.subheader("🌍 Country with Highest Drug-Related Stops")
    query = """
        SELECT country_name, COUNT(*) as count
        FROM traffic_stops_cleaned
        WHERE drugs_related_stop = TRUE
        GROUP BY country_name
        ORDER BY count DESC;
    """
    st.dataframe(pd.read_sql(query, con=engine))

elif query_option == "8. Country with most searches conducted":
    st.subheader("🌍 Country with Most Searches Conducted")
    query = """
        SELECT country_name, COUNT(*) as count
        FROM traffic_stops_cleaned
        WHERE search_conducted = TRUE
        GROUP BY country_name
        ORDER BY count DESC;
    """
    st.dataframe(pd.read_sql(query, con=engine))
    
with st.expander("📄 View SQL Query"):
     st.code(query, language="sql")

st.subheader("📝 Add New Police Log Entry & Predict Outcome")

with st.form("add_log_form"):
    vehicle_number = st.text_input("Vehicle Number")
    driver_age = st.number_input("Driver Age", min_value=15, max_value=100)
    driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])
    violation = st.text_input("Violation")
    stop_duration = st.selectbox("Stop Duration", ["0-15 Min", "16-30 Min", "30+ Min"])
    country_name = st.text_input("Country Name")
    drugs_related_stop = st.checkbox("Drug Related Stop?")
    search_conducted = st.checkbox("Search Conducted?")
    stop_time = st.time_input("Stop Time")
    
    submitted = st.form_submit_button("Submit & Predict")

if submitted:
   
    likely_arrest = (search_conducted or drugs_related_stop) and (violation.lower() in ["drugs", "weapon", "dui"])
    result = "🔴 Likely Arrest" if likely_arrest else "🟢 Not Likely Arrest"
    
    st.success("New Log Submitted!")
    
    st.markdown(f"""
    ### 🚨 Prediction Result: {result}
    - Vehicle: `{vehicle_number}`
    - Age/Gender: {driver_age} / {driver_gender}
    - Violation: `{violation}`
    - Duration: `{stop_duration}`
    - Country: `{country_name}`
    - Search: {"Yes" if search_conducted else "No"}, Drugs: {"Yes" if drugs_related_stop else "No"}
    - Time: `{stop_time.strftime('%I:%M %p')}`
    """)

