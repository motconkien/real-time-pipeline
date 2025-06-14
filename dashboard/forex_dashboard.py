import streamlit as st
import pandas as pd
import psycopg2
import time

@st.cache_data(ttl=1)
def load_data():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="root",
        port=5432,
    )
    query = "SELECT * FROM forex_data ORDER BY timestamp DESC LIMIT 100;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Forex Data Dashboard")
placeholder = st.empty()

while True:
    df = load_data()
    placeholder.dataframe(df)
    time.sleep(2)  # Refresh every 5 seconds


