import sqlite3
import pandas as pd
import streamlit as st

DB_NAME = "property_prediction.db"
TABLE_NAME = "property_data"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Square_Footage REAL,
            Bedrooms INTEGER,
            Bathrooms INTEGER,
            Age INTEGER,
            Garage_Spaces INTEGER,
            Lot_Size REAL,
            Floors INTEGER,
            Neighborhood_Rating INTEGER,
            Condition INTEGER,
            School_Rating INTEGER,
            Has_Pool INTEGER,
            Renovated INTEGER,
            Location_Type_Dec TEXT,
            Distance_To_Center_KM REAL,
            Days_On_Market INTEGER,
            Prediction TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Save data to DB
def save_to_db(data: dict, prediction: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    data["Prediction"] = prediction

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))

    sql = f"""
        INSERT INTO {TABLE_NAME} ({columns})
        VALUES ({placeholders})
    """

    try:
        cursor.execute(sql, list(data.values()))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error saving data: {e}")

    conn.close()

# Fetch all data from DB
def fetch_all_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df
