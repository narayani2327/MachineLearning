import sqlite3
import pandas as pd
import streamlit as st

DB_NAME = "loan_predictions.db"
TABLE_NAME = "loan_dataa"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            Loan_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Gender TEXT,
            Married TEXT,
            Dependents TEXT,
            Education TEXT,
            Self_Employed TEXT,
            ApplicantIncome REAL,
            CoapplicantIncome REAL,
            LoanAmount REAL,
            Loan_Amount_Term REAL,
            Credit_History INTEGER,
            Property_Area TEXT,
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

    # Remove Loan_ID if present (AUTOINCREMENT)
    data.pop("Loan_ID", None)
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