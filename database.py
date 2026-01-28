import sqlite3
import pandas as pd

DB_NAME = "loan_predictions.db"
TABLE_NAME = "loan_dataa"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
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

def insert_record(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))

    sql = f"""
        INSERT INTO {TABLE_NAME} ({columns})
        VALUES ({placeholders})
    """

    cursor.execute(sql, list(data.values()))
    conn.commit()
    conn.close()

def fetch_all_records():
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df
